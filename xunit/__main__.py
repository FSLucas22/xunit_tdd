from xunit.src import *
from xunit.tests import *


def main() -> None:
    result = TestResult()
    summary = DetailedTestSummary()
    resumedSummary = TestSummary()
    suite = TestSuite.fromTestCase(TestCaseTest)
    suite.run(result)
    suite = TestSuite.fromTestCase(TestSummaryTest)
    suite.run(result)
    suite = TestSuite.fromTestCase(TestResultTest)
    suite.run(result)
    suite = TestSuite.fromTestCase(TestSuiteTest)
    suite.run(result)
    print(summary.results(result))
    print(resumedSummary.results(result))
    

if __name__ == "__main__":
    main()
