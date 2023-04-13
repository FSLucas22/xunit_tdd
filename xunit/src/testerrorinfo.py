import traceback
from typing import Type

class TestErrorInfo:
    line_number: int
    exception_type: Type[Exception]
    
    def __init__(self, error: Exception):
        info = traceback.extract_tb(error.__traceback__)[-1]
        self.line_number = info.lineno or 0
        self.exception_type = type(error)
