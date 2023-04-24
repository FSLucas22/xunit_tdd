from xunit.src import *
from xunit.src.status import TestStatus


@TestClass
class TestTestStatus(TestCase):

    @Test
    def testCreation(self) -> None:
        status = TestStatus("someTest", "passed", "-")
        assert status.name == "someTest"
        assert status.result == "passed"
        assert status.info == "-"

    @Test
    def testEquality(self) -> None:
        status1 = TestStatus("someTest", "passed", "-")
        status2 = TestStatus("someTest", "passed", "-")
        assert status1 == status2
