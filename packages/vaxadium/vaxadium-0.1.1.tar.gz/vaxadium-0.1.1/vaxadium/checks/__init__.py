from vaxadium.checks.basechecker import Checker
from vaxadium.checks.sample import SampleChecker
from vaxadium.checks.data import (
    AbsoluteIntensityChecker,
    DataSimilarityChecker,
    DataOverlapChecker,
    PercentageSignalChecker,
)
from vaxadium.checks.convergence import ConvergenceChecker
from vaxadium.checks.extractor import ExtractorChecker
from vaxadium.checks.calibration import CalibrationChecker


def run_diagnostics_checks(experiment):
    return [x().check(experiment) for x in Checker.__subclasses__()]
