from xunit.src import *
from os.path import dirname


@TestClass
class TestFromCommandLine(TestCase):

    @Test
    def testFindModuleByPath(self) -> None:
        from xunit.tests import testpackage
        module = findModule(
            testpackage.__name__, testpackage.__file__
        )
        assert module.__name__ == testpackage.__name__
        assert module.__file__ == testpackage.__file__
        
