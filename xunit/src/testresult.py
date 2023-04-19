from xunit.src.log import Log
from xunit.src.testerrorinfo import TestErrorInfo


class TestResult:
    _failed: Log
    _passed: Log
    _not_completed: Log
    _failed_errors: list[TestErrorInfo]
    _not_completed_errors: list[TestErrorInfo]
    
    def __init__(self) -> None:
        self._failed = Log()
        self._not_completed = Log()
        self._passed = Log()
        self._failed_errors = []
        self._not_completed_errors = []
        
    def _test_not_completed(self, test_name: str,
                         error_info: TestErrorInfo) -> None:
        self._not_completed_errors.append(error_info)

    def _test_passed(self, test_name: str) -> None:
        self._passed.register(test_name)

    def _test_failed(self, test_name: str, error_info: TestErrorInfo) -> None:
        self._failed_errors.append(error_info)

    @property
    def run_count(self) -> int:
        return self._passed.register_count() + \
               len(self._failed_errors) 

    @property
    def failed_count(self) -> int:
        return len(self._failed_errors)

    @property
    def not_completed_count(self) -> int:
        return len(self._not_completed_errors)

    @property
    def passed_count(self) -> int:
        return self._passed.register_count()

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
            errors.register(error.test_name)
        return errors.executed

    @property
    def passed(self) -> str:
        return self._passed.executed

    @property
    def not_completed(self) -> str:
        errors = Log()
        for error in self._not_completed_errors:
            errors.register(error.test_name)
        return errors.executed
