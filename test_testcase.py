from xunit import *


class TestCaseTest(TestCase):
    test: WasRun
    result: TestResult
    testNames = "testTemplateMethod testResult testFailedResult testFailedInSetUp testNotCompletedWhenNotFound testFailedResultCallsTearDown"
    
    def setUp(self) -> None:
        self.result = TestResult()

    def testTemplateMethod(self) -> None:
        self.test = WasRun("testMethod")
        self.test.run(self.result)
        assert self.test.log == "setUp testMethod tearDown"

    def testResult(self) -> None:
        test = WasRun("testMethod")
        test.run(self.result)
        assert 1 == self.result.passedCount
        assert 0 == self.result.failedCount
        assert 0 == self.result.notCompletedCount
        assert "testMethod" == self.result.getAllPassed()

    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert 1 == self.result.failedCount
        assert 0 == self.result.notCompletedCount
        assert "testBrokenMethod" == self.result.getAllFailed()

    def testFailedInSetUp(self) -> None:
        test = FailedSetUp("testMethod")
        test.run(self.result)
        assert "tearDown" in test.log
        assert self.result.failedCount == 0
        assert self.result.notCompletedCount == 1
        assert "testMethod" == self.result.getAllNotCompleted()

    def testNotCompletedWhenNotFound(self) -> None:
        test = WasRun("notImplementedTest")
        test.run(self.result)
        assert self.result.notCompletedCount == 1
        assert "notImplementedTest" == self.result.getAllNotCompleted()
        
    def testFailedResultCallsTearDown(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert "tearDown" in test.log
