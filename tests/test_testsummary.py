from src.xunit import *
from .testclasses import *
from src.xunit.status import TestStatus, Status


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
    def test_mixed_summary(self) -> None:
        basic_summary = TestSummary(
            BASIC_UNCOLORED_FORMATTERS, Status.FAILED, Status.PASSED, Status.NOT_COMPLETED)
        summariesToMix: list[Summary] = [
            basic_summary, SimpleTestSummary()
        ]
        summary = MixedTestSummary(*summariesToMix)
        self.result.save_status(TestStatus("someTest", Status.PASSED, ""))
        self.result.save_status(TestStatus("", Status.NOT_COMPLETED, ""))
        summary_result = summary.results(self.result)
        individual_results = [s.results(self.result) for s in summariesToMix]
        assert summary_result == '\n'.join(individual_results)

    @Test
    def test_format_messeges(self) -> None:
        formatters = {
            Status.PASSED: lambda status: "{P}" + basic_msg_formatter(status),
            Status.FAILED: lambda status: "{F}" + basic_msg_formatter(status),
            Status.NOT_COMPLETED: lambda status: "{NC}" + basic_msg_formatter(status)
        }
        summary = TestSummary(TestStatusFormatter(formatters), 
                                      Status.FAILED, Status.PASSED, Status.NOT_COMPLETED)
        
        self.result.save_status(TestStatus("passedTest", Status.PASSED, ""))
        self.result.save_status(TestStatus("failedTest", Status.FAILED, ""))
        self.result.save_status(TestStatus("not_completedTest", Status.NOT_COMPLETED, ""))

        assert summary.results(self.result
                ) == "{F}failedTest - Failed\n{P}passedTest - Passed\n{NC}not_completedTest - Not completed"
