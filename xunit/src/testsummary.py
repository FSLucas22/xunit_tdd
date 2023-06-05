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
    passed_formatter: formatter
    failed_formatter: formatter
    not_completed_formatter: formatter
    
    def __init__(self, passed_formatter: formatter = color.green,
                       failed_formatter: formatter = color.red,
                       not_completed_formatter: formatter = color.yellow, formatters: Mapping[Status, formatter] = FORMATTERS):
        self.passed_formatter = passed_formatter
        self.failed_formatter = failed_formatter
        self.not_completed_formatter = not_completed_formatter
        self.formatters = formatters
    
    def formatter(self, status: Status) -> formatter:
        return self.formatters.get(status, lambda x: x)

    @abstractmethod
    def results(self, result: TestResult) -> str:
        pass
    
    
class SimpleTestSummary:
    def results(self, result: TestResult) -> str:
        return f"{result.run_count} run, {result.failed_count} failed, "\
               f"{result.not_completed_count} not completed"


class PassedSummary(Summary):

    def formatter(self, status: Status) -> formatter:
        return self.passed_formatter
    
    def is_interesting(self, test_status: TestStatus) -> bool:
        return test_status.result is Status.PASSED
    
    def results(self, result: TestResult) -> str:
        results = []
        for status in filter(self.is_interesting, result.results):
            messege = self.formatter(status.result)(f'{status.name} - {status.result}')
            results.append(messege)
        return '\n'.join(results)


class FailedSummary(Summary):
    def formatter(self, status: Status) -> formatter:
        return self.failed_formatter

    def is_interesting(self, test_status: TestStatus) -> bool:
        return test_status.result is Status.FAILED
    
    def results(self, result: TestResult) -> str:
        results = []
        for status in filter(self.is_interesting, result.results):
            messege = self.formatter(status.result)(f'{status.name} - {status.result}')
            results.append(messege)
        return '\n'.join(results)


class not_completedSummary(Summary):
    def formatter(self, status: Status) -> formatter:
        return self.not_completed_formatter

    def is_interesting(self, test_status: TestStatus) -> bool:
        return test_status.result is Status.NOT_COMPLETED
    
    def results(self, result: TestResult) -> str:
        results = []
        for status in filter(self.is_interesting, result.results):
            messege = self.formatter(status.result)(f'{status.name} - {status.result}')
            results.append(messege)
        return '\n'.join(results)



class DetailedTestSummary(Summary):
    def results(self, result: TestResult) -> str:
        summary = [
            FailedSummary(failed_formatter=self.failed_formatter).results(result),
            PassedSummary(passed_formatter=self.passed_formatter).results(result),
            not_completedSummary(not_completed_formatter=self.not_completed_formatter).results(result)
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
        for error_info in result.failed_errors:
            messege = self.failed_formatter(
                f"{error_info.name} - Failed\n{error_info.info}"
            )
            errors.append(messege)
        for error_info in result.not_completed_errors:
            messege = self.not_completed_formatter(
                f"{error_info.name} - Not completed\n{error_info.info}"
            )
            errors.append(messege)
        return '\n'.join(errors)

    
class StatusSummary(Summary):
    def results(self, result: TestResult) -> str:
        status_list: list[str] = []
        
        for status in result.results:
            messege = self.formatter(status.result)(
                f"{status.name} - {status.result}: {status.info}"
            )
            status_list.append(messege)

        return "\n".join(status_list)
