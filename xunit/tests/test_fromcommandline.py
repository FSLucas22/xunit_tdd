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

        result1 = TestResult()
        result2 = TestResult()
        suite1 = TestSuite.fromPackage(testpackage)
        suite2 = TestSuite.fromPackage(module)
        suite1.run(result1)
        suite2.run(result2)
        assert result1.getAllPassed() == result2.getAllPassed()
        assert result1.getAllFailed() == result2.getAllFailed()
        assert result1.getAllNotCompleted() == result2.getAllNotCompleted()
