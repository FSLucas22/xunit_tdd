from ...src import *


@TestClass
class TestX(TestCase):
    @Test
    def x(self) -> None:
        pass

    @Test
    def x1(self) -> None:
        raise Exception
