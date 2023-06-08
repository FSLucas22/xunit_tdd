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

    @classmethod
    def suite(cls, observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
              error_info_factory: StatusFactory = TestStatus.from_exception) -> Self:
        if observers is None:
            observers = []
        return cls(*observers, name=name, error_info_factory=error_info_factory)

    @classmethod
    def from_test_case(cls, *tests: Type[TestCase],
                       observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
                       error_info_factory: StatusFactory = TestStatus.from_exception) -> Self:
        suite = cls.suite(observers, name, error_info_factory)
        for test_case in tests:
            test_suite = cls.suite(name=test_case.__name__, error_info_factory=error_info_factory)
            for testname in test_case.xunit_test_names.split():
                test_suite.add(test_case(testname))
            suite.add(test_suite)
        return suite

    @classmethod
    def from_module(cls, *modules: ModuleType,
                    observers: list[Observer] | None = None) -> Self:
        classes = []
        for module in modules:
            classes += pm.get_test_classes(module)
        return cls.from_test_case(*classes, observers=observers)

    @classmethod
    def from_package(cls, package: ModuleType,
                    ignore: pm.Predicate = lambda _,__: False,
                    observers: list[Observer] | None = None) -> Self:
        objs = pm.get_package_objects(package, ignore)
        suite = cls()
        for obj in objs:
            obj_suite = cls.from_package(
                obj.value, ignore=ignore
                ) if obj.is_package else cls.from_module(obj.value)
            suite.add(obj_suite)
        if observers is None:
            observers = []
        suite.register(*observers)
        return suite
