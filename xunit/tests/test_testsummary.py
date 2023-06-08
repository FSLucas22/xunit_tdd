from xunit.src import *
from xunit.tests.testclasses import *
from xunit.src.status import TestStatus, Status


@TestClass
class TestSummaryTest(TestCase):
    result: TestResult
    error_info: TestStatus

    def setup(self) -> None:
        self.result = TestResult()
        self.error_info = TestStatus("", Status.PASSED, "")

    @Test
    def test_summary(self) -> None:
        summary = SimpleTestSummary()
        self.result.save_status(TestStatus("someTest", Status.PASSED, ""))
        self.result.save_status(TestStatus("", Status.NOT_COMPLETED, ""))
        assert summary.results(self.result) == "1 run, 0 failed, 1 not completed"

    @Test
    def test_detailed_summary(self) -> None:
        summary = DetailedTestSummary(BASIC_UNCOLORED_FORMATTERS)
        self.result.save_status(TestStatus("someOtherTest", Status.PASSED, ""))
        self.result.save_status(TestStatus("someTest", Status.FAILED, ""))
        self.result.save_status(TestStatus("someBrokenTest", Status.NOT_COMPLETED, ""))
        assert summary.results(self.result
                               ) == "someTest - Failed\nsomeOtherTest - Passed\nsomeBrokenTest - Not completed"

    @Test
    def test_mixed_summary(self) -> None:
        summariesToMix: list[TestSummary] = [
            DetailedTestSummary(), SimpleTestSummary()
        ]
        summary = MixedTestSummary(*summariesToMix)
        self.result.save_status(TestStatus("someTest", Status.PASSED, ""))
        self.result.save_status(TestStatus("", Status.NOT_COMPLETED, ""))
        summary_result = summary.results(self.result)
        individual_results = [s.results(self.result) for s in summariesToMix]
        assert summary_result == '\n'.join(individual_results)

    @Test
    def test_error_info_summary_for_failed_test(self) -> None:
        summary = ErrorInfoSummary(UNCOLORED_FORMATTERS)
        test = MockTestCase("testMethod", Exception())
        test2 = MockTestCase("testMethod2", Exception())
        test.register(self.result.save_status)
        test2.register(self.result.save_status)
        test.run()
        test2.run()
        error_info = self.result.get_results_of_status(Status.FAILED)
        assert summary.results(self.result) == f"testMethod - Failed\n{error_info[0].info}\ntestMethod2 - Failed\n{error_info[1].info}"

    @Test
    def test_error_info_summary_for_not_completed_test(self) -> None:
        summary = ErrorInfoSummary(UNCOLORED_FORMATTERS)
        test = MockTestCase("testMethod2", Exception())
        test2 = MockBrokenTestCase("testMethod", Exception())
        test.register(self.result.save_status)
        test2.register(self.result.save_status)
        test.run()
        test2.run()
        failed_info = self.result.get_results_of_status(Status.FAILED)[0]
        not_completed_info = self.result.get_results_of_status(Status.NOT_COMPLETED)[0]
        assert summary.results(self.result) == f"testMethod2 - Failed\n{failed_info.info}\n"\
                                               f"testMethod - Not completed\n{not_completed_info.info}"

    @Test
    def test_format_messeges(self) -> None:
        formatters = {
            Status.PASSED: lambda status: "{P}" + basic_msg_formatter(status),
            Status.FAILED: lambda status: "{F}" + basic_msg_formatter(status),
            Status.NOT_COMPLETED: lambda status: "{NC}" + basic_msg_formatter(status)
        }
        summary = DetailedTestSummary(TestStatusFormatter(formatters))
        self.result.save_status(TestStatus("passedTest", Status.PASSED, ""))
        self.result.save_status(TestStatus("failedTest", Status.FAILED, ""))
        self.result.save_status(TestStatus("not_completedTest", Status.NOT_COMPLETED, ""))
        assert summary.results(self.result) == "{F}failedTest - Failed\n{P}passedTest - Passed\n{NC}not_completedTest - Not completed"

    @Test
    def test_error_info_summary_formatter(self) -> None:
        formatters = {
            Status.FAILED: lambda status: "[F]" + error_msg_formatter(status),
            Status.NOT_COMPLETED: lambda status: "[NC]" + error_msg_formatter(status)
        }
        summary = ErrorInfoSummary(TestStatusFormatter(formatters))

        test = MockTestCase("testMethod2", Exception())
        test2 = MockBrokenTestCase("testMethod", Exception())
        test.register(self.result.save_status)
        test2.register(self.result.save_status)
        test.run()
        test2.run()
        failed_info = self.result.get_results_of_status(Status.FAILED)[0]
        not_completed_info = self.result.get_results_of_status(Status.NOT_COMPLETED)[0]
        assert summary.results(self.result) == f"[F]testMethod2 - Failed\n{failed_info.info}\n"\
                                               f"[NC]testMethod - Not completed\n{not_completed_info.info}"
    
    @Test
    def test_status_summary(self) -> None:
        self.result.save_status(TestStatus("Suite", Status.CREATED, "someSuite"))
        self.result.save_status(TestStatus("Some test", Status.FAILED_TO_RUN, "info"))
        summary: Summary = StatusSummary()
        assert summary.results(self.result) == f"Suite - Created: someSuite\nSome test - Failed to run: info"
