from src.xunit import *


@TestClass
class TestZ(TestCase):
    
    @Test
    def z(self) -> None:
        pass

    @Test
    def z1(self) -> None:
        raise Exception
