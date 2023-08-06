"""Factory method to get a probe instance based on the probe type name."""

from .probetypes import (
    CipProbe,
    CpiProbe,
    HsiProbe,
    HvpsProbe,
    Hvps4V50Probe,
    Hvps4V150Probe,
    Hvps4H50Probe,
    Hvps4H150Probe,
    PipProbe,
    SpifProbe,
    TwoDcProbe,
    TwoDsHProbe,
    TwoDsVProbe,
)


def get_probe(probe_type: str) -> SpifProbe:
    """
    Get a probe instance from a probe type name.

    Parameters
    ----------
    probe_type : str
        Probe type name

    Returns
    -------
    SpifProbe
        Probe instance

    Raises
    ------
    ValueError
        Invalid probe type
    """
    probe = probe_type.lower()

    if probe == "cpi":
        return CpiProbe()
    elif probe == "hsi":
        return HsiProbe()
    elif probe == "2ds-v":
        return TwoDsVProbe()
    elif probe == "2ds-h":
        return TwoDsHProbe()
    elif probe == "2dc":
        return TwoDcProbe()
    elif probe == "hvps":
        return HvpsProbe()
    elif probe == "hvps4-v50":
        return Hvps4V50Probe()
    elif probe == "hvps4-h50":
        return Hvps4H50Probe()
    elif probe == "hvps4-v150":
        return Hvps4V150Probe()
    elif probe == "hvps4-h150":
        return Hvps4H150Probe()
    elif probe == "cip":
        return CipProbe()
    elif probe == "pip":
        return PipProbe()
    else:
        raise ValueError("Invalid probe type.")
