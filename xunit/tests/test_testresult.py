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
        failed_test = TestStatus("failedTest", Status.FAILED, "")
        self.result.save_status(TestStatus("passedTest", Status.PASSED, ""))
        self.result.save_status(failed_test)

        assert [failed_test] == self.result.get_results_of_status(Status.FAILED)

    @Test
    def test_should_get_names_of_given_status(self) -> None:
        failed_test = TestStatus("failedTest", Status.FAILED, "")
        self.result.save_status(TestStatus("passedTest", Status.PASSED, ""))
        self.result.save_status(failed_test)

        assert "failedTest" == self.result.get_names_of_status(Status.FAILED)

    @Test
    def test_completed_multiple_tests(self) -> None:
        self.result.save_status(TestStatus("someTest", Status.FAILED, ""))
        self.result.save_status(TestStatus("someOtherTest", Status.FAILED, ""))
        assert self.result.get_names_of_status(Status.FAILED) == "someTest someOtherTest"

    @Test
    def test_save_status(self) -> None:
        self.result.save_status(TestStatus("someTest", Status.PASSED, "-"))
        self.result.save_status(TestStatus("someOtherTest", Status.FAILED, "-"))
        self.result.save_status(TestStatus("brokenTest", Status.NOT_COMPLETED, "-"))
        assert self.result.get_names_of_status(Status.PASSED) == "someTest"
        assert self.result.get_names_of_status(Status.FAILED) == "someOtherTest"
        assert self.result.get_names_of_status(Status.NOT_COMPLETED) == "brokenTest"
