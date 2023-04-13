from xunit.src import *
import traceback


@TestClass
class TestErrors(TestCase):

    @Test
    def testErrorInfo(self) -> None:
        try:
            raise InvalidAttributeException
        except Exception as e:
            info = TestErrorInfo(e, error_info="Test")
            assert info.line_number == 11
            assert info.exception_type == InvalidAttributeException
            assert info.path == __file__
            assert info.error_info == "Test"
