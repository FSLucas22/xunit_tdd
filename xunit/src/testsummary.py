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


COLOR_FORMATTERS = {
    Status.FAILED: color.red,
    Status.PASSED: color.green,
    Status.NOT_COMPLETED: color.yellow
}

FORMATTERS: Mapping[Status, test_status_formatter] = {
    Status.PASSED: basic_msg_formatter,
    Status.FAILED: error_msg_formatter,
    Status.NOT_COMPLETED: error_msg_formatter
}

class TestStatusFormatter:
    def __init__(self, color_formatters: Mapping[Status, formatter], 
                 messege_formatters: Mapping[Status, test_status_formatter]) -> None:
        self.color_formatters = color_formatters
        self.messege_formatters = messege_formatters

    def __call__(self, test_status: TestStatus) -> str:
        color_formatter = self.color_formatters.get(test_status.result, lambda x: x)
        messege_formatter = self.messege_formatters.get(test_status.result, detailed_msg_formatter)
        return color_formatter(messege_formatter(test_status))


class Summary:
    def __init__(self, color_formatters: Mapping[Status, formatter] = COLOR_FORMATTERS,
                 messege_formatters: Mapping[Status, test_status_formatter] = FORMATTERS,
                *order_filter: Status):
        self.color_formatters = color_formatters
        self.messege_formatters = messege_formatters
        self.order_filter = order_filter
        self.test_status_formatter = TestStatusFormatter(color_formatters, messege_formatters)

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
    def __init__(self, color_formatters: Mapping[Status, formatter] = COLOR_FORMATTERS,
                 messege_formatters: Mapping[Status, test_status_formatter] = {
                     Status.PASSED: basic_msg_formatter,
                     Status.FAILED: basic_msg_formatter,
                     Status.NOT_COMPLETED: basic_msg_formatter
                 }):
    
        self.color_formatters = color_formatters
        self.messege_formatters = messege_formatters
    
    def results(self, result: TestResult) -> str:
        summary = [
            Summary(self.color_formatters, self.messege_formatters, Status.FAILED).results(result),
            Summary(self.color_formatters, self.messege_formatters, Status.PASSED).results(result),
            Summary(self.color_formatters, self.messege_formatters, Status.NOT_COMPLETED).results(result)
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
    def __init__(self, color_formatters: Mapping[Status, formatter] = COLOR_FORMATTERS,
                 messege_formatters: Mapping[Status, test_status_formatter] = FORMATTERS) -> None:
        super().__init__(color_formatters, messege_formatters, Status.FAILED, Status.NOT_COMPLETED)

    
class StatusSummary(Summary):
    pass
