import traceback
from typing import Type


class TestErrorInfo:
    line_number: int
    exception_type: Type[Exception]
    path: str
    error_info: str
    
    def __init__(self, error: Exception, line_number: int, error_info: str):
        info = traceback.extract_tb(error.__traceback__)[-1]
        self.line_number = line_number
        self.exception_type = type(error)
        self.path = info.filename
        self.error_info = error_info
