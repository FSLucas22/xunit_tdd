from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import TestSuite as TestSuite
from xunit.src import testdecorator
from xunit.src.testexceptions import *
from xunit.src import testcolours
import xunit.src.packagemanager  as pm
from typing import Type, Callable
from types import ModuleType


color = testcolours
Test = testdecorator.Test
TestClass = testdecorator.TestClass


class TestRunner:
    capture_output: Callable[[str], None]
    
    def __init__(self, capture_output: Callable[[str], None] = print) -> None:
        self.capture_output = capture_output

    def _run(self, suite: TestSuite) -> None:
        result = TestResult()
        summary = MixedTestSummary(
            PassedSummary(),
            ErrorInfoSummary(),
            SimpleTestSummary()
        )
        suite.register(result.save_status)
        suite.run()
        self.capture_output(summary.results(result))

    def run_for_class(self, cls: Type[TestCase]) -> None:
        self._run(TestSuite.from_test_case(cls))

    def run_for_module(self, module: ModuleType) -> None:
        self._run(TestSuite.from_module(module))

    def run_for_package(
        self, package: ModuleType, ignore: pm.Predicate=pm.ignore_name
        ) -> None:
        self._run(TestSuite.from_package(package, ignore))

    def run_for_module_path(self, path: str) -> None:
        self._run(TestSuite.from_path("test_module", path, False))

    def run_for_package_path(
        self, path: str, ignore: pm.Predicate=pm.ignore_name
        ) -> None:
        self._run(TestSuite.from_path("test_package", path, True, ignore))
