from xunit.src import *
import traceback


@TestClass
class TestErrors(TestCase):

    @Test
    def testErrorInfo(self) -> None:
        try:
            raise InvalidAttributeException
        except Exception as e:
            info = TestErrorInfo(e, line_number=11, error_info="Test",
                                 test_name="testErrorInfo")
            assert info.line_number == 11
            assert info.exception_type == InvalidAttributeException
            assert info.path == __file__
            assert info.error_info == "Test"
            assert info.test_name == "testErrorInfo"

    @Test
    def testFromException(self) -> None:
        try:
            raise InvalidAttributeException("Test")
        except Exception as e:
            error_info = traceback.extract_tb(e.__traceback__)[-1]
            info = TestErrorInfo.fromException(e)
            assert info.line_number == 24
            assert info.exception_type == InvalidAttributeException
            assert info.path == __file__
            assert info.error_info == ''.join(
            traceback.format_exception(type(e), e, e.__traceback__)
            )
            assert info.test_name == "testFromException"

    @Test
    def testFromExceptionWithTestName(self) -> None:
        try:
            raise InvalidAttributeException("Test")
        except Exception as e:
            info = TestErrorInfo.fromException(e, "testMethod")
            assert info.test_name == "testMethod"


