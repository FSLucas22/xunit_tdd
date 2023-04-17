from typing import NamedTuple, cast
from types import ModuleType
import pkgutil
from os.path import dirname


class PackageObject(NamedTuple):
    name: str
    value: ModuleType


class InvalidPathError(Exception):
    pass


def getPackageObjects(package: ModuleType) -> list[PackageObject]:
    if not package.__file__:
        raise InvalidPathError("package must have a valid path")
    
    package_path = dirname(package.__file__)
    modules = pkgutil.iter_modules([package_path])
    objects: list[PackageObject] = []
    
    for module in modules:
        name = module.name
        value = getattr(package, name)
        objects.append(PackageObject(name, value))
        
    return objects
