from src.xunit import *


@TestClass
class TestColors(TestCase):

    @Test
    def test_color_functions(self) -> None:
        assert color.green("Test") == '\033[32mTest\033[0m'
        assert color.red("Test") == '\033[31mTest\033[0m'
        assert color.yellow("Test") == '\033[33mTest\033[0m'
