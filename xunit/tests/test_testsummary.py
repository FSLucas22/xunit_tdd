from xunit.src import *
from xunit.tests.testclasses import *


@TestClass
class TestSummaryTest(TestCase):
    result: TestResult
    error_info: TestErrorInfo
    
    def setUp(self) -> None:
        self.result = TestResult()
        self.error_info = TestErrorInfo(Exception(), 1, "", "")

    @Test
    def testSummary(self) -> None:
        summary = SimpleTestSummary()
        self.result.testPassed("someTest")
        self.result.testNotCompleted("someTest", self.error_info)
        assert summary.results(self.result) == "1 run, 0 failed, 1 not completed"

    @Test
    def testDetailedSummary(self) -> None:
        summary = DetailedTestSummary()
        self.result.testPassed("someOtherTest")
        self.result.testFailed("someTest", self.error_info)
        self.result.testNotCompleted("someBrokenTest", self.error_info)
        assert summary.results(self.result) == "someTest - Failed\nsomeOtherTest - Passed\nsomeBrokenTest - Not completed"

    @Test
    def testMixedSummary(self) -> None:
        summariesToMix: list[TestSummary] = [
            DetailedTestSummary(), SimpleTestSummary()
        ]
        summary = MixedTestSummary(*summariesToMix)
        self.result.testPassed("someTest")
        self.result.testNotCompleted("someTest", self.error_info)
        summary_result = summary.results(self.result)
        individual_results = [s.results(self.result) for s in summariesToMix]
        assert summary_result == '\n'.join(individual_results)

    @Test
    def testErrorInfoSummaryForFailedTest(self) -> None:
        summary = ErrorInfoSummary()
        test = MockTestCase("testMethod", Exception())
        test2 = MockTestCase("testMethod2", Exception())
        test.run(self.result)
        test2.run(self.result)
        error_info = self.result.failedErrors
        assert summary.results(self.result) == f"testMethod - Failed\n{error_info[0].error_info}\ntestMethod2 - Failed\n{error_info[1].error_info}"
        
