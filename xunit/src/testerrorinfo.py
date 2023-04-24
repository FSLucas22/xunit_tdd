import traceback
from typing import Type, Protocol, NamedTuple
from xunit.src.status import TestStatus


class TestErrorInfo(TestStatus):

    @staticmethod
    def from_exception(error: Exception, test_name: str | None = None
                      ) -> 'TestErrorInfo':
        name = traceback.extract_tb(error.__traceback__)[-1][2]
        error_info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        test_name = test_name or name
        return TestErrorInfo(test_name, "Failed", error_info)


class ErrorInfoFactory(Protocol):
    def __call__(self, error: Exception,/,test_name: str | None =...
                 ) -> TestErrorInfo:
        pass

        
