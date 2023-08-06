""" spifpy library public imports """

from pkg_resources import DistributionNotFound, get_distribution

from .core.dataset import SpifDataset

try:
    __version__ = get_distribution("spifpy").version
except DistributionNotFound:
    # package is not installed
    pass

__all__ = ["SpifDataset"]
