from src.xunit import *


@TestClass
class SomeTest(TestCase):
    @Test
    def someTest(self) -> None:
        pass


@TestClass
class SomeOtherTest(TestCase):
    @Test
    def someOtherTest(self) -> None:
        raise Exception
