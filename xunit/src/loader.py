from types import ModuleType
from typing import Protocol, Sequence, Type, TypeVar
from xunit.src.status import StatusFactory, TestStatus
from xunit.src.testcase import TestCase
from xunit.src import packagemanager as pm
from xunit.src.testsuite import Runnable, TestSuite


def load(suite: TestSuite, tests: Sequence[Runnable]) -> TestSuite:
    suite.add(*tests)
    return suite


def tests_from_class(*tests: Type[TestCase]) -> list[TestCase]:
        result: list[TestCase] = []
        for test_case in tests:
            for testname in test_case.xunit_test_names.split():
                result.append(test_case(testname))
        return result


def tests_from_module(*modules: ModuleType) -> list[TestCase]:
    result: list[TestCase] = []
    for module in modules:
        tests = tests_from_class(*pm.get_test_classes(module))
        result.extend(tests)
    return result


def tests_from_package(package: ModuleType, ignore: pm.Predicate = pm.ignore_name) -> list[TestCase]:
    result: list[TestCase] = []
    objs = pm.get_package_objects(package, ignore)
    for obj in objs:
        if obj.is_package:
            result.extend(tests_from_package(obj.value, ignore=ignore))
        else:
            result.extend(tests_from_module(obj.value))
    return result


def suites_from_class(*tests: Type[TestCase], 
                     error_info_factory: StatusFactory = TestStatus.from_exception) -> list[TestSuite]:
    result: list[TestSuite] = []
    for test_case in tests:
        suite = TestSuite(name=test_case.__name__, error_info_factory=error_info_factory)
        suite.add(*tests_from_class(test_case))
        result.append(suite)
    return result


def suites_from_module(*modules: ModuleType) -> list[TestSuite]:
    result: list[TestSuite] = []
    for module in modules:
        suite = TestSuite(name=module.__name__)
        suite.add(*suites_from_class(*pm.get_test_classes(module)))
        result.append(suite)
    return result


def suites_from_package(package: ModuleType, ignore: pm.Predicate = pm.ignore_name) -> list[TestSuite]:
    objs: list[pm.PackageObject] = pm.get_package_objects(package, ignore)
    main_suite = TestSuite(name=package.__name__)
    for obj in objs:
        suite = TestSuite(name=obj.name)
        if obj.is_package:
            suite.add(*suites_from_package(obj.value, ignore=ignore))
        else:
            suite.add(*suites_from_module(obj.value))
        main_suite.add(suite)
    return [main_suite]
