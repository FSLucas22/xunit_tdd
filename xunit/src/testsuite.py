from types import ModuleType
from typing import Self, Type, Protocol
import xunit.src.packagemanager as pm
from xunit.src.observer import Observer, Subject, SubjectImp
from xunit.src.status import Status, StatusFactory, TestStatus
from xunit.src.testcase import TestCase


DEFAULT_SUITE_NAME = 'Base suite'


class Runnable(Subject, Protocol):

    def run(self) -> None:
        ...


class TestSuite(SubjectImp):
    name: str
    erro_info_factory: StatusFactory

    def __init__(self, *observers: Observer, name: str = DEFAULT_SUITE_NAME, 
                 error_info_factory: StatusFactory = TestStatus.from_exception) -> None:
        self._tests: list[Runnable] = []
        self.name = name
        self.error_info_factory = error_info_factory
        super().__init__(*observers)
        
    def add(self, *tests: Runnable) -> None:
        for test in tests:
            test.register(self.notify)
        self._tests += list(tests)

    def run(self) -> None:
        self.notify(TestStatus("Suite", Status.CREATED, self.name))
        for test in self._tests:
            try:
                test.run()
            except Exception as e:
                self.notify(
                    self.error_info_factory(e,
                    type(test).__name__, Status.FAILED_TO_RUN)
                )
