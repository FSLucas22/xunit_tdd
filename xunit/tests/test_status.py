from xunit.src import *
from xunit.src.status import TestStatus
import traceback


@TestClass
class TestTestStatus(TestCase):

    @Test
    def test_creation(self) -> None:
        status = TestStatus("someTest", "passed", "-")
        assert status.name == "someTest"
        assert status.result == "passed"
        assert status.info == "-"

    @Test
    def test_equality(self) -> None:
        status1 = TestStatus("someTest", "passed", "-")
        status2 = TestStatus("someTest", "passed", "-")
        assert status1 == status2

    @Test
    def test_from_exception(self) -> None:
        try:
            raise InvalidAttributeException("Test")
        except Exception as e:
            error_info = traceback.extract_tb(e.__traceback__)[-1]
            name = "test_from_exception"
            result = "Not completed"
            info = TestStatus.from_exception(e, name, result)
            assert info.info == ''.join(
            traceback.format_exception(type(e), e, e.__traceback__)
            )
            assert info.name == name
            assert info.result == result
