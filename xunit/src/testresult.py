from xunit.src.status import TestStatus, Status


class TestResult:
    _results: list[TestStatus]
    
    def __init__(self) -> None:
        self._results = []

    def save_status(self, status: TestStatus) -> None:
        self._results.append(status)

    @property
    def run_count(self) -> int:
        return self.passed_count + self.failed_count 

    @property
    def failed_count(self) -> int:
        return self.get_status_count(Status.FAILED)

    @property
    def not_completed_count(self) -> int:
        return self.get_status_count(Status.NOT_COMPLETED)

    @property
    def passed_count(self) -> int:
        return self.get_status_count(Status.PASSED)

    @property
    def results(self) -> list[TestStatus]:
        return self._results[:]
    
    def get_status_count(self, status: Status) -> int:
        return len(self.get_results_of_status(status))
    
    def get_names_of_status(self, status: Status) -> str:
        names = map(lambda x: x.name, self.get_results_of_status(status))
        return ' '.join(names)

    def get_results_of_status(self, status: Status) -> list[TestStatus]:
        return [
            test_status for test_status in self._results if test_status.result == status
        ]
