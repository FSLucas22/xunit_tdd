from xunit.src import *
from xunit.src.status import TestStatus, Status
from xunit.tests.testclasses import *


@TestClass
class TestResultTest(TestCase):
    result: TestResult
    
    def setup(self) -> None:
        self.result = TestResult()

    @Test
    def test_completed_tests(self) -> None:
        self.result.save_status(TestStatus("someTest", Status.FAILED, ""))
        assert self.result.get_names_of_status(Status.FAILED) == "someTest"

    @Test
    def test_completed_multiple_tests(self) -> None:
        self.result.save_status(TestStatus("someTest", Status.FAILED, ""))
        self.result.save_status(TestStatus("someOtherTest", Status.FAILED, ""))
        assert self.result.get_names_of_status(Status.FAILED) == "someTest someOtherTest"

    @Test
    def test_not_completed_tests(self) -> None:
        assert self.result.not_completed == ""
        self.result.save_status(TestStatus("someBrokenTest", Status.NOT_COMPLETED, ""))
        assert self.result.not_completed == "someBrokenTest"
        self.result.save_status(TestStatus("someOtherBrokenTest", Status.NOT_COMPLETED, ""))
        assert self.result.not_completed == "someBrokenTest someOtherBrokenTest"

    @Test
    def test_passed_tests(self) -> None:
        assert self.result.get_names_of_status(Status.PASSED) == ""
        self.result.save_status(TestStatus("someTest", Status.PASSED, ""))
        self.result.save_status(TestStatus("someOtherTest", Status.PASSED, ""))
        assert self.result.get_names_of_status(Status.PASSED) == "someTest someOtherTest"

    @Test
    def test_runned_equals_passed_plus_failed(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.add(FailedSetUp("testMethod"))
        suite.register(self.result.save_status)
        suite.run()
        
        assert self.result.passed_count == 1
        assert self.result.failed_count == 1
        assert self.result.run_count == self.result.passed_count + self.result.failed_count

    @Test
    def test_failed_errors(self) -> None:
        assert self.result.failed_errors == []
        error_info = TestStatus("", Status.FAILED, "")
        self.result.save_status(error_info)
        assert self.result.failed_errors == [error_info]

    @Test
    def test_not_completed_errors(self) -> None:
        assert self.result.not_completed_errors == []
        error_info = TestStatus("", Status.NOT_COMPLETED, "")
        self.result.save_status(error_info)
        assert self.result.failed_errors == []
        assert self.result.not_completed_errors == [error_info]

    @Test
    def test_save_status(self) -> None:
        self.result.save_status(TestStatus("someTest", Status.PASSED, "-"))
        self.result.save_status(TestStatus("someOtherTest", Status.FAILED, "-"))
        self.result.save_status(TestStatus("brokenTest", Status.NOT_COMPLETED, "-"))
        assert self.result.get_names_of_status(Status.PASSED) == "someTest"
        assert self.result.get_names_of_status(Status.FAILED) == "someOtherTest"
        assert self.result.not_completed == "brokenTest"
        
        














