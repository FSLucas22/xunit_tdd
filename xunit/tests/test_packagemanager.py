from xunit.src import *


@TestClass
class TestPackageManager(TestCase):

    @Test
    def testPackageObjects(self) -> None:
        from xunit.tests.testpackage import packagemodule
        obj = PackageObject("packagemodule", packagemodule)
        assert PackageObject("packagemodule", packagemodule) == obj

    @Test
    def testGetPackageObjects(self) -> None:
        from xunit.tests import testpackage
        from xunit.tests.testpackage import packagemodule, packagemodule2
        package_objects = getPackageObjects(testpackage)
        expected_object1 = PackageObject("packagemodule", packagemodule)
        expected_object2 = PackageObject("packagemodule2", packagemodule2)
        assert expected_object1 in package_objects
        assert expected_object2 in package_objects
        assert len(getPackageObjects(testpackage)) == 2
