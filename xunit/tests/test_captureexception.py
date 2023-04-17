from xunit.src import *
from xunit.tests.testclasses import *


@TestClass
class TestCaptureException(TestCase):
    
    @Test
    def testCaptureException(self) -> None:
        @TestClass
        class SomeTestClass(TestCase):
            @Test
            def testError(self) -> None:
                with expects(InvalidAttributeException) as e:
                    raise InvalidAttributeException
            @Test
            def testDifferentError(self) -> None:
                with expects(InvalidAttributeException) as e:
                    raise Exception
        result = TestResult()
        TestSuite.fromTestCase(SomeTestClass).run(result)
        assert result.getAllPassed() == "testError"
        assert result.getAllFailed() == "testDifferentError"
