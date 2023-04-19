import traceback
from typing import Type, Protocol, NamedTuple


class TestErrorInfo(NamedTuple):
    error_info: str
    test_name: str

    @staticmethod
    def from_exception(error: Exception, test_name: str | None = None
                      ) -> 'TestErrorInfo':
        name = traceback.extract_tb(error.__traceback__)[-1][2]
        error_info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        test_name = test_name or name
        return TestErrorInfo(error_info, test_name)


class ErrorInfoFactory(Protocol):
    def __call__(self, error: Exception,/,test_name: str | None =...
                 ) -> TestErrorInfo:
        pass

        
