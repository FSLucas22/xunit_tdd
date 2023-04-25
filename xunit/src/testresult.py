from xunit.src.log import Log
from xunit.src.status import TestStatus


class TestResult:
    _results: list[TestStatus]
    
    def __init__(self) -> None:
        self._results = []

    def save_status(self, status: TestStatus) -> None:
        self._results.append(status)

    @property
    def run_count(self) -> int:
        return self.passed_count + \
               len(self._failed_errors) 

    @property
    def failed_count(self) -> int:
        return len(self._failed_errors)

    @property
    def not_completed_count(self) -> int:
        return len(self._not_completed_errors)

    @property
    def passed_count(self) -> int:
        return len(
            [status for status in self._results if status.result == "Passed"]
        )

    @property
    def _failed_errors(self) -> list[TestStatus]:
        return [status for status in self._results if status.result == "Failed"]

    @property
    def _not_completed_errors(self) -> list[TestStatus]:
        return [status for status in self._results if status.result == "Not completed"]
    
    @property
    def started(self) -> str:
        started = Log()
        for passed in self.passed.split():
            started.register(passed)
        for failed in self.failed.split():
            started.register(failed)
        return started.executed

    @property
    def failed(self) -> str:
        errors = Log()
        for error in self._failed_errors:
            errors.register(error.name)
        return errors.executed

    @property
    def passed(self) -> str:
        names = [
            status.name for status in self._results if status.result == "Passed"
        ]
        return ' '.join(names)

    @property
    def not_completed(self) -> str:
        errors = Log()
        for error in self._not_completed_errors:
            errors.register(error.name)
        return errors.executed
