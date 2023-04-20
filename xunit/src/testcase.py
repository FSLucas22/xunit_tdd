from xunit.src.testresult import TestResult
from xunit.src.testerrorinfo import TestErrorInfo, ErrorInfoFactory
from typing import Callable


class TestCase:
    name: str
    xunit_test_names: str
    _is_xunit_test_class: bool
    
    def __init__(self, name: str):
        self.name = name

    def setup(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def run(self, result: TestResult,
            error_info_factory: ErrorInfoFactory = TestErrorInfo.from_exception
            ) -> None:
        try:
            self.setup()
            method = getattr(self, self.name)
        except Exception as e:
            error_info = error_info_factory(e, self.name)
            result._test_not_completed(error_info)
            self.teardown()
            return
        try:
            method()
            result._test_passed(self.name)
        except Exception as e:
            error_info = error_info_factory(e, self.name)
            result._test_failed(error_info)
        self.teardown()
