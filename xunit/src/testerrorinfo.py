import traceback
from typing import Type


class TestErrorInfo:
    line_number: int
    exception_type: Type[Exception]
    path: str | None
    error_info: str
    
    def __init__(self, error: Exception, line_number: int, error_info: str):
        self.line_number = line_number
        self.error_info = error_info
        self.exception_type = type(error)
        try:
            info = traceback.extract_tb(error.__traceback__)[-1]
            self.path = info.filename
        except:
            self.path = None
