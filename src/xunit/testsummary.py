from typing import Protocol
from .testresult import TestResult
from .status import Status
from .formatters import *


class Summary(Protocol):
    def results(self, result: TestResult) -> str:
        ...


class TestSummary:
    def __init__(self, formatter: test_status_formatter = FORMATTERS,
                *order_filter: Status):
        self.order_filter = order_filter
        self.formatter = formatter

    def results(self, result: TestResult) -> str:
        
        status_list: list[str] = []
        
        for status in result.get_results(*self.order_filter):
            messege = self.formatter(status)
            status_list.append(messege)

        return "\n".join(status_list)
    
    
class SimpleTestSummary:
    def results(self, result: TestResult) -> str:
        failed_count = result.get_status_count(Status.FAILED)
        run_count = result.get_status_count(Status.PASSED) + failed_count
        not_completed_count = result.get_status_count(Status.NOT_COMPLETED)
        return f"{run_count} run, {failed_count} failed, {not_completed_count} not completed"


class MixedTestSummary:
    def __init__(self, *summaries: Summary):
        self.summaries = summaries
        
    def results(self, result: TestResult) -> str:
        summary_results = []
        for summary in self.summaries:
            summary_results.append(summary.results(result))
        return '\n'.join(summary_results)
