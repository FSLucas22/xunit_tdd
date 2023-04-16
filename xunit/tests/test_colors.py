from xunit.src import *


@TestClass
class TestColors(TestCase):

    @Test
    def testColorFunctions(self) -> None:
        assert green("Test") == '\033[32mTest\033[0m'
