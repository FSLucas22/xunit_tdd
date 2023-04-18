from typing import NamedTuple, Callable, Any
from types import ModuleType
import pkgutil
import importlib
from os.path import dirname


class PackageObject(NamedTuple):
    name: str
    value: ModuleType
    is_package: bool = False


class InvalidPathError(Exception):
    pass


Predicate = Callable[[PackageObject], bool]


def getPackageObjects(package: ModuleType, ignore: Predicate = lambda obj: False
                      ) -> list[PackageObject]:
    if not package.__file__:
        raise InvalidPathError("package must have a valid path")
    
    package_path = dirname(package.__file__)
    modules = pkgutil.iter_modules([package_path])
    
    objects: list[PackageObject] = []
    
    for module in modules:
        name = module.name
        value = importlib.import_module(package.__name__ +'.' + name)
        is_package = module.ispkg
        obj = PackageObject(name, value, is_package)
        if ignore(obj):
            continue
        objects.append(obj)
        
    return objects


def getIgnoreFileContent(package: ModuleType) -> None | Any:
    return None







