from typing import Type, Self
from xunit.src.testcase import TestCase
from xunit.src.status import TestStatus, Status
from xunit.src.observer import Observer, SubjectImp
from xunit.src.testresult import TestResult
import xunit.src.packagemanager as pm
from types import ModuleType


class TestSuite(SubjectImp):
    
    def __init__(self, *observers: Observer) -> None:
        self._tests: list[TestCase] = []
        super().__init__(*observers)
        
    def add(self, *tests: TestCase) -> None:
        for test in tests:
            test.register(self.notify)
        self._tests += list(tests)

    def merge(self, other_suite: 'TestSuite') -> Self:
        merged = type(self)()
        
        for test in self._tests + other_suite._tests:
            merged.add(test)
        
        return merged

    def run(self) -> None:
        self.notify(TestStatus("Suite", Status.CREATED, "individual"))
        for test in self._tests:
            test.run()

    @classmethod
    def suite(cls, observers: list[Observer] | None = None) -> Self:
        if observers is None:
            observers = []
        return cls(*observers)

    @classmethod
    def from_test_case(cls, *tests: Type[TestCase],
                       observers: list[Observer] | None = None) -> Self:
        suite = cls.suite(observers)
        for test_case in tests:
            for testname in test_case.xunit_test_names.split():
                suite.add(test_case(testname))
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
                obj.value, ignore
                ) if obj.is_package else cls.from_module(obj.value)
            suite = suite.merge(obj_suite)
        if observers is None:
            observers = []
        suite.register(*observers)
        return suite

    @classmethod
    def from_path(cls, name: str, path: str, is_package: bool,
                 ignore: pm.Predicate=lambda _,__: False,
                 observers: list[Observer] | None = None) -> Self:
        module = pm.find_module(name, path)
        if is_package:
            return cls.from_package(module, ignore, observers=observers)
        return cls.from_module(module, observers=observers)











