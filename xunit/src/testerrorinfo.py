import traceback
from typing import Type, Self


class TestErrorInfo:
    line_number: int
    exception_type: Type[Exception]
    path: str | None
    error_info: str
    test_name: str
    
    def __init__(self, error: Exception, line_number: int,
                 error_info: str, test_name: str):
        self.line_number = line_number
        self.error_info = error_info
        self.exception_type = type(error)
        self.test_name = test_name
        try:
            info = traceback.extract_tb(error.__traceback__)[-1]
            self.path = info.filename
        except:
            self.path = None

    @staticmethod
    def fromException(error: Exception) -> 'TestErrorInfo':
        info = traceback.extract_tb(error.__traceback__)[-1]
        line_number = info.lineno or -1
        error_info = ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        test_name = info[2]
        return TestErrorInfo(error, line_number, error_info, test_name)

        
