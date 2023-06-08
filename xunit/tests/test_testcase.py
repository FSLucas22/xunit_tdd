from xunit.src import *
from xunit.src.status import TestStatus, Status
from xunit.src.observer import Observer, Subject
from xunit.tests.testclasses import *
from typing import cast


@TestClass
class TestCaseTest(TestCase):
    test: WasRun
    result: TestResult
    
    def setup(self) -> None:
        self.result = TestResult()
        self.test = WasRun("testMethod", self.result.save_status)

    @Test
    def test_template_method(self) -> None:
        self.test.run()
        assert self.test.log == "setup testMethod teardown"

    @Test
    def test_result(self) -> None:
        self.test.run()
        assert 1 == self.result.get_status_count(Status.PASSED)
        assert 0 == self.result.get_status_count(Status.FAILED)
        assert 0 == self.result.get_status_count(Status.NOT_COMPLETED)
        assert "testMethod" == self.result.get_names_of_status(Status.PASSED)

    @Test
    def test_failed_result(self) -> None:
        test = WasRun("testBrokenMethod", self.result.save_status)
        test.run()
        assert 1 == self.result.get_status_count(Status.FAILED)
        assert 0 == self.result.get_status_count(Status.NOT_COMPLETED)
        assert "testBrokenMethod" == self.result.get_names_of_status(Status.FAILED)

    @Test
    def test_failed_in_set_up(self) -> None:
        test = FailedSetUp("testMethod", self.result.save_status)
        test.run()
        assert "teardown" in test.log
        assert self.result.get_status_count(Status.FAILED) == 0
        assert self.result.get_status_count(Status.NOT_COMPLETED) == 1
        assert "testMethod" == self.result.get_names_of_status(Status.NOT_COMPLETED)

    @Test
    def test_not_completed_when_not_found(self) -> None:
        test = WasRun("notImplementedTest", self.result.save_status)
        test.run()
        assert self.result.get_status_count(Status.NOT_COMPLETED) == 1
        assert "notImplementedTest" == self.result.get_names_of_status(Status.NOT_COMPLETED)

    @Test 
    def test_failed_result_calls_tear_down(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run()
        assert "teardown" in test.log

    @Test
    def test_failed_result_passes_exception(self) -> None:
        error = Exception()
        mock_class = MockTestCase("testMethod", error)
        mock_class.register(self.result.save_status)
        mock_class.run()
        assert mock_class.exception_raised == error
        expected_info = TestStatus.from_exception(
            error, "testMethod", Status.FAILED
        )
        error_info = self.result.get_results(Status.FAILED)[0]
        assert expected_info == error_info

    @Test
    def test_not_completed_result_passes_exception(self) -> None:
        error = Exception()
        mock_class = MockBrokenTestCase("testMethod", error)
        mock_class.register(self.result.save_status)
        mock_class.run()
        assert mock_class.exception_raised == error
        expected_info = TestStatus.from_exception(
            error, "testMethod", Status.NOT_COMPLETED
        )
        error_info = self.result.get_results(Status.NOT_COMPLETED)[0]
        assert error_info == expected_info

