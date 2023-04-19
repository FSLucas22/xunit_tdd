from xunit.src import TestCase
from xunit.src.testerrorinfo import TestErrorInfo


class WasRun(TestCase):
    log: str = ""
    testNames = "testMethod testBrokenMethod"
    def setup(self) -> None:
        self.log = "setup"

    def teardown(self) -> None:
        self.log += " teardown"

    def testMethod(self) -> None:
       self.log += " testMethod"

    def testBrokenMethod(self) -> None:
        raise Exception


class FailedSetUp(WasRun):
    def setup(self) -> None:
        raise Exception


class DummyTestCase(TestCase):
    testNames = "passedTest1 passedTest2 failedTest1 failedTest2"
    
    def passedTest1(self) -> None:
        pass

    def passedTest2(self) -> None:
        pass

    def failedTest1(self) -> None:
        raise Exception

    def failedTest2(self) -> None:
        raise Exception


class MockTestCase(TestCase):
    exception_raised: Exception

    def __init__(self, name: str, exception: Exception) -> None:
        self.exception_raised = exception
        super().__init__(name)

    def testMethod(self) -> None:
        raise self.exception_raised

    def testMethod2(self) -> None:
        raise self.exception_raised


class MockBrokenTestCase(TestCase):
    exception_raised: Exception

    def __init__(self, name: str, exception: Exception) -> None:
        self.exception_raised = exception
        super().__init__(name)

    def setup(self) -> None:
        raise self.exception_raised
    
    def testMethod(self) -> None:
        pass


class MockPrint:
    passed_value: str = ""
    
    def __call__(self, result: str) -> None:
        self.passed_value = result




