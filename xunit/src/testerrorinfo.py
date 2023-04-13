import traceback


class TestErrorInfo:
    line_number: int

    def __init__(self, error: Exception):
        info = traceback.extract_tb(error.__traceback__)[-1]
        self.line_number = info.lineno or 0
