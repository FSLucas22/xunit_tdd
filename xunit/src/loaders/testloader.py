from types import ModuleType
from typing import Type
from xunit.src.testcase import TestCase
from xunit.src import packagemanager as pm


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
