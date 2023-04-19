import traceback
from typing import Type, Protocol


class TestErrorInfo:
    
    def __init__(self, error_info: str, test_name: str):
        self._error_info = error_info
        self._test_name = test_name

    @staticmethod
    def fromException(error: Exception, test_name: str | None = None
                      ) -> 'TestErrorInfo':
        name = traceback.extract_tb(error.__traceback__)[-1][2]
        error_info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        test_name = test_name or name
        return TestErrorInfo(error_info, test_name)

    @property
    def error_info(self) -> str:
        return self._error_info

    @property
    def test_name(self) -> str:
        return self._test_name

    def __str__(self) -> str:
        return f"TestErrorInfo({self.test_name}, {self.error_info})"


class ErrorInfoFactory(Protocol):
    def __call__(self, error: Exception,/,test_name: str | None =...
                 ) -> TestErrorInfo:
        pass

        
