from xunit.src import *


@TestClass
class TestFromCommandLine(TestCase):

    @Test
    def testFindModuleByPath(self) -> None:
        from xunit.tests import testpackage as t1
        from xunit.tests import testpackage as t2
        assert t1 == t2
        module = findModule('testpackage')
        assert module == t1
