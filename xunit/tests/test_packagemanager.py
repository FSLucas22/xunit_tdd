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
        from xunit.tests.testpackage import packagemodule
        package_object = getPackageObjects(testpackage)[0]
        expected_object = PackageObject("packagemodule", testpackage.packagemodule)
        assert package_object.name == expected_object.name
        assert package_object.value == expected_object.value
        assert len(getPackageObjects(testpackage)) == 1
