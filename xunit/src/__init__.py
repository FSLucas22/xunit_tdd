from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import TestSuite as TestSuite
from xunit.src import testdecorator
from xunit.src.testexceptions import *
from xunit.src import testcolours
from xunit.src.loaders import *
from xunit.src.formatters import *
from xunit.src.observer import *
from typing import Callable


color = testcolours
Test = testdecorator.Test
TestClass = testdecorator.TestClass


DEFAULT_SUMMARY = MixedTestSummary(
    TestSummary(FORMATTERS),
    SimpleTestSummary())


class TestRunner(SubjectImp):
    capture_output: Callable[[str], None]
    summary: Summary
    suite: TestSuite | None
    
    def __init__(self, capture_output: Callable[[str], None] = print, 
                 summary: Summary=DEFAULT_SUMMARY,
                 *observers: Observer,
                 suite: TestSuite | None = None) -> None:
        
        self.capture_output = capture_output
        self.summary = summary
        self.suite = suite
        super().__init__(*observers)

    def run(self) -> None:
        result = TestResult()
        if self.suite is not None:
            self.suite.register(result.save_status)
            self.suite.run()
        self.capture_output(self.summary.results(result))
