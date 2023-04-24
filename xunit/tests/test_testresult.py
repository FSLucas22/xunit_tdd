from xunit.src import *
from xunit.src.status import TestStatus
from xunit.src.testerrorinfo import TestErrorInfo
from xunit.tests.testclasses import *


@TestClass
class TestResultTest(TestCase):
    result: TestResult
    error_info: TestErrorInfo
    
    def setup(self) -> None:
        self.result = TestResult()
        self.error_info = TestErrorInfo("","", "")

    @Test
    def test_completed_tests(self) -> None:
        assert self.result.started == ""
        self.result._test_failed(TestErrorInfo("someTest", "", ""))
        assert self.result.started == "someTest"
        assert self.result.failed == "someTest"

    @Test
    def test_completed_multiple_tests(self) -> None:
        self.result._test_failed(TestErrorInfo("someTest", "", ""))
        self.result._test_failed(TestErrorInfo("someOtherTest", "", ""))
        assert self.result.failed == "someTest someOtherTest"

    @Test
    def test_not_completed_tests(self) -> None:
        assert self.result.not_completed == ""
        self.result._test_not_completed(TestErrorInfo("someBrokenTest", "", ""))
        assert self.result.not_completed == "someBrokenTest"
        assert self.result.failed == self.result.started == ""
        self.result._test_not_completed(TestErrorInfo("someOtherBrokenTest", "", ""))
        assert self.result.not_completed == "someBrokenTest someOtherBrokenTest"

    @Test
    def test_passed_tests(self) -> None:
        assert self.result.passed == ""
        self.result._test_passed("someTest")
        self.result._test_passed("someOtherTest")
        assert self.result.passed == "someTest someOtherTest"

    @Test
    def test_runned_equals_passed_plus_failed(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.add(FailedSetUp("testMethod"))
        suite.run(self.result)
        
        assert self.result.passed_count == 1
        assert self.result.failed_count == 1
        assert self.result.run_count == self.result.passed_count + self.result.failed_count
        assert self.result.started == 'testMethod testBrokenMethod'

    @Test
    def test_failed_errors(self) -> None:
        assert self.result._failed_errors == []
        self.result._test_failed(self.error_info)
        assert self.result._failed_errors == [self.error_info]

    @Test
    def test_not_completed_errors(self) -> None:
        assert self.result._not_completed_errors == []
        self.result._test_not_completed(self.error_info)
        assert self.result._failed_errors == []
        assert self.result._not_completed_errors == [self.error_info]

    @Test
    def test_save_status(self) -> None:
        self.result.save_status(TestStatus("someTest", "Passed", "-"))
        self.result.save_status(TestStatus("someOtherTest", "Failed", "-"))
        self.result.save_status(TestStatus("brokenTest", "Not completed", "-"))
        assert self.result.passed == "someTest"
        assert self.result.failed == "someOtherTest"
        assert self.result.not_completed == "brokenTest"
        
        














