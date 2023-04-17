from xunit.src import *
from xunit.tests.testclasses import *


@TestClass
class TestCaptureException(TestCase):
    def testCaptureException(self) -> None:
        class SomeTestClass(TestCase):
            def testError(self) -> None:
                with expects(InvalidAttributeException) as e:
                    raise InvalidAttributeException
        result = TestResult()
        SomeTestClass("testError").run(result)
        assert result.getAllPassed() == "testError"
