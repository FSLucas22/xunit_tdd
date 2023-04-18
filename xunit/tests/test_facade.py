from xunit.src import *


@TestClass
class TestFacade(TestCase):

    @Test
    def testFacade(self) -> None:
        from xunit.tests.testclasses import MockPrint
        mock = MockPrint()
        mock("Test")
        assert mock.passed_value == "Test"
