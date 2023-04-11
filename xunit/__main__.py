from xunit.src import *
from xunit.tests import *


def main() -> None:
    result = TestResult()
    summary = DetailedTestSummary()
    resumedSummary = TestSummary()
    suite = TestSuite.fromTestCase(
        TestCaseTest,
        TestSummaryTest,
        TestResultTest,
        TestSuiteTest
    )
    suite.run(result)
    print(summary.results(result))
    print(resumedSummary.results(result))
    

if __name__ == "__main__":
    main()
