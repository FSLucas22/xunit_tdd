from xunit.src import *
import colorama


@TestClass
class TestColors(TestCase):

    @Test
    def testColorFunctions(self) -> None:
        color = Green(os="nt")
        assert colorama.Fore.GREEN + "Test" + colorama.Style.RESET_ALL == color("Test")
