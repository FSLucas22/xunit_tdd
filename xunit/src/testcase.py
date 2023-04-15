from xunit.src.testresult import TestResult
from xunit.src.testerrorinfo import TestErrorInfo
from typing import Callable


class TestCase:
    name: str
    testNames: str

    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self, result: TestResult,
            error_info_factory: Callable[[Exception], TestErrorInfo] = TestErrorInfo.fromException
            ) -> None:
        try:
            self.setUp()
            method = getattr(self, self.name)
        except Exception as e:
            error_info = error_info_factory(e)
            result.testNotCompleted(self.name, error_info)
            self.tearDown()
            return
        try:
            method()
            result.testPassed(self.name)
        except Exception as e:
            error_info = error_info_factory(e)
            result.testFailed(self.name, error_info)
        self.tearDown()
