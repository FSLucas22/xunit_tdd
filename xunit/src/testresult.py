from xunit.src.status import TestStatus, Status


class TestResult:
    _results: list[TestStatus]
    
    def __init__(self) -> None:
        self._results = []

    def save_status(self, status: TestStatus) -> None:
        self._results.append(status)

    @property
    def results(self) -> list[TestStatus]:
        return self._results[:]
    
    def get_status_count(self, status: Status) -> int:
        return len(self.get_results_of_status(status))
    
    def get_names_of_status(self, status: Status) -> str:
        names = map(lambda test_status: test_status.name, self.get_results_of_status(status))
        return ' '.join(names)

    def get_results_of_status(self, status: Status, *other_status: Status) -> list[TestStatus]:
        results = []

        for status in [status] + list(other_status):
            results += [test_status for test_status in self._results if test_status.result == status]

        return results
