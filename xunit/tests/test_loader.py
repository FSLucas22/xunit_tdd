from xunit.src import *
from xunit.src import loader
from xunit.tests.testclasses import *


@TestClass
class SuiteFactoryTest(TestCase):
    result: TestResult
    suite: TestSuite

    def setup(self) -> None:
        self.result = TestResult()
        self.suite = TestSuite(self.result.save_status)

    @Test
    def test_tests_from_class(self) -> None:
        self.suite.add(*loader.tests_from_class(PassedTestCase, FailedTestCase))
        self.suite.run()
  
        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "passed_test failed_test"
        assert self.result.get_results(Status.CREATED) == [TestStatus('Suite', Status.CREATED, 'Base suite')]

    @Test
    def test_suites_from_class(self) -> None:
        self.suite.add(*loader.suites_from_class(PassedTestCase))
        self.suite.run()
  
        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "passed_test"
        assert self.result.get_results(Status.CREATED) == [TestStatus('Suite', Status.CREATED, 'Base suite'),
                                                           TestStatus('Suite', Status.CREATED, 'PassedTestCase')]

    @Test
    def test_tests_from_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        self.suite.add(*loader.tests_from_module(testmodule))
        self.suite.run()

        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "someTest someOtherTest"
        assert self.result.get_results(Status.CREATED) == [TestStatus('Suite', Status.CREATED, 'Base suite')]

    @Test
    def test_suites_from_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        self.suite.add(*loader.suites_from_module(testmodule))
        self.suite.run()

        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "someTest someOtherTest"
        results = self.result.get_results(Status.CREATED)
        assert TestStatus('Suite', Status.CREATED, 'xunit.tests.testmodule') in results
        assert TestStatus('Suite', Status.CREATED, 'SomeOtherTest') in results
        assert TestStatus('Suite', Status.CREATED, 'SomeTest') in results
    
    @Test
    def test_tests_from_package(self) -> None:
        import xunit.tests.testpackage as testpackage
        self.suite.add(*loader.tests_from_package(testpackage, lambda _, __: False))
        self.suite.run()

        passed = self.result.get_names_of_status(Status.PASSED)
        failed = self.result.get_names_of_status(Status.FAILED)

        assert "x" in passed and "y" in passed and "z" in passed
        assert "x1" in failed and "y1" in failed and "z1" in failed
        assert self.result.get_results(Status.CREATED) == [TestStatus('Suite', Status.CREATED, 'Base suite')]

    @Test
    def test_suites_from_package(self) -> None:
        import xunit.tests.testpackage as testpackage
        self.suite.add(*loader.suites_from_package(testpackage, lambda _, __: False))
        self.suite.run()

        passed = self.result.get_names_of_status(Status.PASSED)
        failed = self.result.get_names_of_status(Status.FAILED)
        created = self.result.get_results(Status.CREATED)
        print(created)
        assert "x" in passed and "y" in passed and "z" in passed
        assert "x1" in failed and "y1" in failed and "z1" in failed
        assert TestStatus('Suite', Status.CREATED, testpackage.__name__) in created
        assert TestStatus('Suite', Status.CREATED, 'xunit.tests.testpackage.packagemodule') in created
        assert TestStatus('Suite', Status.CREATED, 'xunit.tests.testpackage.packagemodule2') in created
        assert TestStatus('Suite', Status.CREATED, 'xunit.tests.testpackage.subpackage') in created
        assert TestStatus('Suite', Status.CREATED, 
                          'xunit.tests.testpackage.subpackage.subpackagemodule') in created
        assert TestStatus('Suite', Status.CREATED, 'TestX') in created
        assert TestStatus('Suite', Status.CREATED, 'TestY') in created

    @Test
    def test_ignore(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackage"]
        self.suite.add(*loader.tests_from_package(testpackage, ignore=ignore))
        self.suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)

    @Test
    def test_ignore_perpetuates(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackagemodule"]
        self.suite.add(*loader.tests_from_package(testpackage, ignore=ignore))
        self.suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)
