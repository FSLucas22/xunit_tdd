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


class SuiteFactory(Protocol):
    def suite(self, observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME, 
              error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        ...
    
    def from_test_case(self, *tests: Type[TestCase],
                       observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
                       error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        ...
    
    def from_module(self, *modules: ModuleType,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        ...

    def from_package(self, package: ModuleType,
                    ignore: pm.Predicate = lambda _,__: False,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        ...


class SuiteFactoryImp:
    def suite(self, observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
              error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        if observers is None:
            observers = []
        return TestSuite(*observers, name=name, error_info_factory=error_info_factory)

    def from_test_case(self, *tests: Type[TestCase],
                       observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
                       error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        suite = self.suite(observers, name, error_info_factory)
        for test_case in tests:
            test_suite = self.suite(name=test_case.__name__, error_info_factory=error_info_factory)
            for testname in test_case.xunit_test_names.split():
                test_suite.add(test_case(testname))
            suite.add(test_suite)
        return suite

    def from_module(self, *modules: ModuleType,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        base_suite = self.suite(observers=observers, name=name)
        for module in modules:
            module_suite = self.from_test_case(*pm.get_test_classes(module), name=module.__name__)
            base_suite.add(module_suite)
        return base_suite

    def from_package(self, package: ModuleType,
                    ignore: pm.Predicate = lambda _,__: False,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        objs = pm.get_package_objects(package, ignore)
        suite = self.suite(name=name)
        for obj in objs:
            obj_suite = self.from_package(
                obj.value, ignore=ignore, name=obj.name
                ) if obj.is_package else self.from_module(obj.value, name=obj.name)
            suite.add(obj_suite)
        if observers is None:
            observers = []
        suite.register(*observers)
        return suite