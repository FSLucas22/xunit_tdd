from xunit.src import *
from xunit.src.packagemanager import *


@TestClass
class TestPackageManager(TestCase):

    @Test
    def test_package_objects(self) -> None:
        from xunit.tests.testpackage import packagemodule
        obj = PackageObject("packagemodule", packagemodule)
        assert PackageObject("packagemodule", packagemodule) == obj

    @Test
    def test_get_package_objects(self) -> None:
        from xunit.tests import testpackage
        from xunit.tests.testpackage import (
            packagemodule, packagemodule2, subpackage
        )
        package_objects = get_package_objects(testpackage)
        expected_object1 = PackageObject("packagemodule", packagemodule)
        expected_object2 = PackageObject("packagemodule2", packagemodule2)
        expected_object3 = PackageObject("subpackage", subpackage, True)
        assert expected_object1 in package_objects
        assert expected_object2 in package_objects
        assert expected_object3 in package_objects
        assert len(package_objects) == 3

    @Test
    def test_get_package_objects_ignore(self) -> None:
        from xunit.tests import testpackage
        from xunit.tests.testpackage import packagemodule2
        expected_object = PackageObject("packagemodule2", packagemodule2)
        package_objects = get_package_objects(
            testpackage,
            ignore=lambda obj, _: obj.name in ["packagemodule","subpackage"]
        )
        assert len(package_objects) == 1
        assert expected_object == package_objects[0]

    @Test
    def test_get_ignore_file_content(self) -> None:
        from xunit.tests import testpackage
        from xunit.tests.testpackage import subpackage
        assert get_ignore_file_content(testpackage) == []
        assert get_ignore_file_content(subpackage) == ["subpackagemodule",
                                                    "subpackagemodule2"]

    @Test
    def test_ignore_name(self) -> None:
        from xunit.tests.testpackage import subpackage
        from xunit.tests.testpackage.subpackage import subpackagemodule
        assert ignore_name(
            PackageObject("subpackagemodule", subpackagemodule),
            subpackage
        )
        from xunit.tests import testpackage
        from xunit.tests.testpackage import packagemodule
        assert not ignore_name(
            PackageObject("packagemodule", packagemodule),
            testpackage
        )

    @Test
    def test_find_module_by_path(self) -> None:
        from xunit.tests import testpackage
        module = find_module(
            testpackage.__name__, testpackage.__file__
        )
        assert module.__name__ == testpackage.__name__
        assert module.__file__ == testpackage.__file__

        result1 = TestResult()
        result2 = TestResult()
        suite1 = TestSuite.from_package(testpackage)
        suite2 = TestSuite.from_package(module)
        suite1.run(result1)
        suite2.run(result2)
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.not_completed == result2.not_completed

    @Test
    def test_can_create_module_path(self) -> None:
        path_for_package = get_path("package", "p\\x\\z", is_package=True)
        path_for_module = get_path("module.py", "p\\x\\z", is_package=False)
        assert "p\\x\\z\\package\\__init__.py" == path_for_package
        assert "p\\x\\z\\module.py" == path_for_module
        
        
