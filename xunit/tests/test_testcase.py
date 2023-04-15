from xunit.src import *
from xunit.tests.testclasses import *
from typing import cast


@TestClass
class TestCaseTest(TestCase):
    test: WasRun
    result: TestResult
    
    def setUp(self) -> None:
        self.result = TestResult()
        self.test = WasRun("testMethod")

    @Test
    def testTemplateMethod(self) -> None:
        self.test.run(self.result)
        assert self.test.log == "setUp testMethod tearDown"

    @Test
    def testResult(self) -> None:
        self.test.run(self.result)
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

    @Test
    def testFailedResultPassesException(self) -> None:
        error = Exception()
        mock_info = MockTestErrorInfo(error)
        assert mock_info.exception_passed == error

        mock_class = MockTestCase("testMethod", error)
        mock_class.run(self.result, MockTestErrorInfo)
        assert mock_class.exception_raised == error
        
        error_info = cast(MockTestErrorInfo, self.result.failedErrors[0])
        assert error == error_info.exception_passed

    @Test
    def testnotCompletedResultPassesException(self) -> None:
        error = Exception()
        mock_class = MockBrokenTestCase("testMethod", error)
        mock_class.run(self.result, MockTestErrorInfo)
        assert mock_class.exception_raised == error

        error_info = cast(MockTestErrorInfo, self.result.notCompletedErrors[0])
        assert error == error_info.exception_passed
