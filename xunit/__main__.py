from xunit.src import *
from xunit.tests import *
import colorama
import os


def main() -> None:
    result = TestResult()
    summary = MixedTestSummary(
        ErrorInfoSummary(failed_formatter=red, notCompleted_formatter=yellow),
        PassedSummary(passed_formatter=green),
        SimpleTestSummary()
    )
    suite = TestSuite.fromTestCase(
        TestCaseTest,
        TestSummaryTest,
        TestResultTest,
        TestSuiteTest,
        TestTest,
        TestErrors,
        TestColors
    )
    suite.run(result)
    print(summary.results(result))
    

if __name__ == "__main__":
    if os.name == "nt":
        colorama.init()
    main()
