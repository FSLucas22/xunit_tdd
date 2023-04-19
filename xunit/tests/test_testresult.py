from xunit.src import *
from xunit.src.testerrorinfo import TestErrorInfo
from xunit.tests.testclasses import *


@TestClass
class TestResultTest(TestCase):
    result: TestResult
    error_info: TestErrorInfo
    
    def setUp(self) -> None:
        self.result = TestResult()
        self.error_info = TestErrorInfo(Exception(), 1, "", "")

    @Test
    def testCompletedTests(self) -> None:
        assert self.result.started == ""
        self.result._test_failed("someTest",
                                 TestErrorInfo(Exception(), 1, "", "someTest"))
        assert self.result.started == "someTest"
        assert self.result.failed == "someTest"

    @Test
    def testCompletedMultipleTests(self) -> None:
        self.result._test_failed("someTest",
                                 TestErrorInfo(Exception(), 1, "", "someTest"))
        self.result._test_failed("someOtherTest",
                                 TestErrorInfo(Exception(), 1, "", "someOtherTest"))
        assert self.result.failed == "someTest someOtherTest"

    @Test
    def testNotCompletedTests(self) -> None:
        assert self.result.not_completed == ""
        self.result._test_not_completed("someBrokenTest",
                                        TestErrorInfo(Exception(), 1, "", "someBrokenTest"))
        assert self.result.not_completed == "someBrokenTest"
        assert self.result.failed == self.result.started == ""
        self.result._test_not_completed("someOtherBrokenTest",
                                        TestErrorInfo(Exception(), 1, "", "someOtherBrokenTest"))
        assert self.result.not_completed == "someBrokenTest someOtherBrokenTest"

    @Test
    def testPassedTests(self) -> None:
        assert self.result.passed == ""
        self.result._test_passed("someTest")
        self.result._test_passed("someOtherTest")
        assert self.result.passed == "someTest someOtherTest"

    @Test
    def testRunnedEqualsPassedPlusFailed(self) -> None:
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
    def testFailedErrors(self) -> None:
        assert self.result._failed_errors == []
        self.result._test_failed("someTest", self.error_info)
        assert self.result._failed_errors == [self.error_info]

    @Test
    def testNotCompletedErrors(self) -> None:
        assert self.result._not_completed_errors == []
        self.result._test_not_completed("someTest", self.error_info)
        assert self.result._failed_errors == []
        assert self.result._not_completed_errors == [self.error_info]














