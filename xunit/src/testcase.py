from xunit.src.testresult import TestResult
from xunit.src.status import TestStatus, StatusFactory
from xunit.src.observer import Observer
from typing import Callable


class TestCase:
    name: str
    xunit_test_names: str
    _is_xunit_test_class: bool
    
    def __init__(self, name: str):
        self.name = name
        self._observers: list[Observer] = []

    def setup(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def notify(self, status: TestStatus) -> None:
        for observer in self._observers:
            observer(status)

    def register(self, *observer: Observer) -> None:
        self._observers += list(observer)

    def run(self, result: TestResult,
            status_factory: StatusFactory = TestStatus.from_exception
            ) -> None:
        try:
            self.setup()
            method = getattr(self, self.name)
        except Exception as e:
            error_info = status_factory(e, self.name, "")
            result._test_not_completed(error_info)
            self.teardown()
            return
        try:
            method()
            result._test_passed(self.name)
        except Exception as e:
            error_info = status_factory(e, self.name, "")
            result._test_failed(error_info)
        self.teardown()
