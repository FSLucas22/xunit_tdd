from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import TestSuite as TestSuite
from xunit.src import testdecorator
from xunit.src.testexceptions import *
from xunit.src import testcolors
from xunit.src.packagemanager import *
from typing import Type, Callable, cast
from types import ModuleType


color = testcolors
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
        suite.run(result)
        self.capture_output(summary.results(result))

    def runForClass(self, cls: Type[TestCase]) -> None:
        self._run(TestSuite.from_test_case(cls))

    def runForModule(self, module: ModuleType) -> None:
        self._run(TestSuite.from_module(module))

    def runForPackage(
        self, package: ModuleType, ignore: Predicate=ignoreName
        ) -> None:
        self._run(TestSuite.from_package(package, ignore))

    def runForModulePath(self, path: str) -> None:
        self._run(TestSuite.from_path("test_module", path, False))

    def runForPackagePath(
        self, path: str, ignore: Predicate=ignoreName
        ) -> None:
        self._run(TestSuite.from_path("test_package", path, True, ignore))
