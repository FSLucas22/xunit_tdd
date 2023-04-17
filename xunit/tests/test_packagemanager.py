from xunit.src import *


@TestClass
class TestPackageManager(TestCase):

    @Test
    def testPackageObjects(self) -> None:
        from xunit.tests import testpackage
        obj = PackageObject("packagemodule", testpackage.packagemodule)
        assert PackageObject("packagemodule", testpackage.packagemodule) == obj
    
