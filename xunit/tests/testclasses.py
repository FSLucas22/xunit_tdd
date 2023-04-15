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
    exception_passed: Exception

    def __init__(self, exception_passed: Exception, test_name: str | None = None
                 ) -> None:
        self.exception_passed = exception_passed


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

    def setUp(self) -> None:
        raise self.exception_raised
    
    def testMethod(self) -> None:
        pass







