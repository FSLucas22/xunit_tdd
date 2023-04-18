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
        from xunit.tests.testpackage import (
            packagemodule, packagemodule2, subpackage
        )
        package_objects = getPackageObjects(testpackage)
        expected_object1 = PackageObject("packagemodule", packagemodule)
        expected_object2 = PackageObject("packagemodule2", packagemodule2)
        expected_object3 = PackageObject("subpackage", subpackage, True)
        assert expected_object1 in package_objects
        assert expected_object2 in package_objects
        assert expected_object3 in package_objects
        assert len(package_objects) == 3

    @Test
    def testGetPackageObjectsIgnore(self) -> None:
        from xunit.tests import testpackage
        from xunit.tests.testpackage import packagemodule2
        expected_object = PackageObject("packagemodule2", packagemodule2)
        package_objects = getPackageObjects(
            testpackage,
            ignore=lambda obj: obj.name in ["packagemodule","subpackage"]
        )
        assert len(package_objects) == 1
        assert expected_object == package_objects[0]

    @Test
    def getIgnoreFile(self) -> None:
        from xunit.tests import testpackage
        assert getIgnoreFile(testpackage) is None
        
