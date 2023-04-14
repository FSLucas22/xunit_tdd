import traceback
from typing import Type


class TestErrorInfo:
    line_number: int
    exception_type: Type[Exception]
    path: str | None
    error_info: str
    test_name: str | None
    
    def __init__(self, error: Exception, line_number: int,
                 error_info: str, test_name: str | None = None):
        self.line_number = line_number
        self.error_info = error_info
        self.exception_type = type(error)
        self.test_name = test_name
        try:
            info = traceback.extract_tb(error.__traceback__)[-1]
            self.path = info.filename
        except:
            self.path = None
