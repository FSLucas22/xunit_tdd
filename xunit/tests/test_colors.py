from xunit.src import *


@TestClass
class TestColors(TestCase):

    @Test
    def testColorFunctions(self) -> None:
        assert green("Test") == '\033[32mTest\033[0m'
        assert red("Test") == '\033[31mTest\033[0m'
