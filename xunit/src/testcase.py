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

    def unregister(self, *observers: Observer) -> None:
        for observer in observers:
            if observer in self._observers:
                self._observers.remove(observer)

    def run(self, status_factory: StatusFactory = TestStatus.from_exception
            ) -> None:
        try:
            self.setup()
            method = getattr(self, self.name)
        except Exception as e:
            info = status_factory(e, self.name, "Not completed")
            self.notify(info)
            self.teardown()
            return
        try:
            method()
            info = TestStatus(self.name, "Passed", "-")
        except Exception as e:
            info = status_factory(e, self.name, "Failed")
        self.notify(info)
        self.teardown()
