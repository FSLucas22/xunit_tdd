from typing import Protocol
from xunit.src.testresult import TestResult


class TestSummary(Protocol):
    def results(self, result: TestResult) -> str:
        pass

    
class SimpleTestSummary:
    def results(self, result: TestResult) -> str:
        return f"{result.runCount} run, {result.failedCount} failed, {result.notCompletedCount} not completed"


class DetailedTestSummary:
    def results(self, result: TestResult) -> str:
        summary = ""
        for test in result.getAllFailed().split():
            summary += test + ' - Failed\n'
        for test in result.getAllPassed().split():
            summary += test + ' - Passed\n'
        for test in result.getAllNotCompleted().split():
            summary += test + ' - Not completed\n'
        return summary[:-1]


class MixedTestSummary:
    def __init__(self, *summaries: TestSummary):
        self.summaries = summaries
        
    def results(self, result: TestResult) -> str:
        summary_results = []
        for summary in self.summaries:
            summary_results.append(summary.results(result))
        return '\n'.join(summary_results)


class ErrorInfoSummary:
    def results(self, result: TestResult) -> str:
        error_info = result.failedErrors[0]
        return f"{error_info.test_name} - Failed\n{error_info.error_info}"
