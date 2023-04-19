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


def run(
    subject: Type[TestCase] | ModuleType | str,
    type: str,
    capture_output: Callable[[str], None]
    ) -> None:

    result = TestResult()
    summary = MixedTestSummary(
        PassedSummary(passed_formatter=green),
        ErrorInfoSummary(failed_formatter=red, notCompleted_formatter=yellow),
        SimpleTestSummary()
    )
    
    if type == "class":
        subject = cast(Type[TestCase], subject)
        suite = TestSuite.fromTestCase(subject)
    if type == "module":
        subject = cast(ModuleType, subject)
        suite = TestSuite.fromModule(subject)
    if type == "package":
        subject = cast(ModuleType, subject)
        suite = TestSuite.fromPackage(subject)
        
    suite.run(result)
    capture_output(summary.results(result))
