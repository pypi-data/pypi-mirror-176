from functools import singledispatch
import logging
from pathlib import Path
import h5py
import numpy as np
import xraylib
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from ..constants import KEYS, PHYSICAL
from vaxadium.core.units import Q_

logger = logging.getLogger(__name__)


@singledispatch
def get_units(arg):
    return arg


@get_units.register
def _(arg: bytes):
    return arg.decode()


@singledispatch
def get_value(arg):
    return arg


@get_value.register
def _(arg: bytes):
    return arg.decode()


@get_value.register
def _(arg: np.ndarray):
    if len(arg) == 1:
        return get_value(arg[0])
    elif isinstance(arg[0], bytes):  # who puts an isinstance in a singledispatch
        return arg.astype(str)
    else:
        return arg


class VanillaNexusReader(object):
    def __init__(self, nodes):
        self.f = None
        self.params = {}
        self.nodes = nodes
        self.pyfai = AzimuthalIntegrator()

    def _open(self, filename, swmr):
        self.filename = filename
        try:
            self.f = h5py.File(filename, "r", swmr=swmr)
        except:
            logger.error("File could not be opened {}".format(filename))
            print("File could not be opened")
            raise

    def _close(self):
        self.f.close()

    def _read(self):
        pass

    def _read_common(self):
        self.params[KEYS.PRIMARY_BEAM_ENERGY] = self._read_node(
            self.nodes.PRIMARY_BEAM_ENERGY
        )
        self.params[KEYS.PRIMARY_BEAM_WAVELENGTH] = (
            PHYSICAL.SPEED_OF_LIGHT
            * PHYSICAL.PLANCK_CONSTANT
            / self.params[KEYS.PRIMARY_BEAM_ENERGY]
        ).to("angstrom")
        self.params[KEYS.DETECTOR_DISTANCE] = self._read_node(
            self.nodes.DETECTOR_DISTANCE
        )

    def _serialize_common(self, serializer, source):
        serializer.start_object(source)
        serializer.add_property(KEYS.SOURCE_FILE, self.filename)
        serializer.add_property(KEYS.PRIMARY_BEAM_DIRECTION, [0, 0, 1])
        serializer.add_property(KEYS.PRIMARY_BEAM_ELLIPTICAL, False)
        serializer.add_property(
            KEYS.PRIMARY_BEAM_ENERGY, self.params[KEYS.PRIMARY_BEAM_ENERGY]
        )
        serializer.add_property(
            KEYS.DETECTOR_DISTANCE, self.params[KEYS.DETECTOR_DISTANCE]
        )

        # also do the pyfai values
        serializer.add_property(KEYS.DETECTOR_PONI1, Q_(self.pyfai.get_poni1(), "m"))
        serializer.add_property(KEYS.DETECTOR_PONI2, Q_(self.pyfai.get_poni2(), "m"))
        serializer.add_property(
            KEYS.DETECTOR_ROT1, Q_(self.pyfai.get_rot1(), "radians")
        )
        serializer.add_property(
            KEYS.DETECTOR_ROT2, Q_(self.pyfai.get_rot2(), "radians")
        )
        serializer.add_property(
            KEYS.DETECTOR_ROT3, Q_(self.pyfai.get_rot3(), "radians")
        )
        serializer.add_property(
            KEYS.DETECTOR_PYFAI_DIST, Q_(self.pyfai.get_dist(), "m")
        )
        serializer.add_property(
            KEYS.PRIMARY_BEAM_WAVELENGTH, Q_(self.pyfai.get_wavelength(), "m")
        )

    def read(self, filename, swmr=False):
        filename_path = Path(filename).expanduser().absolute()
        self._open(filename_path, swmr)
        self._read_common()
        self._read()
        self._close()

    def _get_node(self, address):
        if not bool(self.f):
            logger.error("Attempted to read node from closed hdf5 file object")
            raise IOError("hdf5 file object is closed")
        try:
            node = self.f[address]
        except KeyError:
            return False
        return node

    def _read_node(self, address):
        node = self._get_node(address)
        if node is False:
            return node
        value = get_value(node[()])
        if "units" in node.attrs.keys():
            units = get_units(node.attrs["units"])
            return Q_(value, units)
        elif isinstance(value, str):
            return value
        else:
            return Q_(value, None)

    def _read_node_new(self, nexkey):
        node = self._get_node(nexkey.address)
        if node is False:
            logger.warning("Node expected at {} not found.".format(nexkey.address))
            return
        value = get_value(node[()])
        units = None
        if "units" in node.attrs.keys():
            units = get_units(node.attrs["units"])
        elif nexkey.unit_required:
            units = nexkey.default_unit
            logger.warning(
                "Node requires units but none present at {}. Using default ({})".format(
                    nexkey.address, units
                )
            )

        if units is None:
            return value
        else:
            return Q_(value, units)

    def _add_param_to_params(self, key, nexkey):
        param = self._read_node_new(nexkey)
        self.params[key] = param

    def _read_axes_from_node(self, address):
        node = self._get_node(address)
        if "axes" in node.attrs.keys():
            axes_labels = get_value(node.attrs["axes"])[
                :-2
            ]  # -2 so as to avoid x and y
            axes_values = []
            for label in axes_labels:
                axis_values = self._read_node(address + "/" + label)
                try:
                    # TODO https://github.com/hgrecco/pint/issues/1195
                    a = axis_values.tolist()
                    axes_values.append(a)
                except TypeError:
                    axes_values += [[axis_values]]
            return axes_labels, axes_values
        else:
            return None, None

    def _get_number_of_members(self, address):
        try:
            n = len(self.f[address].keys())
        except KeyError:
            logger.debug(
                "cannot get number of members of {}, assuming n=0".format(address)
            )
            n = 0
        return n

    def search(self, target, values_also=True):
        """a helpful fucntion to find the params that match the target string"""
        for k, v in self.params.items():
            if target in k:
                if values_also:
                    print("{:25s} {}".format(k, v))
                else:
                    print(k)
