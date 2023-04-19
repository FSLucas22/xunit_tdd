from xunit.src.testresult import TestResult
from xunit.src.testerrorinfo import TestErrorInfo, ErrorInfoFactory
from typing import Callable


class TestCase:
    name: str
    testNames: str
    _is_xunit_test_class: bool
    
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self, result: TestResult,
            error_info_factory: ErrorInfoFactory = TestErrorInfo.fromException
            ) -> None:
        try:
            self.setUp()
            method = getattr(self, self.name)
        except Exception as e:
            error_info = error_info_factory(e, self.name)
            result._test_not_completed(self.name, error_info)
            self.tearDown()
            return
        try:
            method()
            result._test_passed(self.name)
        except Exception as e:
            error_info = error_info_factory(e, self.name)
            result._test_failed(self.name, error_info)
        self.tearDown()
