from xunit.src import *


@TestClass
class TestPackageManager(TestCase):

    @Test
    def testPackageObjects(self) -> None:
        from xunit.tests import testpackage
        obj = PackageObject("packagemodule", testpackage.packagemodule)
        assert PackageObject("packagemodule", testpackage.packagemodule) == obj

    @Test
    def testGetPackageObjects(self) -> None:
        from xunit.tests import testpackage
        package_object = getPackageObjects(testpackage)[0]
        expected_object = PackageObject("packagemodule", testpackage.packagemodule)
        assert package_object.name == expected_object.name
        assert package_object.value == expected_object.value
