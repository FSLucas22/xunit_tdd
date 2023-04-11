from typing import Type, Self
from xunit.src.testcase import TestCase
from xunit.src.testresult import TestResult


class TestSuite:
    tests: list[TestCase]

    def __init__(self) -> None:
        self.tests = []
        
    def add(self, test: TestCase) -> None:
        self.tests.append(test)

    def run(self, result: TestResult) -> None:
        for test in self.tests:
            test.run(result)

    @classmethod
    def fromTestCase(cls, *tests: Type[TestCase]) -> Self:
        suite = cls()
        for testCase in tests:
            for testName in testCase.testNames.split():
                suite.add(testCase(testName))
        return suite
