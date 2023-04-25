from xunit.src import *
from xunit.src.status import TestStatus
from xunit.tests.testclasses import *


@TestClass
class TestResultTest(TestCase):
    result: TestResult
    
    def setup(self) -> None:
        self.result = TestResult()

    @Test
    def test_completed_tests(self) -> None:
        assert self.result.started == ""
        self.result.save_status(TestStatus("someTest", "Failed", ""))
        assert self.result.started == "someTest"
        assert self.result.failed == "someTest"

    @Test
    def test_completed_multiple_tests(self) -> None:
        self.result.save_status(TestStatus("someTest", "Failed", ""))
        self.result.save_status(TestStatus("someOtherTest", "Failed", ""))
        assert self.result.failed == "someTest someOtherTest"

    @Test
    def test_not_completed_tests(self) -> None:
        assert self.result.not_completed == ""
        self.result.save_status(TestStatus("someBrokenTest", "Not completed", ""))
        assert self.result.not_completed == "someBrokenTest"
        assert self.result.failed == self.result.started == ""
        self.result.save_status(TestStatus("someOtherBrokenTest", "Not completed", ""))
        assert self.result.not_completed == "someBrokenTest someOtherBrokenTest"

    @Test
    def test_passed_tests(self) -> None:
        assert self.result.passed == ""
        self.result.save_status(TestStatus("someTest", "Passed", ""))
        self.result.save_status(TestStatus("someOtherTest", "Passed", ""))
        assert self.result.passed == "someTest someOtherTest"

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
        assert self.result.started == 'testMethod testBrokenMethod'

    @Test
    def test_failed_errors(self) -> None:
        assert self.result.failed_errors == []
        error_info = TestStatus("", "Failed", "")
        self.result.save_status(error_info)
        assert self.result.failed_errors == [error_info]

    @Test
    def test_not_completed_errors(self) -> None:
        assert self.result.not_completed_errors == []
        error_info = TestStatus("", "Not completed", "")
        self.result.save_status(error_info)
        assert self.result.failed_errors == []
        assert self.result.not_completed_errors == [error_info]

    @Test
    def test_save_status(self) -> None:
        self.result.save_status(TestStatus("someTest", "Passed", "-"))
        self.result.save_status(TestStatus("someOtherTest", "Failed", "-"))
        self.result.save_status(TestStatus("brokenTest", "Not completed", "-"))
        assert self.result.passed == "someTest"
        assert self.result.failed == "someOtherTest"
        assert self.result.not_completed == "brokenTest"
        
        














