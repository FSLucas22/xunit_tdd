from xunit.src import *
from xunit.tests.testclasses import *


@TestClass
class TestCaptureException(TestCase):
    
    @Test
    def test_capture_exception(self) -> None:
        @TestClass
        class SomeTestClass(TestCase):
            @Test
            def testError(self) -> None:
                with expects(InvalidAttributeException):
                    raise InvalidAttributeException
            @Test
            def testDifferentError(self) -> None:
                with expects(InvalidAttributeException):
                    raise Exception

            @Test
            def testNoError(self) -> None:
                with expects(InvalidAttributeException):
                    pass
                
        result = TestResult()
        TestSuite.from_test_case(SomeTestClass).run(result)
        assert result.passed == "testError"
        assert result.failed == "testDifferentError testNoError"

    @Test
    def test_raises_expectation_error(self) -> None:
        with expects(ExpectationError):
            with expects(Exception):
                pass

        
