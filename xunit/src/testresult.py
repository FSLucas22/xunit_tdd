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
        return len(self.get_results_of_status(Status.FAILED))

    @property
    def not_completed_count(self) -> int:
        return len(self.get_results_of_status(Status.NOT_COMPLETED))

    @property
    def passed_count(self) -> int:
        return len(self.get_results_of_status(Status.PASSED))

    @property
    def failed_errors(self) -> list[TestStatus]:
        return self.get_results_of_status(Status.FAILED)

    @property
    def not_completed_errors(self) -> list[TestStatus]:
        return self.get_results_of_status(Status.NOT_COMPLETED)

    @property
    def results(self) -> list[TestStatus]:
        return self._results[:]

    @property
    def failed(self) -> str:
        return self.get_names_of_status(Status.FAILED)

    @property
    def passed(self) -> str:
        return self.get_names_of_status(Status.PASSED)

    @property
    def not_completed(self) -> str:
        return self.get_names_of_status(Status.NOT_COMPLETED)
    
    def get_names_of_status(self, status: Status) -> str:
        names = map(lambda x: x.name, self.get_results_of_status(status))
        return ' '.join(names)

    def get_results_of_status(self, status: Status) -> list[TestStatus]:
        return [
            test_status for test_status in self._results if test_status.result == status
        ]
