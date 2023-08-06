import logging
from copy import deepcopy

import numpy as np
import xraylib
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator

from .nexus_reader import VanillaNexusReader
from ..constants import J15NXS, KEYS
from vaxadium.core.units import Q_

logger = logging.getLogger(__name__)


class NexusDataIterator:
    def __init__(self, nxs):
        self._nxs = nxs
        self._index = 0

    def __next__(self):
        if self._nxs.n_points == 0:
            logger.warn("Iterating over nxs handler with no data points")
        if self._index < self._nxs.n_points:
            axis_names, axis_values, result = self._nxs.read_data_and_axes(self._index)
            self._index += 1
            return axis_names, axis_values, result
        raise StopIteration


class NxxpdfNexusReader(VanillaNexusReader):
    def __init__(self):
        super().__init__(J15NXS)
        self.n_points = 0

    def __iter__(self):
        return NexusDataIterator(self)

    def read_data(self, frame=0, swmr=False):
        raise DeprecationWarning
        logger.info("loading data slice {} from {}".format(frame, self.filename))
        self._open(self.filename, swmr)
        data = self.f[self.nodes.DATA][frame]
        self._close()
        return data

    def read_data_and_axes(self, frame=0, swmr=False):
        logger.info("loading data slice {} from {}".format(frame, self.filename))
        self._open(self.filename, swmr)
        data = self.f[self.nodes.DATA][frame]
        axis_names, axis_value = self._read_axes_from_node(self.nodes.DETECTOR_FOR_AXES)
        self._close()
        logger.info(
            "axis name/s: {}, axis value = {}".format(
                axis_names[0], axis_value[0][frame]
            )
        )
        return axis_names, axis_value[0][frame], data

    def _read(self):
        try:
            n_points = len(self._read_node(self.nodes.UNIQUE_KEYS).magnitude)
        except TypeError:
            n_points = 1
        self.n_points = n_points

        self.params[KEYS.PRIMARY_BEAM_EXTENT] = self._read_node(
            self.nodes.PRIMARY_BEAM_EXTENT
        )
        self.params[KEYS.PIXEL_SIZE_SLOW] = self._read_node(self.nodes.PIXEL_SIZE_SLOW)
        self.params[KEYS.PIXEL_SIZE_FAST] = self._read_node(self.nodes.PIXEL_SIZE_FAST)
        self.params[KEYS.DETECTOR_THICKNESS] = self._read_node(
            self.nodes.DETECTOR_THICKNESS
        )
        self.params[KEYS.DETECTOR_DENSITY] = self._read_node(
            self.nodes.DETECTOR_DENSITY
        )
        self.params[KEYS.DETECTOR_MATERIAL] = self._read_node(
            self.nodes.DETECTOR_MATERIAL
        )
        self.params[KEYS.BACKGROUND_FILEPATH] = self._read_node(
            self.nodes.BACKGROUND_FILEPATH
        )
        # Read the sample
        self.params[KEYS.SAMPLEn_CHEMICAL_FORMULA.format(0)] = self._read_node(
            self.nodes.SAMPLE_CHEMICAL_FORMULA
        )
        self.params[KEYS.SAMPLEn_DENSITY.format(0)] = self._read_node(
            self.nodes.SAMPLE_DENSITY
        )
        self.params[KEYS.SAMPLEn_DIMENSIONS.format(0)] = self._read_node(
            self.nodes.SAMPLE_DIMENSIONS
        )

        self.params[KEYS.SAMPLEn_NAME.format(0)] = self._read_node(
            self.nodes.SAMPLE_NAME
        )
        self.params[KEYS.SAMPLEn_DESCRIPTION.format(0)] = self._read_node(
            self.nodes.SAMPLE_DESCRIPTION
        )
        self.params[KEYS.SAMPLEn_VOLUME_FRACTION.format(0)] = self._read_node(
            self.nodes.SAMPLE_VOLUME_FRACTION
        )
        # Read the number of linked files by inspecting members of the containers group
        self.params[KEYS.SAMPLE_NUMBER] = self._get_number_of_members(
            self.nodes.CONTAINERS
        )  # one container is background; sample is not container
        for i in range(1, self.params[KEYS.SAMPLE_NUMBER]):
            self.params[KEYS.SAMPLEn_FILEPATH] = self._read_node(
                self.nodes.CONTAINERn_FILEPATH.format(i)
            )
            self.params[KEYS.SAMPLEn_CHEMICAL_FORMULA.format(i)] = self._read_node(
                self.nodes.CONTAINERn_CHEMICAL_FORMULA.format(i)
            )
            self.params[KEYS.SAMPLEn_DENSITY.format(i)] = self._read_node(
                self.nodes.CONTAINERn_DENSITY.format(i)
            )
            self.params[KEYS.SAMPLEn_NAME.format(i)] = self._read_node(
                self.nodes.CONTAINERn_NAME.format(i)
            )
            self.params[KEYS.SAMPLEn_DESCRIPTION.format(i)] = self._read_node(
                self.nodes.CONTAINERn_DESCRIPTION.format(i)
            )
            self.params[KEYS.SAMPLEn_VOLUME_FRACTION.format(i)] = self._read_node(
                self.nodes.CONTAINERn_VOLUME_FRACTION.format(i)
            )
            self.params[KEYS.SAMPLEn_DIMENSIONS.format(i)] = self._read_node(
                self.nodes.CONTAINERn_DIMENSIONS.format(i)
            )
            # read the container data
            self.params[KEYS.SAMPLEn_DATA.format(i)] = self._read_node(
                self.nodes.SAMPLEn_DATA.format(i)
            )

        # read the background data
        self.params[KEYS.BACKGROUND_DATA] = self._read_node(self.nodes.BACKGROUND_DATA)

        # read the actual data
        self.params[KEYS.DATA] = self._read_node(self.nodes.DATA)

        # configure the pyfai
        if str(self.filename) == "/dls/i15-1/data/2020/cy27040-1/i15-1-37202.nxs":
            self.params[
                KEYS.DETECTOR_PONI_FILEPATH
            ] = "/dls/i15-1/data/2020/cy27040-1/processing/vaxadium/i15-1-36503.poni"  # TODO make processing chain which inserts this
        else:
            self.params[
                KEYS.DETECTOR_PONI_FILEPATH
            ] = "/dls/science/users/fer45166/geant4/testing/cy22337-3/i15-1-35785_1.poni"  # TODO make processing chain which inserts this
        # self.params[KEYS.DETECTOR_PONI_FILEPATH] = self._read_node(self.nodes.DETECTOR_PONI_FILEPATH)
        self.pyfai.load(self.params[KEYS.DETECTOR_PONI_FILEPATH])
        self.params[KEYS.PIXEL_NUMBERS] = self._read_node(self.nodes.PIXEL_NUMBERS)

        # now the axis
        # axes_names, axes_values = self._read_axes_from_node(self.nodes.DETECTOR_FOR_AXES)
        # self.params[KEYS.AXES_NAMES] = axes_names
        # self.params[KEYS.AXES_VALUES] = axes_values

        # now the attenuation in place of an I0 measurement
        self.params[KEYS.ATTENUATOR_TRANSMISSION] = self._read_node(
            self.nodes.ATTENUATOR_TRANSMISSION
        )

    def serialize(self, serializer):
        self._serialize_common(serializer, "j15")
        serializer.add_property(
            KEYS.PRIMARY_BEAM_HALF_DIMENSIONS, self.params[KEYS.PRIMARY_BEAM_EXTENT] / 2
        )
        pixel_size_x = self.params[KEYS.PIXEL_SIZE_FAST].to("m").magnitude
        pixel_size_y = self.params[KEYS.PIXEL_SIZE_SLOW].to("m").magnitude
        pixel_sizes = Q_(np.asarray((pixel_size_x, pixel_size_y)), "m")
        serializer.add_property(KEYS.PIXEL_SIZES, pixel_sizes)

        # probably something like self.pyfai.position_array()[0,0] for origin
        # and then self.pyfai.rotation_matrix() for ui, uk
        detector_origin = Q_(np.asarray((0.305, 0.305, 0.234)), "m")
        serializer.add_property(
            KEYS.DETECTOR_ORIGIN, detector_origin
        )  # TODO bring this in from pyfai
        serializer.add_property(
            KEYS.DETECTOR_UI, (-0.707, 0.707, 0)
        )  # TODO bring this in from pyfai
        serializer.add_property(
            KEYS.DETECTOR_UK, (0.0, 0.0, -1.0)
        )  # TODO bring this in from pyfai

        serializer.add_property(
            KEYS.DETECTOR_THICKNESS, self.params[KEYS.DETECTOR_THICKNESS]
        )
        serializer.add_property(
            KEYS.DETECTOR_MATERIAL, self.params[KEYS.DETECTOR_MATERIAL]
        )
        serializer.add_property(
            KEYS.DETECTOR_DENSITY, self.params[KEYS.DETECTOR_DENSITY]
        )

        serializer.add_property(KEYS.SAMPLE_NUMBER, self.params[KEYS.SAMPLE_NUMBER])

        for i in range(self.params[KEYS.SAMPLE_NUMBER]):
            for keyn in [
                KEYS.SAMPLEn_CHEMICAL_FORMULA,
                KEYS.SAMPLEn_DENSITY,
                KEYS.SAMPLEn_NAME,
                KEYS.SAMPLEn_VOLUME_FRACTION,
                KEYS.SAMPLEn_DIMENSIONS,
                KEYS.SAMPLEn_DESCRIPTION,
            ]:
                key = keyn.format(i)
                serializer.add_property(key, self.params[key])
            xrl_compound = xraylib.CompoundParser(
                self.params[KEYS.SAMPLEn_CHEMICAL_FORMULA.format(i)]
            )
            atoms = [xraylib.AtomicNumberToSymbol(x) for x in xrl_compound["Elements"]]
            mass_fractions = xrl_compound["massFractions"]
            serializer.add_property(KEYS.SAMPLEn_ATOMS.format(i), atoms)
            serializer.add_property(
                KEYS.SAMPLEn_MASS_FRACTIONS.format(i), mass_fractions
            )

        # and the background data
        serializer.add_property(KEYS.BACKGROUND_DATA, self.params[KEYS.BACKGROUND_DATA])
        serializer.add_property(
            KEYS.PIXEL_NUMBERS, tuple(self.params[KEYS.PIXEL_NUMBERS].magnitude)
        )

        # and the data
        serializer.add_property(KEYS.DATA, self.params[KEYS.DATA])

        # and the axes
        # serializer.add_property(KEYS.AXES_NAMES, self.params[KEYS.AXES_NAMES])
        # serializer.add_property(KEYS.AXES_VALUES, self.params[KEYS.AXES_VALUES])

        # and the attenuator
        serializer.add_property(
            KEYS.ATTENUATOR_TRANSMISSION, self.params[KEYS.ATTENUATOR_TRANSMISSION]
        )
