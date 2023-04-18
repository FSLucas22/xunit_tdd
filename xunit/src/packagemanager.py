from typing import NamedTuple, Callable, Protocol
from types import ModuleType
import pkgutil
import importlib
from pathlib import Path
from os.path import dirname


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


def findModule(path: str) -> ModuleType:
    return importlib.import_module(path)






