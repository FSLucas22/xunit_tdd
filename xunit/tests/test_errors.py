from xunit.src import *


@TestClass
class TestErrors(TestCase):

    @Test
    def testErrorInfo(self) -> None:
        try:
            raise Exception
        except Exception as e:
            info = TestErrorInfo(e)
            assert info.line_number == 10
