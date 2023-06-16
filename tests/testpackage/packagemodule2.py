from src.xunit import *


@TestClass
class TestY(TestCase):
    @Test
    def y(self) -> None:
        pass

    @Test
    def y1(self) -> None:
        raise Exception
