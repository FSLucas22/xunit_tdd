from typing import Protocol, Callable
from xunit.src.testresult import TestResult
from abc import ABC, abstractmethod


class TestSummary(Protocol):
    def results(self, result: TestResult) -> str:
        pass


formatter = Callable[[str], str]


class Summary(ABC):
    passed_formatter: formatter
    failed_formatter: formatter
    notCompleted_formatter: formatter
    
    def __init__(self, passed_formatter: formatter = lambda messege: messege,
                       failed_formatter: formatter = lambda messege: messege,
                       notCompleted_formatter: formatter = lambda messege: messege):
        self.passed_formatter = passed_formatter
        self.failed_formatter = failed_formatter
        self.notCompleted_formatter = notCompleted_formatter

    @abstractmethod
    def results(self, result: TestResult) -> str:
        pass
    
    
class SimpleTestSummary:
    def results(self, result: TestResult) -> str:
        return f"{result.runCount} run, {result.failedCount} failed, {result.notCompletedCount} not completed"


class PassedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.getAllPassed().split():
            messege = self.passed_formatter(test + ' - Passed')
            results.append(messege)
        return '\n'.join(results)


class FailedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.getAllFailed().split():
            messege = self.failed_formatter(test + ' - Failed')
            results.append(messege)
        return '\n'.join(results)


class NotCompletedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.getAllNotCompleted().split():
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
        for error_info in result.failedErrors:
            messege = self.failed_formatter(
                f"{error_info.test_name} - Failed\n{error_info.error_info}"
            )
            errors.append(messege)
        for error_info in result.notCompletedErrors:
            messege = self.notCompleted_formatter(
                f"{error_info.test_name} - Not completed\n{error_info.error_info}"
            )
            errors.append(messege)
        return '\n'.join(errors)
