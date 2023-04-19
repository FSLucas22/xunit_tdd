import traceback
from typing import Type, Protocol


class TestErrorInfo:
    line_number: int
    exception_type: Type[Exception]
    path: str | None
    error_info: str
    test_name: str
    
    def __init__(self, error: Exception, line_number: int,
                 error_info: str, test_name: str):
        self.error_info = error_info
        self.test_name = test_name

    @staticmethod
    def fromException(error: Exception, test_name: str | None = None) -> 'TestErrorInfo':
        name = traceback.extract_tb(error.__traceback__)[-1][2]
        error_info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        test_name = test_name or name
        return TestErrorInfo(error, 1, error_info, test_name)

    def __str__(self) -> str:
        return f"TestErrorInfo({self.test_name}, {self.error_info})"


class ErrorInfoFactory(Protocol):
    def __call__(self, error: Exception,/,test_name: str | None =...
                 ) -> TestErrorInfo:
        pass

        
