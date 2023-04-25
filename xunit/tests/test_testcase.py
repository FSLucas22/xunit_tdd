from xunit.src import *
from xunit.src.status import TestStatus
from xunit.src.observer import Observer, Subject
from xunit.tests.testclasses import *
from typing import cast


@TestClass
class TestCaseTest(TestCase):
    test: WasRun
    result: TestResult
    
    def setup(self) -> None:
        self.result = TestResult()
        self.test = WasRun("testMethod")
        self.test.register(self.result.save_status)

    @Test
    def test_template_method(self) -> None:
        self.test.run()
        assert self.test.log == "setup testMethod teardown"

    @Test
    def test_result(self) -> None:
        self.test.run()
        assert 1 == self.result.passed_count
        assert 0 == self.result.failed_count
        assert 0 == self.result.not_completed_count
        assert "testMethod" == self.result.passed

    @Test
    def test_failed_result(self) -> None:
        test = WasRun("testBrokenMethod")
        test.register(self.result.save_status)
        test.run()
        assert 1 == self.result.failed_count
        assert 0 == self.result.not_completed_count
        assert "testBrokenMethod" == self.result.failed

    @Test
    def test_failed_in_set_up(self) -> None:
        test = FailedSetUp("testMethod")
        test.register(self.result.save_status)
        test.run()
        assert "teardown" in test.log
        assert self.result.failed_count == 0
        assert self.result.not_completed_count == 1
        assert "testMethod" == self.result.not_completed

    @Test
    def test_not_completed_when_not_found(self) -> None:
        test = WasRun("notImplementedTest")
        test.register(self.result.save_status)
        test.run()
        assert self.result.not_completed_count == 1
        assert "notImplementedTest" == self.result.not_completed

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
            error, "testMethod", "Failed"
        )
        error_info = self.result._failed_errors[0]
        assert expected_info == error_info

    @Test
    def test_not_completed_result_passes_exception(self) -> None:
        error = Exception()
        mock_class = MockBrokenTestCase("testMethod", error)
        mock_class.register(self.result.save_status)
        mock_class.run()
        assert mock_class.exception_raised == error
        expected_info = TestStatus.from_exception(
            error, "testMethod", "Not completed"
        )
        error_info = self.result._not_completed_errors[0]
        assert error_info == expected_info

    @Test
    def test_observer(self) -> None:
        observer: Observer = DummyObserver()
        status = TestStatus("x", "y", "z")
        observer(status)
        observer = cast(DummyObserver, observer)
        assert observer.received == [status]
        observer(status)
        assert observer.received == [status, status]
        
    @Test
    def test_testcase_is_subject(self) -> None:
        subject: Subject = DummyTestCase("passedTest1") 
        observer1 = DummyObserver()
        observer2 = DummyObserver()
        status = TestStatus("x", "y", "z")
        subject.register(observer1, observer2)
        subject.notify(status)
        assert observer1.received == observer2.received == [status]
        subject.unregister(observer1)
        subject.notify(status)
        assert observer1.received == [status]
        assert observer2.received == [status, status]

