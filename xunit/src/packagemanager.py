import importlib
import importlib.util
import pkgutil
from inspect import getmembers
from os.path import dirname
from pathlib import Path
from types import ModuleType
from typing import NamedTuple, Protocol, Type

from xunit.src.testcase import TestCase
from xunit.src.testexceptions import InvalidPathError


class PackageObject(NamedTuple):
    name: str
    value: ModuleType
    is_package: bool = False


class Predicate(Protocol):
    def __call__(self, obj: PackageObject, pkg: ModuleType, /) -> bool:
        ...


def get_package_objects(package: ModuleType,
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


def get_ignore_file_content(package: ModuleType) -> list[str]:
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


def ignore_name(obj: PackageObject, pkg: ModuleType | None = None) -> bool:
    if pkg is None:
        raise Exception
    return obj.name in get_ignore_file_content(pkg)


def get_test_classes(module: ModuleType) -> list[Type[TestCase]]:
    return [cls for _, cls in getmembers(
        module,
        lambda value: hasattr(value, "_is_xunit_test_class") and \
        value._is_xunit_test_class and value.__module__ == module.__name__
    )]





