from typing import NamedTuple, Callable, Protocol, Type
from xunit.src.testcase import TestCase
from types import ModuleType
from inspect import getmembers
import pkgutil
import importlib
import importlib.util
from pathlib import Path
import os
from os.path import dirname
import sys


class PackageObject(NamedTuple):
    name: str
    value: ModuleType
    is_package: bool = False


class InvalidPathError(Exception):
    pass


class Predicate(Protocol):
    def __call__(self, obj: PackageObject, pkg: ModuleType, /) -> bool:
        pass


def getPackageObjects(package: ModuleType,
                      ignore: Predicate = lambda obj, pkg: False
                      ) -> list[PackageObject]:
    if not package.__file__:
        raise InvalidPathError("package must have a valid path")
    
    package_path = dirname(package.__file__)
    modules = pkgutil.iter_modules([package_path])
    
    objects: list[PackageObject] = []
    
    for module in modules:
        name = module.name
        value = importlib.import_module(package.__name__ + '.' + name)
        is_package = module.ispkg
        obj = PackageObject(name, value, is_package)
        if ignore(obj, package):
            continue
        objects.append(obj)
        
    return objects


def getIgnoreFileContent(package: ModuleType) -> list[str]:
    if not package.__file__:
        raise InvalidPathError("package must have a valid path")
    package_path = Path(dirname(package.__file__))
    ignore_path = package_path / 'ignore.txt'
    try:
        with open(ignore_path, 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]
            return lines
    except FileNotFoundError as e:
        return []


def ignoreName(obj: PackageObject, pkg: ModuleType | None = None) -> bool:
    if pkg is None:
        raise Exception
    return obj.name in getIgnoreFileContent(pkg)


def findModule(module_name: str, file_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ModuleNotFoundError("Module not found.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def getPath(name: str, directory_path: str, is_package: bool) -> str:
    path = directory_path + "\\" + name
    if is_package:
        path += "\\" + "__init__.py"
    return path


def getTestClasses(module: ModuleType) -> list[Type[TestCase]]:
    return [cls for _, cls in getmembers(
        module,
        lambda value: hasattr(value, "_is_xunit_test_class") and \
        value._is_xunit_test_class and value.__module__ == module.__name__
    )]





