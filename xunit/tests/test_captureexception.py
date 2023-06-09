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
        suite = VerboseSuiteFactory().from_test_case(SomeTestClass)
        suite.register(result.save_status)
        suite.run()
        assert result.get_names_of_status(Status.PASSED) == "testError"
        assert result.get_names_of_status(Status.FAILED) == "testDifferentError testNoError"

    @Test
    def test_raises_expectation_error(self) -> None:
        with expects(ExpectationError):
            with expects(Exception):
                pass
