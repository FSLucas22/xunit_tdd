from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import *
from xunit.src.testdecorator import *
from xunit.src.testexceptions import *
from xunit.src.testerrorinfo import *
from xunit.src.testcolors import *
from xunit.src.packagemanager import *
from typing import Type, Callable, cast
from types import ModuleType


class TestRunner:
    capture_output: Callable[[str], None]
    
    def __init__(self, capture_output: Callable[[str], None] = print) -> None:
        self.capture_output = capture_output

    def _run(self, suite: TestSuite) -> None:
        result = TestResult()
        summary = MixedTestSummary(
            PassedSummary(passed_formatter=green),
            ErrorInfoSummary(failed_formatter=red, notCompleted_formatter=yellow),
            SimpleTestSummary()
        )
        suite.run(result)
        self.capture_output(summary.results(result))

    def runForClass(self, cls: Type[TestCase]) -> None:
        self._run(TestSuite.fromTestCase(cls))

    def runForModule(self, module: ModuleType) -> None:
        self._run(TestSuite.fromModule(module))

    def runForPackage(
        self, package: ModuleType, ignore: Predicate=ignoreName
        ) -> None:
        self._run(TestSuite.fromPackage(package, ignore))

    def runForModulePath(self, path: str) -> None:
        self._run(TestSuite.fromPath("test_module", path, False))

    def runForPackagePath(
        self, path: str, ignore: Predicate=ignoreName
        ) -> None:
        self._run(TestSuite.fromPath("test_package", path, True, ignore))
