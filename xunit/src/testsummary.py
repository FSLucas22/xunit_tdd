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


FORMATTERS = {
    Status.FAILED: color.red,
    Status.PASSED: color.green,
    Status.NOT_COMPLETED: color.yellow
}


class Summary:
    def __init__(self, formatters: Mapping[Status, formatter] = FORMATTERS,
                *order_filter: Status):
        self.formatters = formatters
        self.order_filter = order_filter
    
    def formatter(self, status: Status) -> formatter:
        return self.formatters.get(status, lambda x: x)
    
    def test_status_formatter(self, test_status: TestStatus) -> str:
       return self.formatter(test_status.result)(f'{test_status.name} - {test_status.result}')

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
    def __init__(self, formatters: Mapping[Status, formatter] = FORMATTERS):
        self.formatters = formatters
    
    def results(self, result: TestResult) -> str:
        summary = [
            Summary(self.formatters, Status.FAILED).results(result),
            Summary(self.formatters, Status.PASSED).results(result),
            Summary(self.formatters, Status.NOT_COMPLETED).results(result)
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
    def __init__(self, formatters: Mapping[Status, formatter] = FORMATTERS) -> None:
        super().__init__(formatters, Status.FAILED, Status.NOT_COMPLETED)

    def test_status_formatter(self, test_status: TestStatus) -> str:
       return self.formatter(test_status.result)(
           f"{test_status.name} - {test_status.result}\n{test_status.info}")

    
class StatusSummary(Summary):
    def test_status_formatter(self, test_status: TestStatus) -> str:
       return self.formatter(test_status.result)(
           f"{test_status.name} - {test_status.result}: {test_status.info}")

