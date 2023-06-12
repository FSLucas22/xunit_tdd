from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import Runnable, TestSuite as TestSuite
from xunit.src import testdecorator
from xunit.src.testexceptions import *
from xunit.src import testcolours
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
    suite: Runnable | None
    
    def __init__(self, capture_output: Callable[[str], None] = print, 
                 summary: Summary=DEFAULT_SUMMARY,
                 *observers: Observer,
                 runnable: Runnable | None = None) -> None:
        
        self.capture_output = capture_output
        self.summary = summary
        self.runnable = runnable
        super().__init__(*observers)

    def run(self) -> None:
        result = TestResult()
        if self.runnable is not None:
            self.runnable.register(result.save_status)
            self.runnable.run()
        self.capture_output(self.summary.results(result))
