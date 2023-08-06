from vaxadium.core.units import Q_


class G4DIFFSIM:
    """when serializing into macro files, these are the defaults for the
    simulation"""

    DET_EBINS = 1000
    DET_DIST = Q_(20, "cm")
    DET_XPIXELS = 101
    DET_YPIXELS = 101
    DET_SIZE = Q_([51.0, 51.0, 0.01], "cm")
    DET_EMAX = Q_(80, "keV")
