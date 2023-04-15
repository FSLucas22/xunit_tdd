from typing import Protocol, Callable
from xunit.src.testresult import TestResult
from abc import ABC, abstractmethod


class TestSummary(Protocol):
    def results(self, result: TestResult) -> str:
        pass


formatter = Callable[[str], str]


class Summary(ABC):
    def __init__(self, passed_formatter: formatter = lambda messege: messege,
                       failed_formatter: formatter = lambda messege: messege,
                       notCompleted_formatter: formatter = lambda messege: messege):
        self.passed_formater = passed_formatter
        self.failed_formatter = failed_formatter
        self.notCompletedFormatter = notCompleted_formatter

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
            results.append(test + ' - Passed')
        return '\n'.join(results)


class FailedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.getAllFailed().split():
            results.append(test + ' - Failed')
        return '\n'.join(results)


class NotCompletedSummary(Summary):
    def results(self, result: TestResult) -> str:
        results = []
        for test in result.getAllNotCompleted().split():
            results.append(test + ' - Not completed')
        return '\n'.join(results)


class DetailedTestSummary(Summary):
    def results(self, result: TestResult) -> str:
        summary = [
            FailedSummary().results(result),
            PassedSummary().results(result),
            NotCompletedSummary().results(result)
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
            errors.append(f"{error_info.test_name} - Failed\n{error_info.error_info}")
        for error_info in result.notCompletedErrors:
            errors.append(f"{error_info.test_name} - Not completed\n{error_info.error_info}")
        return '\n'.join(errors)
