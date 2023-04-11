from xunit.src import *


class TestSummaryTest(TestCase):
    result: TestResult
    testNames = "testSummary testDetailedSummary testMixedSummary"

    def setUp(self) -> None:
        self.result = TestResult()

    def testSummary(self) -> None:
        summary = SimpleTestSummary()
        self.result.testPassed("someTest")
        self.result.testNotCompleted("someTest")
        assert summary.results(self.result) == "1 run, 0 failed, 1 not completed"

    def testDetailedSummary(self) -> None:
        summary = DetailedTestSummary()
        self.result.testPassed("someOtherTest")
        self.result.testFailed("someTest")
        self.result.testNotCompleted("someBrokenTest")
        assert summary.results(self.result) == "someTest - Failed\nsomeOtherTest - Passed\nsomeBrokenTest - Not completed"

    def testMixedSummary(self) -> None:
        summariesToMix: list[TestSummary] = [
            DetailedTestSummary(), SimpleTestSummary()
        ]
        summary = MixedTestSummary(*summariesToMix)
        self.result.testPassed("someTest")
        self.result.testNotCompleted("someTest")
        summary_result = summary.results(self.result)
        individual_results = [s.results(self.result) for s in summariesToMix]
        assert summary_result == '\n'.join(individual_results)
