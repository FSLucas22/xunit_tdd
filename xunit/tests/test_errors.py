from xunit.src import *
from xunit.src.testerrorinfo import TestErrorInfo
import traceback


@TestClass
class TestErrors(TestCase):

    @Test
    def testErrorInfo(self) -> None:
        try:
            raise InvalidAttributeException
        except Exception as e:
            info = TestErrorInfo(
                error_info="Test", test_name="testErrorInfo"
            )
            assert info.error_info == "Test"
            assert info.test_name == "testErrorInfo"

    @Test
    def testFromException(self) -> None:
        try:
            raise InvalidAttributeException("Test")
        except Exception as e:
            error_info = traceback.extract_tb(e.__traceback__)[-1]
            info = TestErrorInfo.from_exception(e)
            assert info.error_info == ''.join(
            traceback.format_exception(type(e), e, e.__traceback__)
            )
            assert info.test_name == "testFromException"

    @Test
    def testFromExceptionWithTestName(self) -> None:
        try:
            raise InvalidAttributeException("Test")
        except Exception as e:
            info = TestErrorInfo.from_exception(e, "testMethod")
            assert info.test_name == "testMethod"

    @Test
    def testEquality(self) -> None:
        assert TestErrorInfo("x", "y") == TestErrorInfo("x", "y")


