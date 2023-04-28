from xunit.src.log import Log
from xunit.src.status import TestStatus, Status


class TestResult:
    _results: list[TestStatus]
    
    def __init__(self) -> None:
        self._results = []

    def save_status(self, status: TestStatus) -> None:
        self._results.append(status)

    @property
    def run_count(self) -> int:
        return self.passed_count + \
               len(self.failed_errors) 

    @property
    def failed_count(self) -> int:
        return len(self.failed_errors)

    @property
    def not_completed_count(self) -> int:
        return len(self.not_completed_errors)

    @property
    def passed_count(self) -> int:
        return len(
            [status for status in self._results if status.result == Status.PASSED]
        )

    @property
    def failed_errors(self) -> list[TestStatus]:
        return [status for status in self._results if status.result == Status.FAILED]

    @property
    def not_completed_errors(self) -> list[TestStatus]:
        return [status for status in self._results if status.result == Status.NOT_COMPLETED]
    
    @property
    def started(self) -> str:
        started = Log()
        for passed in self.passed.split():
            started.register(passed)
        for failed in self.failed.split():
            started.register(failed)
        return started.executed

    @property
    def results(self) -> list[TestStatus]:
        return self._results[:]

    @property
    def failed(self) -> str:
        errors = Log()
        for error in self.failed_errors:
            errors.register(error.name)
        return errors.executed

    @property
    def passed(self) -> str:
        names = [
            status.name for status in self._results if status.result == Status.PASSED
        ]
        return ' '.join(names)

    @property
    def not_completed(self) -> str:
        errors = Log()
        for error in self.not_completed_errors:
            errors.register(error.name)
        return errors.executed
