from xunit.src import *
from xunit.tests.testclasses import WasRun, FailedSetUp


@TestClass
class TestCaseTest(TestCase):
    test: WasRun
    result: TestResult
    
    def setUp(self) -> None:
        self.result = TestResult()

    @Test
    def testTemplateMethod(self) -> None:
        self.test = WasRun("testMethod")
        self.test.run(self.result)
        assert self.test.log == "setUp testMethod tearDown"

    @Test
    def testResult(self) -> None:
        test = WasRun("testMethod")
        test.run(self.result)
        assert 1 == self.result.passedCount
        assert 0 == self.result.failedCount
        assert 0 == self.result.notCompletedCount
        assert "testMethod" == self.result.getAllPassed()

    @Test
    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert 1 == self.result.failedCount
        assert 0 == self.result.notCompletedCount
        assert "testBrokenMethod" == self.result.getAllFailed()

    @Test
    def testFailedInSetUp(self) -> None:
        test = FailedSetUp("testMethod")
        test.run(self.result)
        assert "tearDown" in test.log
        assert self.result.failedCount == 0
        assert self.result.notCompletedCount == 1
        assert "testMethod" == self.result.getAllNotCompleted()

    @Test
    def testNotCompletedWhenNotFound(self) -> None:
        test = WasRun("notImplementedTest")
        test.run(self.result)
        assert self.result.notCompletedCount == 1
        assert "notImplementedTest" == self.result.getAllNotCompleted()

    @Test 
    def testFailedResultCallsTearDown(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert "tearDown" in test.log
