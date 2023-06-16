from .testcase import *
from .testresult import *
from .testsummary import *
from .testsuite import Runnable, TestSuite as TestSuite
from . import testdecorator
from .testexceptions import *
from . import testcolours
from .formatters import *
from .observer import *
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
