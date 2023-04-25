from typing import NamedTuple, Protocol
import traceback


class TestStatus(NamedTuple):
    name: str
    result: str
    info: str

    @staticmethod
    def from_exception(error: Exception, name: str, info: str) -> 'TestStatus':
        info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        return TestStatus(name, "Failed", info)


class StatusFactory(Protocol):
    def __call__(self, error: Exception, name: str, info: str) -> TestStatus:
        pass
