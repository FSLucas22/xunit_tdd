from xunit.src import *


@TestClass
class TestColors(TestCase):

    @Test
    def testColorFunctions(self) -> None:
        assert color.green("Test") == '\033[32mTest\033[0m'
        assert color.red("Test") == '\033[31mTest\033[0m'
        assert color.yellow("Test") == '\033[33mTest\033[0m'
