from xunit.src import *
from xunit.src.testerrorinfo import TestErrorInfo
from xunit.tests.testclasses import *
import colorama


@TestClass
class TestSummaryTest(TestCase):
    result: TestResult
    error_info: TestErrorInfo
    
    def setup(self) -> None:
        self.result = TestResult()
        self.error_info = TestErrorInfo("", "", "")

    @Test
    def test_summary(self) -> None:
        summary = SimpleTestSummary()
        self.result._test_passed("someTest")
        self.result._test_not_completed(self.error_info)
        assert summary.results(self.result) == "1 run, 0 failed, 1 not completed"

    @Test
    def test_detailed_summary(self) -> None:
        identity = lambda messege: messege
        summary = DetailedTestSummary(
            passed_formatter=identity, failed_formatter=identity, not_completed_formatter=identity)
        self.result._test_passed("someOtherTest")
        self.result._test_failed(TestErrorInfo("someTest", "", ""))
        self.result._test_not_completed(TestErrorInfo("someBrokenTest", "", ""))
        assert summary.results(self.result) == "someTest - Failed\nsomeOtherTest - Passed\nsomeBrokenTest - Not completed"

    @Test
    def test_mixed_summary(self) -> None:
        summariesToMix: list[TestSummary] = [
            DetailedTestSummary(), SimpleTestSummary()
        ]
        summary = MixedTestSummary(*summariesToMix)
        self.result._test_passed("someTest")
        self.result._test_not_completed(self.error_info)
        summary_result = summary.results(self.result)
        individual_results = [s.results(self.result) for s in summariesToMix]
        assert summary_result == '\n'.join(individual_results)

    @Test
    def test_error_info_summary_for_failed_test(self) -> None:
        identity = lambda messege: messege
        summary = ErrorInfoSummary(
            passed_formatter=identity, failed_formatter=identity, not_completed_formatter=identity)
        test = MockTestCase("testMethod", Exception())
        test2 = MockTestCase("testMethod2", Exception())
        test.run(self.result)
        test2.run(self.result)
        error_info = self.result._failed_errors
        assert summary.results(self.result) == f"testMethod - Failed\n{error_info[0].info}\ntestMethod2 - Failed\n{error_info[1].info}"

    @Test
    def test_error_info_summary_for_not_completed_test(self) -> None:
        identity = lambda messege: messege
        summary = ErrorInfoSummary(
            passed_formatter=identity, failed_formatter=identity, not_completed_formatter=identity)
        test = MockTestCase("testMethod2", Exception())
        test2 = MockBrokenTestCase("testMethod", Exception())
        test.run(self.result)
        test2.run(self.result)
        failed_info = self.result._failed_errors[0]
        not_completed_info = self.result._not_completed_errors[0]
        assert summary.results(self.result) == f"testMethod2 - Failed\n{failed_info.info}\n"\
                                               f"testMethod - Not completed\n{not_completed_info.info}"

    @Test
    def test_format_messeges(self) -> None:
        failed_formatter = lambda messege: "{F}" + messege
        passed_formatter = lambda messege: "{P}" + messege
        not_completed_formatter = lambda messege: "{NC}" + messege
        summary = DetailedTestSummary(passed_formatter=passed_formatter, failed_formatter=failed_formatter, not_completed_formatter=not_completed_formatter)
        self.result._test_passed("passedTest")
        self.result._test_failed(TestErrorInfo("failedTest", "", ""))
        self.result._test_not_completed(TestErrorInfo("not_completedTest", "", ""))
        assert summary.results(self.result) == "{F}failedTest - Failed\n{P}passedTest - Passed\n{NC}not_completedTest - Not completed"

    @Test
    def test_error_info_summary_formatter(self) -> None:
        failed_formatter = lambda messege: "[F]" + messege
        not_completed_formatter = lambda messege: "[NC]" + messege
        summary = ErrorInfoSummary(failed_formatter=failed_formatter, not_completed_formatter=not_completed_formatter)
        test = MockTestCase("testMethod2", Exception())
        test2 = MockBrokenTestCase("testMethod", Exception())
        test.run(self.result)
        test2.run(self.result)
        failed_info = self.result._failed_errors[0]
        not_completed_info = self.result._not_completed_errors[0]
        assert summary.results(self.result) == f"[F]testMethod2 - Failed\n{failed_info.info}\n"\
                                               f"[NC]testMethod - Not completed\n{not_completed_info.info}"
