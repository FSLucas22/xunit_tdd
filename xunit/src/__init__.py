import importlib
from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import TestSuite as TestSuite
from xunit.src import testdecorator
from xunit.src.testexceptions import *
from xunit.src import testcolours
from xunit.src.formatters import *
import xunit.src.packagemanager  as pm
from typing import Type, Callable
from types import ModuleType
from pathlib import Path

color = testcolours
Test = testdecorator.Test
TestClass = testdecorator.TestClass


DEFAULT_SUMMARY = MixedTestSummary(
    TestSummary(FORMATTERS, 
            Status.PASSED,
            Status.FAILED, 
            Status.NOT_COMPLETED, 
            Status.FAILED_TO_RUN),
    SimpleTestSummary())


class TestRunner:
    capture_output: Callable[[str], None]
    summary: Summary
    
    def __init__(self, capture_output: Callable[[str], None] = print, 
                 summary: Summary=DEFAULT_SUMMARY) -> None:
        self.capture_output = capture_output
        self.summary = summary

    def _run(self, suite: TestSuite) -> None:
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        self.capture_output(self.summary.results(result))

    def run_for_class(self, cls: Type[TestCase]) -> None:
        self._run(TestSuite.from_test_case(cls))

    def run_for_module(self, module: ModuleType) -> None:
        self._run(TestSuite.from_module(module))

    def run_for_package(
        self, package: ModuleType, ignore: pm.Predicate=pm.ignore_name
        ) -> None:
        self._run(TestSuite.from_package(package, ignore))

    def run_for_module_name(self, module_name: str) -> None:
        module = importlib.import_module(module_name)
        self._run(TestSuite.from_module(module))

    def run_for_package_name(
        self, package_name: str, ignore: pm.Predicate=pm.ignore_name
        ) -> None:
        package = importlib.import_module(package_name)
        self._run(TestSuite.from_package(package, ignore=ignore))
