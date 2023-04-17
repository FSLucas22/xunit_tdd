from typing import NamedTuple
from types import ModuleType


class PackageObject(NamedTuple):
    name: str
    value: ModuleType
