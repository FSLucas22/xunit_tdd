from xunit import *


class TestResultTest(TestCase):
    result: TestResult
    testNames = "testCompletedTests testCompletedMultipleTests testNotCompletedTests "\
                "testPassedTests testRunnedEqualsPassedPlusFailed"
    
    def setUp(self) -> None:
        self.result = TestResult()

    def testCompletedTests(self) -> None:
        assert self.result.getAllStarted() == ""
        self.result.testFailed("someTest")
        assert self.result.getAllStarted() == "someTest"
        assert self.result.getAllFailed() == "someTest"

    def testCompletedMultipleTests(self) -> None:
        self.result.testFailed("someTest")
        self.result.testFailed("someOtherTest")
        assert self.result.getAllFailed() == "someTest someOtherTest"

    def testNotCompletedTests(self) -> None:
        assert self.result.getAllNotCompleted() == ""
        self.result.testNotCompleted("someBrokenTest")
        assert self.result.getAllNotCompleted() == "someBrokenTest"
        assert self.result.getAllFailed() == self.result.getAllStarted() == ""
        self.result.testNotCompleted("someOtherBrokenTest")
        assert self.result.getAllNotCompleted() == "someBrokenTest someOtherBrokenTest"

    def testPassedTests(self) -> None:
        assert self.result.getAllPassed() == ""
        self.result.testPassed("someTest")
        self.result.testPassed("someOtherTest")
        assert self.result.getAllPassed() == "someTest someOtherTest"

    def testRunnedEqualsPassedPlusFailed(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.add(FailedSetUp("testMethod"))
        suite.run(self.result)
        assert self.result.passedCount == 1
        assert self.result.failedCount == 1
        assert self.result.runCount == self.result.passedCount + self.result.failedCount
        assert self.result.getAllStarted() == 'testMethod testBrokenMethod'
