from xunit.src import *
from xunit.tests.testclasses import *
from xunit.src.loaders import testloader as loader


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
        suite = TestSuite(result.save_status)
        suite.add(*loader.tests_from_class(SomeTestClass))
        suite.run()

        assert result.get_names_of_status(Status.PASSED) == "testError"
        assert result.get_names_of_status(Status.FAILED) == "testDifferentError testNoError"

    @Test
    def test_raises_expectation_error(self) -> None:
        with expects(ExpectationError):
            with expects(Exception):
                pass
