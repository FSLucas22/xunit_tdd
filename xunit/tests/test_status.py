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
