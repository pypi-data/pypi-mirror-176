import logging
import os
import sys
from datetime import datetime, timedelta
from os import PathLike
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Union

import numpy as np
import numpy.typing as npt
import xarray as xr

from spifpy.probes import get_probe, SpifProbe

logger = logging.getLogger(__name__)


class SpifDatasetException(Exception):
    pass


class ParticleData(NamedTuple):
    """Typing for SPIF particle data."""

    image_id: int
    image: npt.NDArray
    timestamp: datetime
    metadata: Optional[Dict[str, Any]]


ParticleDataList = List[ParticleData]
FilePath = Union[str, PathLike]


class SpifDataset:
    """Generic SPIF dataset class."""

    SUPPORTED_PROBES = ["2DC", "2DS-H", "2DS-V", "CIP", "CPI", "HSI", "HVPS", "PIP"]
    DEFAULT_TIME_BASIS = "seconds since start_date"
    DEFAULT_TIME_FORMAT = "%F %T %z"

    def __init__(self, fpath: FilePath, probe: Optional[str] = None):
        self.fpath = fpath

        if not os.path.exists(self.fpath) or not os.path.isfile(self.fpath):
            raise FileNotFoundError(
                f"Spif Dataset file not found under path {self.fpath}"
            )

        self.probe: SpifProbe = self._read_probe(probe)
        self._init_dataset()

    def _init_dataset(self):
        self.probe_group = self._get_probe_group()
        self.core_group = self._get_core_group()
        self.start_date = self._get_start_date()
        self.data_dimension = self._get_data_dimension()
        self.image_widths = self._get_image_widths()
        self.image_heights = self._get_image_heights()
        self.image_indices = self._get_indices()

        self.datetimes = self._convert_datetimes()
        self.start_index, self.end_index = 0, len(self.datetimes) - 1

    def _convert_datetimes(self):
        particle_sec = self.core_group[self._get_seconds_variable_name()]
        particle_ns = self.core_group[self._get_nanoseconds_variable_name()]
        time_data = particle_sec[:] + particle_ns[:] * 1e-9

        particle_time_format = SpifDataset.DEFAULT_TIME_FORMAT
        if "strftime_format" in particle_sec.attrs:
            particle_time_format = particle_sec.strftime_format
        elif "strptime_format" in particle_sec.attrs:
            # Deprecated: will be removed in the future release because
            # 'strptime_format' has been renamed to 'strftime_format'
            particle_time_format = particle_sec.strptime_format

        time_basis = (
            particle_sec.units
            if "units" in particle_sec.attrs
            else SpifDataset.DEFAULT_TIME_BASIS
        )

        datetimes = self.convert_netcdf_time(
            time_data.data,
            time_basis,
            particle_time_format,
            start_date=self.start_date,
        )

        return datetimes

    def _get_core_group(self):
        return xr.open_dataset(
            self.fpath,
            group=f"{self.probe.get_name()}/core/",
            engine="h5netcdf",
            decode_times=False,
        )

    def _get_data_dimension(self):
        return self.core_group[self._get_image_data_field_name()].ndim

    def _get_image_data_field_name(self):
        return "image"

    def _get_image_heights(self):
        return np.repeat(
            self.probe_group["pixels"].data, self.image_widths.shape[0]
        ).astype(np.uint32)

    def _get_image_widths(self):
        return self.core_group["image_len"].data.astype(np.uint32)

    def _get_images_axis_name(self):
        return "Images"

    def _get_images_batch(self, batch_start: int, batch_end: int):
        if self.data_dimension == 3:
            return self.core_group[
                {self._get_images_axis_name(): slice(batch_start, batch_end)}
            ]
        elif self.data_dimension == 1:
            return self.core_group[
                {
                    self._get_pixels_axis_name(): slice(
                        self.image_indices[batch_start],
                        self.image_indices[batch_end],
                    )
                }
            ]
        else:
            raise SpifDatasetException("2D image arrays are not supported")

    def _get_pixels_axis_name(self):
        return "Pixels"

    def _get_seconds_variable_name(self):
        return "image_sec"

    def _get_nanoseconds_variable_name(self):
        return "image_ns"

    def _get_indices(self):
        indices = np.cumsum(self.image_widths * self.image_heights)
        indices = np.insert(indices, 0, 0)
        return indices

    def _get_probe_group(self):
        return xr.open_dataset(
            self.fpath,
            engine="h5netcdf",
            group=self.probe.get_name(),
            decode_times=False,
        )

    def _get_start_date(self):
        return xr.open_dataset(self.fpath, engine="h5netcdf").start_date.strip()

    def _process_batch(self, batch, *args, **kwargs):
        if self.data_dimension == 3:
            return self._process_batch_3d(batch, *args, **kwargs)
        elif self.data_dimension == 1:
            return self._process_batch_1d(batch, *args, **kwargs)
        else:
            raise SpifDatasetException("2D image arrays are not supported")

    def _process_batch_3d(self, batch, *args, **kwargs):
        batch_start, batch_end = args

        images = batch[self._get_image_data_field_name()].data
        widths = self.image_widths[batch_start:batch_end]
        heights = self.image_heights[batch_start:batch_end]
        datetimes = self.datetimes[batch_start:batch_end]

        result: ParticleDataList = []

        for image_num, (
            image,
            image_width,
            image_height,
            timestamp,
        ) in enumerate(zip(images, widths, heights, datetimes)):
            image_id = batch_start + image_num
            image = image[:image_width, :]
            image = image.reshape((-1, image_height)).T

            result.append(ParticleData(image_id, image, timestamp, None))

        return result

    def _process_batch_1d(self, batch, *args, **kwargs):
        batch_start, batch_end = args

        images = batch[self._get_image_data_field_name()].data
        widths = self.image_widths[batch_start:batch_end]
        heights = self.image_heights[batch_start:batch_end]
        datetimes = self.datetimes[batch_start:batch_end]

        batch_indices = np.cumsum(widths * heights)
        batch_indices = np.insert(batch_indices, 0, 0)

        result: ParticleDataList = []

        for image_num, timestamp in enumerate(datetimes):
            image_id = batch_start + image_num
            if batch_indices[image_num + 1] > len(images):
                raise SpifDatasetException(
                    "Not enough pixel data: number of elements "
                    + "in a pixels array do not equal to multiplication "
                    + "of image widths by heights."
                )

            image = images[batch_indices[image_num] : batch_indices[image_num + 1]]
            if image.shape != (0,):
                image = image.reshape((widths[image_num], heights[image_num])).T

            result.append(ParticleData(image_id, image, timestamp, None))

        return result

    def _read_probe(self, probe: Optional[str] = None) -> SpifProbe:
        available_probes = self.get_available_probes()

        if not probe:
            if len(available_probes) > 1:
                logger.warn(
                    "More than 1 probe found in the dataset file. "
                    f"By default the first probe {available_probes[0]} will be used. "
                    "To change that, specify probe parameter when calling SpifDataset constructor."
                )

            if len(available_probes) >= 1:
                probe_name = available_probes[0]
                return get_probe(probe_name)

            raise SpifDatasetException(
                "No probe groups found in the dataset file. "
                "The file is likely corrupted."
            )

        return get_probe(probe)

    @staticmethod
    def convert_netcdf_time(time_data, time_basis, basis_format, start_date):
        """
        Convert time in standard NetCDF time format into datetime object.
        Author: Matt Freer (mfreer@gmail.com)
        Parameters
        ----------
        time_data : array
            Timestamps of data contained within the file,
            seconds since `start_date`
        time_units : str
            Time units string in the format: 'seconds since start_date'
            `start_date` string is then replaced with the start date parameter
        basis_format: str
            Time format string, e.g. '%F %T %z'
        start_date: str
            Start date timestamp in a string format
        Returns
        -------
        list of datetime object
            Absolute datetimes of provided times.
        """
        TIME_UNITS_DEFAULT = "seconds since "
        basis_format = basis_format.replace("%F", "%Y-%m-%d")
        basis_format = basis_format.replace("%T", "%H:%M:%S")

        if not basis_format.startswith(TIME_UNITS_DEFAULT):
            basis_format = TIME_UNITS_DEFAULT + basis_format

        time_basis = time_basis.replace("start_date", start_date)
        try:
            tb_dt = datetime.strptime(time_basis, basis_format)
        except ValueError:
            tb_dt = datetime.strptime(
                time_basis, basis_format.replace("%z", "").strip()
            )
        time_dt = [tb_dt + timedelta(seconds=t) for t in time_data]

        return time_dt

    def get_available_probes(self) -> List[str]:
        """
        Based on the file, return the list of its probes.

        Returns
        -------
        List[str]
            List of probes, ordered alphabetically,
            data of which this file contains
        """
        file_probes = []

        for probe in SpifDataset.SUPPORTED_PROBES:
            try:
                dataset = xr.open_dataset(
                    self.fpath,
                    engine="h5netcdf",
                    group=f"{probe}/core/",
                    decode_times=False,
                )
                dataset.close()
                file_probes.append(probe)
            except Exception:  # nosec
                # we shouldn't ideally continue after exception,
                # potentially look for a better solution to check available
                # probes in the file
                continue

        return sorted(file_probes)

    def get_end_time(self) -> datetime:
        """Get timestamp of the last image in the dataset."""
        return self.datetimes[-1]

    def get_file_path(self) -> FilePath:
        """Get dataset file path."""
        return self.fpath

    def get_image_id_by_timestamp(self, timestamp: datetime) -> int:
        """
        Get image index by timestamp.

        Considering that all timestamps are ordered in the dataset,
        look up an image that has a timestamp closest to the passed value.

        If the passed timestamp is earlier than the timestamp of the first image,
        0 will be returned. If it is later than the timestamp of the last image,
        the index of the last image will be returned.
        """
        if len(self.datetimes) == 0:
            return 0

        if timestamp > self.datetimes[-1]:
            return len(self.datetimes) - 1

        if timestamp < self.datetimes[0]:
            return 0

        for i, array_timestamp in enumerate(self.datetimes):
            if array_timestamp > timestamp:
                return i

        return 0

    def get_images_number(self) -> int:
        """Get number of images in the dataset."""
        return len(self.datetimes)

    def get_probe(self) -> SpifProbe:
        """Get an instance of the currently open probe."""
        return self.probe

    def get_start_time(self) -> datetime:
        """Get timestamp of the first image in the dataset."""
        return self.datetimes[0]

    def read(self, start: int = 0, end: int = sys.maxsize) -> Iterator[ParticleData]:
        start_index = max(self.start_index, start)
        end_index = min(self.end_index, end)

        for batch_start in range(start_index, end_index):
            batch_end = batch_start + 1

            if batch_end > end_index + 1:
                batch_end = end_index + 1

            batch = self._get_images_batch(batch_start, batch_end)
            batch = self._process_batch(batch, batch_start, batch_end)

            yield batch[0]

    def read_batch(
        self, start: int = 0, end: int = sys.maxsize, batch_size=1
    ) -> Iterator[ParticleDataList]:
        start_index = max(self.start_index, start)
        end_index = min(self.end_index, end)

        for batch_start in range(start_index, end_index, batch_size):
            batch_end = batch_start + batch_size

            if batch_end > end_index + 1:
                batch_end = end_index + 1

            batch = self._get_images_batch(batch_start, batch_end)
            batch = self._process_batch(batch, batch_start, batch_end)

            yield batch
