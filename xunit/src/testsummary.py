from typing import Protocol, Callable
from xunit.src.testresult import TestResult
from xunit.src.status import Status, TestStatus
import xunit.src.testcolours as color
from collections.abc import Mapping


class TestSummary(Protocol):
    def results(self, result: TestResult) -> str:
        ...


formatter = Callable[[str], str]
test_status_formatter = Callable[[TestStatus], str]


basic_msg_formatter: test_status_formatter = lambda status: f'{status.name} - {status.result}'
error_msg_formatter: test_status_formatter = lambda status: f'{status.name} - {status.result}\n{status.info}'
detailed_msg_formatter: test_status_formatter = lambda status: f'{status.name} - {status.result}: {status.info}'


UNCOLORED_FORMATTERS = {
    Status.PASSED: basic_msg_formatter,
    Status.FAILED: error_msg_formatter,
    Status.NOT_COMPLETED: error_msg_formatter
}

FORMATTERS: Mapping[Status, test_status_formatter] = {
    Status.PASSED: lambda msg: color.green(basic_msg_formatter(msg)),
    Status.FAILED: lambda msg: color.red(error_msg_formatter(msg)),
    Status.NOT_COMPLETED: lambda msg: color.yellow(error_msg_formatter(msg))
}

class TestStatusFormatter:
    def __init__(self, messege_formatters: Mapping[Status, test_status_formatter]) -> None:
        self.messege_formatters = messege_formatters

    def __call__(self, test_status: TestStatus) -> str:
        messege_formatter = self.messege_formatters.get(test_status.result, detailed_msg_formatter)
        return messege_formatter(test_status)


class Summary:
    def __init__(self, messege_formatters: Mapping[Status, test_status_formatter] = FORMATTERS,
                *order_filter: Status):
        self.messege_formatters = messege_formatters
        self.order_filter = order_filter
        self.test_status_formatter = TestStatusFormatter(messege_formatters)

    def results(self, result: TestResult) -> str:
        
        status_list: list[str] = []
        
        for status in result.get_results_of_status(*self.order_filter):
            messege = self.test_status_formatter(status)
            status_list.append(messege)

        return "\n".join(status_list)
    
    
class SimpleTestSummary:
    def results(self, result: TestResult) -> str:
        failed_count = result.get_status_count(Status.FAILED)
        run_count = result.get_status_count(Status.PASSED) + failed_count
        not_completed_count = result.get_status_count(Status.NOT_COMPLETED)
        return f"{run_count} run, {failed_count} failed, {not_completed_count} not completed"


class DetailedTestSummary:
    def __init__(self, messege_formatters: Mapping[Status, test_status_formatter] = {
                     Status.PASSED: basic_msg_formatter,
                     Status.FAILED: basic_msg_formatter,
                     Status.NOT_COMPLETED: basic_msg_formatter
                 }):
        self.messege_formatters = messege_formatters
    
    def results(self, result: TestResult) -> str:
        summary = [
            Summary(self.messege_formatters, Status.FAILED).results(result),
            Summary(self.messege_formatters, Status.PASSED).results(result),
            Summary(self.messege_formatters, Status.NOT_COMPLETED).results(result)
        ]
        return '\n'.join(summary)


class MixedTestSummary:
    def __init__(self, *summaries: TestSummary):
        self.summaries = summaries
        
    def results(self, result: TestResult) -> str:
        summary_results = []
        for summary in self.summaries:
            summary_results.append(summary.results(result))
        return '\n'.join(summary_results)


class ErrorInfoSummary(Summary):
    def __init__(self, messege_formatters: Mapping[Status, test_status_formatter] = FORMATTERS) -> None:
        super().__init__(messege_formatters, Status.FAILED, Status.NOT_COMPLETED)

    
class StatusSummary(Summary):
    pass
