from xunit.src import *
from xunit.tests import *


def main() -> None:
    result = TestResult()
    summary = MixedTestSummary(DetailedTestSummary(), SimpleTestSummary())
    suite = TestSuite.fromTestCase(
        TestCaseTest,
        TestSummaryTest,
        TestResultTest,
        TestSuiteTest,
        TestTest,
        TestErrors
    )
    suite.run(result)
    print(summary.results(result))
    

if __name__ == "__main__":
    main()
