from xunit.src import *
from xunit.src.testerrorinfo import TestErrorInfo
import traceback


@TestClass
class TestErrors(TestCase):

    @Test
    def test_from_exception(self) -> None:
        try:
            raise InvalidAttributeException("Test")
        except Exception as e:
            error_info = traceback.extract_tb(e.__traceback__)[-1]
            info = TestErrorInfo.from_exception(e)
            assert info.error_info == ''.join(
            traceback.format_exception(type(e), e, e.__traceback__)
            )
            assert info.test_name == "test_from_exception"

    @Test
    def test_from_exception_with_test_name(self) -> None:
        try:
            raise InvalidAttributeException("Test")
        except Exception as e:
            info = TestErrorInfo.from_exception(e, "testMethod")
            assert info.test_name == "testMethod"

    @Test
    def test_equality(self) -> None:
        assert TestErrorInfo("x", "y") == TestErrorInfo("x", "y")


