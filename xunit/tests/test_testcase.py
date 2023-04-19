from xunit.src import *
from xunit.src.testerrorinfo import TestErrorInfo
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
        assert 1 == self.result.passed_count
        assert 0 == self.result.failed_count
        assert 0 == self.result.not_completed_count
        assert "testMethod" == self.result.passed

    @Test
    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert 1 == self.result.failed_count
        assert 0 == self.result.not_completed_count
        assert "testBrokenMethod" == self.result.failed

    @Test
    def testFailedInSetUp(self) -> None:
        test = FailedSetUp("testMethod")
        test.run(self.result)
        assert "tearDown" in test.log
        assert self.result.failed_count == 0
        assert self.result.not_completed_count == 1
        assert "testMethod" == self.result.not_completed

    @Test
    def testNotCompletedWhenNotFound(self) -> None:
        test = WasRun("notImplementedTest")
        test.run(self.result)
        assert self.result.not_completed_count == 1
        assert "notImplementedTest" == self.result.not_completed

    @Test 
    def testFailedResultCallsTearDown(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert "tearDown" in test.log

    @Test
    def testFailedResultPassesException(self) -> None:
        error = Exception()

        mock_class = MockTestCase("testMethod", error)
        mock_class.run(self.result)
        assert mock_class.exception_raised == error
        expected_info = TestErrorInfo.from_exception(
            error, test_name="testMethod"
        )
        error_info = self.result._failed_errors[0]
        assert expected_info == error_info

    @Test
    def testnotCompletedResultPassesException(self) -> None:
        error = Exception()
        mock_class = MockBrokenTestCase("testMethod", error)
        mock_class.run(self.result)
        assert mock_class.exception_raised == error
        expected_info = TestErrorInfo.from_exception(
            error, test_name="testMethod"
        )
        error_info = self.result._not_completed_errors[0]
        assert error_info == expected_info
