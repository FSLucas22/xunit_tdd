from xunit.src import TestCase, TestErrorInfo


class WasRun(TestCase):
    log: str = ""
    testNames = "testMethod testBrokenMethod"
    def setUp(self) -> None:
        self.log = "setUp"

    def tearDown(self) -> None:
        self.log += " tearDown"

    def testMethod(self) -> None:
       self.log += " testMethod"

    def testBrokenMethod(self) -> None:
        raise Exception


class FailedSetUp(WasRun):
    def setUp(self) -> None:
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


class MockTestErrorInfo(TestErrorInfo):
    calls: int
    exception_passed: Exception

    def __init__(self, calls: int, exception_passed: Exception) -> None:
        self.calls = calls
        self.exception_passed = exception_passed
    
    @staticmethod
    def fromException(error: Exception) -> 'MockTestErrorInfo':
        return MockTestErrorInfo(1, error)









