import numpy as np
import xraylib
from pyFAI.detectors import Detector as PDetector
from .nexus_reader import VanillaNexusReader
from ..constants import G4NXS, KEYS, NEWG4NEXUSKEYS
from vaxadium.core.units import Q_


class G4NexusReader(VanillaNexusReader):
    def __init__(self):
        super().__init__(G4NXS)

    def _read(self):

        self.params[KEYS.PRIMARY_BEAM_HALF_X] = self._read_node(
            self.nodes.PRIMARY_BEAM_HALF_X
        )
        self.params[KEYS.PRIMARY_BEAM_HALF_Y] = self._read_node(
            self.nodes.PRIMARY_BEAM_HALF_Y
        )
        self.params[KEYS.DETECTOR_HALF_X] = self._read_node(self.nodes.DETECTOR_HALF_X)
        self.params[KEYS.DETECTOR_HALF_Y] = self._read_node(self.nodes.DETECTOR_HALF_Y)
        self.params[KEYS.PRIMARY_PHOTONS] = self._read_node(self.nodes.PRIMARY_PHOTONS)
        self.params[KEYS.DATA] = self._read_node(self.nodes.DATA)
        self.params[KEYS.SAMPLE_NUMBER] = self._get_number_of_members(
            self.nodes.SAMPLES
        )
        self.params[KEYS.DETECTOR_ENERGY_BINS] = self._read_node(
            self.nodes.DETECTOR_ENERGY_BINS
        )

        for i in range(self.params[KEYS.SAMPLE_NUMBER]):
            self.params[KEYS.SAMPLEn_ATOMS.format(i)] = self._read_node(
                self.nodes.SAMPLEn_ATOMS.format(i)
            )
            self.params[KEYS.SAMPLEn_DIMENSIONS.format(i)] = self._read_node(
                self.nodes.SAMPLEn_DIMENSIONS.format(i)
            )
            self.params[KEYS.SAMPLEn_DENSITY.format(i)] = self._read_node(
                self.nodes.SAMPLEn_DENSITY.format(i)
            )
            self.params[KEYS.SAMPLEn_MASS_FRACTIONS.format(i)] = self._read_node(
                self.nodes.SAMPLEn_MASS_FRACTIONS.format(i)
            )
            self.params[KEYS.SAMPLEn_NAME.format(i)] = self._read_node(
                self.nodes.SAMPLEn_NAME.format(i)
            )

        # configure the pyfai
        data_shape = self.params[KEYS.DATA].magnitude[0].shape
        pixel_x = (
            2 * self.params[KEYS.DETECTOR_HALF_X].to("m").magnitude / data_shape[1]
        )
        pixel_y = (
            2 * self.params[KEYS.DETECTOR_HALF_Y].to("m").magnitude / data_shape[0]
        )
        self.pyfai.detector = PDetector(
            pixel1=pixel_x, pixel2=pixel_y, max_shape=data_shape
        )
        self.pyfai.set_dist(self.params[KEYS.DETECTOR_DISTANCE].to("m").magnitude)
        self.pyfai.set_poni1(self.params[KEYS.DETECTOR_HALF_X].to("m").magnitude)
        self.pyfai.set_poni2(self.params[KEYS.DETECTOR_HALF_Y].to("m").magnitude)
        self.pyfai.set_wavelength(
            self.params[KEYS.PRIMARY_BEAM_WAVELENGTH].to("m").magnitude
        )

    def serialize(self, serializer):
        self._serialize_common(serializer, "g4")
        dimensions_x = self.params[KEYS.PRIMARY_BEAM_HALF_X].to("m").magnitude
        dimensions_y = self.params[KEYS.PRIMARY_BEAM_HALF_Y].to("m").magnitude
        dimensions = Q_(np.asarray((dimensions_x, dimensions_y)), "m")
        serializer.add_property(KEYS.PRIMARY_BEAM_HALF_DIMENSIONS, dimensions)
        serializer.add_property(KEYS.PRIMARY_PHOTONS, self.params[KEYS.PRIMARY_PHOTONS])

        data_shape = self.params[KEYS.DATA].magnitude[0].shape
        pixel_x = (
            2 * self.params[KEYS.DETECTOR_HALF_X].to("m").magnitude / data_shape[1]
        )
        pixel_y = (
            2 * self.params[KEYS.DETECTOR_HALF_Y].to("m").magnitude / data_shape[0]
        )
        pixel_sizes = Q_(np.asarray((pixel_x, pixel_y)), "m")
        serializer.add_property(KEYS.PIXEL_SIZES, pixel_sizes)
        serializer.add_property(KEYS.PIXEL_NUMBERS, data_shape)
        serializer.add_property(
            KEYS.DETECTOR_ENERGY_BINS, self.params[KEYS.DETECTOR_ENERGY_BINS]
        )

        origin_x = self.params[KEYS.DETECTOR_HALF_X].to("m").magnitude
        origin_y = self.params[KEYS.DETECTOR_HALF_Y].to("m").magnitude
        origin_z = self.params[KEYS.DETECTOR_DISTANCE].to("m").magnitude

        detector_origin = Q_(np.asarray((origin_x, origin_y, origin_z)), "m")

        serializer.add_property(KEYS.DETECTOR_ORIGIN, detector_origin)
        ui = tuple(-self.pyfai.rotation_matrix()[0])
        uk = tuple(-self.pyfai.rotation_matrix()[2])
        serializer.add_property(KEYS.DETECTOR_UI, ui)
        serializer.add_property(KEYS.DETECTOR_UK, uk)

        serializer.add_property(KEYS.SAMPLE_NUMBER, self.params[KEYS.SAMPLE_NUMBER])
        for i in range(self.params[KEYS.SAMPLE_NUMBER]):
            serializer.add_property(
                KEYS.SAMPLEn_ATOMS.format(i), self.params[KEYS.SAMPLEn_ATOMS.format(i)]
            )
            serializer.add_property(
                KEYS.SAMPLEn_DENSITY.format(i),
                self.params[KEYS.SAMPLEn_DENSITY.format(i)],
            )
            serializer.add_property(
                KEYS.SAMPLEn_DIMENSIONS.format(i),
                self.params[KEYS.SAMPLEn_DIMENSIONS.format(i)],
            )
            # need to convert list of atoms and mass fractions to chemical_formula
            atoms = self.params[KEYS.SAMPLEn_ATOMS.format(i)].astype(str)
            atomic_weights = [
                xraylib.AtomicWeight(xraylib.SymbolToAtomicNumber(x)) for x in atoms
            ]
            molar_fractions = np.array(
                [
                    mass / weight
                    for (weight, mass) in zip(
                        atomic_weights,
                        self.params[KEYS.SAMPLEn_MASS_FRACTIONS.format(i)].magnitude,
                    )
                ]
            )
            chemical_formula = [
                "{}{:.5f}".format(sym, num)
                for (sym, num) in zip(atoms, molar_fractions / molar_fractions.min())
            ]
            serializer.add_property(
                KEYS.SAMPLEn_CHEMICAL_FORMULA.format(i), "".join(chemical_formula)
            )
            serializer.add_property(
                KEYS.SAMPLEn_NAME.format(i), self.params[KEYS.SAMPLEn_NAME.format(i)]
            )
        serializer.add_property(KEYS.DATA, self.params[KEYS.DATA])
