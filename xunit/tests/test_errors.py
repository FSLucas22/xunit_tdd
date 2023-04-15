from xunit.src import *


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
        except Exceptin as e:
            info = TestErrorInfo.fromException(e)
            assert info.line_number == 23
            assert info.exception_type == InvalidAttributeException
            assert info.path == __file__
            assert info.error_info == "Test"
            assert info.test_name == "testErrorInfo"
