from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import *
from xunit.src.testdecorator import *
from xunit.src.testexceptions import *
from xunit.src.testerrorinfo import *
from xunit.src.testcolors import *
from xunit.src.packagemanager import *
from typing import Type, Callable, cast, ParamSpec
from types import ModuleType
from abc import ABC, abstractmethod


S = ParamSpec('S')


class TestRunner:
    capture_output: Callable[[str], None]
    
    def __init__(self, capture_output: Callable[[str], None]) -> None:
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

    def runForPackage(self, package: ModuleType) -> None:
        self._run(TestSuite.fromPackage(package))
        

def run(
    subject: Type[TestCase] | ModuleType | str,
    type: str,
    capture_output: Callable[[str], None]
    ) -> None:
    runner = TestRunner(capture_output)
    if type == "class":
        subject = cast(Type[TestCase], subject)
        runner.runForClass(subject)
    if type == "module":
        subject = cast(ModuleType, subject)
        runner.runForModule(subject)
    if type == "package":
        subject = cast(ModuleType, subject)
        runner.runForPackage(subject)
