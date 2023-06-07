from typing import Protocol, Callable
from xunit.src.testresult import TestResult
from xunit.src.status import Status, TestStatus
import xunit.src.testcolours as color
from abc import ABC, abstractmethod
from collections.abc import Mapping


class TestSummary(Protocol):
    def results(self, result: TestResult) -> str:
        ...


formatter = Callable[[str], str]


FORMATTERS = {
    Status.FAILED: color.red,
    Status.PASSED: color.green,
    Status.NOT_COMPLETED: color.yellow
}


class Summary(ABC):
    def __init__(self, formatters: Mapping[Status, formatter] = FORMATTERS):
        self.formatters = formatters
    
    def formatter(self, status: Status) -> formatter:
        return self.formatters.get(status, lambda x: x)

    @abstractmethod
    def results(self, result: TestResult) -> str:
        pass
    
    
class SimpleTestSummary:
    def results(self, result: TestResult) -> str:
        failed_count = result.get_status_count(Status.FAILED)
        run_count = result.get_status_count(Status.PASSED) + failed_count
        not_completed_count = result.get_status_count(Status.NOT_COMPLETED)
        return f"{run_count} run, {failed_count} failed, {not_completed_count} not completed"


class PassedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for status in result.get_results_of_status(Status.PASSED):
            messege = self.formatter(status.result)(f'{status.name} - {status.result}')
            results.append(messege)
        return '\n'.join(results)


class FailedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for status in result.get_results_of_status(Status.FAILED):
            messege = self.formatter(status.result)(f'{status.name} - {status.result}')
            results.append(messege)
        return '\n'.join(results)


class not_completedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for status in result.get_results_of_status(Status.NOT_COMPLETED):
            messege = self.formatter(status.result)(f'{status.name} - {status.result}')
            results.append(messege)
        return '\n'.join(results)


class DetailedTestSummary(Summary):
    def results(self, result: TestResult) -> str:
        summary = [
            FailedSummary(formatters=self.formatters).results(result),
            PassedSummary(formatters=self.formatters).results(result),
            not_completedSummary(formatters=self.formatters).results(result)
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
    def results(self, result: TestResult) -> str:
        errors = []
        for status in result.get_results_of_status(Status.FAILED, Status.NOT_COMPLETED):
            messege = self.formatter(status.result)(
                f"{status.name} - {status.result}\n{status.info}"
            )
            errors.append(messege)
        return '\n'.join(errors)

    
class StatusSummary(Summary):
    def results(self, result: TestResult) -> str:
        status_list: list[str] = []
        
        for status in result.get_results_of_status():
            messege = self.formatter(status.result)(f"{status.name} - {status.result}: {status.info}")
            status_list.append(messege)

        return "\n".join(status_list)
