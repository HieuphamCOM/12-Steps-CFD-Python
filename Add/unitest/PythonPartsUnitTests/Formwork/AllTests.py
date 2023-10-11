""" Unittest for module NemAll_Python_IFW_Input
"""

# pylint: disable=import-outside-toplevel
# pylint: disable=wrong-import-position
# pylint: disable=possibly-unused-variable

from __future__ import annotations
from typing import TYPE_CHECKING

import os
import sys
import pathlib
import unittest
import coverage
 

BASE_DIR = os.path.join( pathlib.Path(__file__).parent.resolve().parent.parent, "PythonPartsContent")

if (exist_framework_path := 2) < len(sys.argv):
    sys.path.append(sys.argv[2])
    sys.path.append(BASE_DIR)

from TestHelper import UnitTestRunner
from TestHelper.UnitTestRunnerUtil import UnitTestRunnerUtil

if TYPE_CHECKING:
    import NemAll_Python_IFW_ElementAdapter as AllplanEleAdapter


# ----------------- Test suites


def __run_unit_tests(
    doc: AllplanEleAdapter.DocumentAdapter, code_coverage: bool
) -> unittest.TestResult:
    """run the unit tests

    Args:
        doc:           document of the Allplan drawing files
        code_coverage: description

    Returns:
        test result
    """

    # ----------------- Factories
    from FunctionTest.Factories import TestBIM2WallFactory
    from FunctionTest.Factories import TestBIM2FaceFactory
    from FunctionTest.Method import TestBIM2Face
    from FunctionTest.Method import TestShapeRecognizer
    from FunctionTest.Controller import TestShapeCtl
    from FunctionTest.Controller import TestFormingCtl
    from FunctionTest.Data import TestDataHandler
    from FunctionTest.Utility import TestUtility
    from FunctionTest.Elements import TestSetAttributes
    from FunctionTest.Elements import TestSetCommonProp


    # ----------------- execute the test

    return UnitTestRunnerUtil.run_unit_tests(
        [item[1] for item in locals().items() if getattr(item[1], "suite", None)],
        code_coverage,
        doc,
        single_test=None,
    )


def run_tests() -> bool:
    """run the tests

    Returns:
        test result
    """

    return UnitTestRunner.execute_tests(__run_unit_tests, "", True)


if __name__ == "__main__":
    # Start coverage measurement
    cov = coverage.Coverage()
    cov.start()

    # Run the tests
    RET = run_tests()

    # Stop coverage measurement and generate report
    cov.stop()
    cov.save()

    cov.xml_report(outfile="coverage.xml")
