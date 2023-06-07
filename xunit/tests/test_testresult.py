from xunit.src import *
from xunit.src.status import TestStatus, Status
from xunit.tests.testclasses import *


@TestClass
class TestResultTest(TestCase):
    result: TestResult
    
    def setup(self) -> None:
        self.result = TestResult()

    @Test
    def test_should_get_results_of_given_status(self) -> None:
        failed_test = TestStatus("passedTest", Status.FAILED, "")
        self.result.save_status(TestStatus("passedTest", Status.PASSED, ""))
        self.result.save_status(failed_test)

        assert [failed_test] == self.result.get_results_of_status(Status.FAILED)

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
        assert self.result.get_names_of_status(Status.NOT_COMPLETED) == ""
        self.result.save_status(TestStatus("someBrokenTest", Status.NOT_COMPLETED, ""))
        assert self.result.get_names_of_status(Status.NOT_COMPLETED) == "someBrokenTest"
        self.result.save_status(TestStatus("someOtherBrokenTest", Status.NOT_COMPLETED, ""))
        assert self.result.get_names_of_status(Status.NOT_COMPLETED) == "someBrokenTest someOtherBrokenTest"

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
        
        assert self.result.get_status_count(Status.PASSED) == 1
        assert self.result.get_status_count(Status.FAILED) == 1

    @Test
    def test_failed_errors(self) -> None:
        assert self.result.get_results_of_status(Status.FAILED) == []
        error_info = TestStatus("", Status.FAILED, "")
        self.result.save_status(error_info)
        assert self.result.get_results_of_status(Status.FAILED) == [error_info]

    @Test
    def test_not_completed_errors(self) -> None:
        assert self.result.get_results_of_status(Status.NOT_COMPLETED) == []
        error_info = TestStatus("", Status.NOT_COMPLETED, "")
        self.result.save_status(error_info)
        assert self.result.get_results_of_status(Status.FAILED) == []
        assert self.result.get_results_of_status(Status.NOT_COMPLETED) == [error_info]

    @Test
    def test_save_status(self) -> None:
        self.result.save_status(TestStatus("someTest", Status.PASSED, "-"))
        self.result.save_status(TestStatus("someOtherTest", Status.FAILED, "-"))
        self.result.save_status(TestStatus("brokenTest", Status.NOT_COMPLETED, "-"))
        assert self.result.get_names_of_status(Status.PASSED) == "someTest"
        assert self.result.get_names_of_status(Status.FAILED) == "someOtherTest"
        assert self.result.get_names_of_status(Status.NOT_COMPLETED) == "brokenTest"
        
        














