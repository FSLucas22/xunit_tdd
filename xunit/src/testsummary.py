from typing import Protocol, Callable
from xunit.src.testresult import TestResult
import xunit.src.testcolors as color
from abc import ABC, abstractmethod


class TestSummary(Protocol):
    def results(self, result: TestResult) -> str:
        pass


formatter = Callable[[str], str]


class Summary(ABC):
    passed_formatter: formatter
    failed_formatter: formatter
    notCompleted_formatter: formatter
    
    def __init__(self, passed_formatter: formatter = color.green,
                       failed_formatter: formatter = color.red,
                       notCompleted_formatter: formatter = color.yellow):
        self.passed_formatter = passed_formatter
        self.failed_formatter = failed_formatter
        self.notCompleted_formatter = notCompleted_formatter

    @abstractmethod
    def results(self, result: TestResult) -> str:
        pass
    
    
class SimpleTestSummary:
    def results(self, result: TestResult) -> str:
        return f"{result.run_count} run, {result.failed_count} failed, "\
               f"{result.not_completed_count} not completed"


class PassedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.passed.split():
            messege = self.passed_formatter(test + ' - Passed')
            results.append(messege)
        return '\n'.join(results)


class FailedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.failed.split():
            messege = self.failed_formatter(test + ' - Failed')
            results.append(messege)
        return '\n'.join(results)


class NotCompletedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.not_completed.split():
            messege = self.notCompleted_formatter(test + ' - Not completed')
            results.append(messege)
        return '\n'.join(results)


class DetailedTestSummary(Summary):
    def results(self, result: TestResult) -> str:
        summary = [
            FailedSummary(failed_formatter=self.failed_formatter).results(result),
            PassedSummary(passed_formatter=self.passed_formatter).results(result),
            NotCompletedSummary(notCompleted_formatter=self.notCompleted_formatter).results(result)
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
        for error_info in result._failed_errors:
            messege = self.failed_formatter(
                f"{error_info.test_name} - Failed\n{error_info.error_info}"
            )
            errors.append(messege)
        for error_info in result._not_completed_errors:
            messege = self.notCompleted_formatter(
                f"{error_info.test_name} - Not completed\n{error_info.error_info}"
            )
            errors.append(messege)
        return '\n'.join(errors)
