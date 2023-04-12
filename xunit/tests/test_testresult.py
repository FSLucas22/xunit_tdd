from xunit.src import *
from xunit.tests.testclasses import *


@TestClass
class TestResultTest(TestCase):
    result: TestResult
    
    def setUp(self) -> None:
        self.result = TestResult()

    @Test
    def testCompletedTests(self) -> None:
        assert self.result.getAllStarted() == ""
        self.result.testFailed("someTest")
        assert self.result.getAllStarted() == "someTest"
        assert self.result.getAllFailed() == "someTest"

    @Test
    def testCompletedMultipleTests(self) -> None:
        self.result.testFailed("someTest")
        self.result.testFailed("someOtherTest")
        assert self.result.getAllFailed() == "someTest someOtherTest"

    @Test
    def testNotCompletedTests(self) -> None:
        assert self.result.getAllNotCompleted() == ""
        self.result.testNotCompleted("someBrokenTest")
        assert self.result.getAllNotCompleted() == "someBrokenTest"
        assert self.result.getAllFailed() == self.result.getAllStarted() == ""
        self.result.testNotCompleted("someOtherBrokenTest")
        assert self.result.getAllNotCompleted() == "someBrokenTest someOtherBrokenTest"

    @Test
    def testPassedTests(self) -> None:
        assert self.result.getAllPassed() == ""
        self.result.testPassed("someTest")
        self.result.testPassed("someOtherTest")
        assert self.result.getAllPassed() == "someTest someOtherTest"

    @Test
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
