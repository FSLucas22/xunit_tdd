from typing import NamedTuple, Protocol
from enum import StrEnum, auto
import traceback


class Status(StrEnum):
    PASSED = "Passed"
    FAILED = "Failed"
    not_completed = "Not completed"


class TestStatus(NamedTuple):
    name: str
    result: str
    info: str

    @staticmethod
    def from_exception(error: Exception, name: str, result: str) -> 'TestStatus':
        info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        return TestStatus(name, result, info)


class StatusFactory(Protocol):
    def __call__(self, error: Exception, name: str, result: str) -> TestStatus:
        pass
