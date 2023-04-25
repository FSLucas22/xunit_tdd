from typing import Type, Self
from xunit.src.testcase import TestCase
from xunit.src.status import TestStatus
from xunit.src.observer import Observer
from xunit.src.testresult import TestResult
import xunit.src.packagemanager as pm
from types import ModuleType


class TestSuite:
    
    def __init__(self) -> None:
        self._tests: list[TestCase] = []
        self._observers: list[Observer] = []
        
    def add(self, *tests: TestCase) -> None:
        for test in tests:
            test.register(self.notify)
        self._tests += list(tests)

    def merge(self, other_suite: 'TestSuite') -> Self:
        merged = type(self)()
        
        for test in self._tests + other_suite._tests:
            merged.add(test)
        
        return merged

    def run(self, result: TestResult = TestResult()) -> None:
        for test in self._tests:
            test.run(result)

    def register(self, *observer: Observer) -> None:
        self._observers += list(observer)

    def notify(self, status: TestStatus) -> None:
        for observer in self._observers:
            observer(status)

    def unregister(self, *observers: Observer) -> None:
        for observer in observers:
            if observer in self._observers:
                self._observers.remove(observer)

    @classmethod
    def from_test_case(cls, *tests: Type[TestCase]) -> Self:
        suite = cls()
        for test_case in tests:
            for testname in test_case.xunit_test_names.split():
                suite.add(test_case(testname))
        return suite

    @classmethod
    def from_module(cls, *modules: ModuleType) -> Self:
        classes = []
        for module in modules:
            classes += pm.get_test_classes(module)
        return cls.from_test_case(*classes)

    @classmethod
    def from_package(cls, package: ModuleType,
                    ignore: pm.Predicate = lambda _,__: False) -> Self:
        objs = pm.get_package_objects(package, ignore)
        suite = cls()
        for obj in objs:
            obj_suite = cls.from_package(
                obj.value, ignore
                ) if obj.is_package else cls.from_module(obj.value)
            suite = suite.merge(obj_suite)
        return suite

    @classmethod
    def from_path(cls, name: str, path: str, is_package: bool,
                 ignore: pm.Predicate=lambda _,__: False) -> Self:
        module = pm.find_module(name, path)
        if is_package:
            return cls.from_package(module, ignore)
        return cls.from_module(module)











