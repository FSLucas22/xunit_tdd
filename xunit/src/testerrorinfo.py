import traceback
from typing import Type, Protocol, NamedTuple
from xunit.src.status import TestStatus


class TestErrorInfo(TestStatus):

    @property
    def test_name(self) -> str:
        return self.name

    @property
    def error_info(self) -> str:
        return self.info

    @staticmethod
    def from_exception(error: Exception, name: str | None = None, result: str | None = "Failed"
                      ) -> 'TestErrorInfo':
        error_info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        test_name = name or traceback.extract_tb(error.__traceback__)[-1][2] 
        return TestErrorInfo(test_name, "Failed", error_info)


class ErrorInfoFactory(Protocol):
    def __call__(self, error: Exception, name: str | None =...
                 ) -> TestErrorInfo:
        pass

        
