from xunit.src import *
from xunit.src import packagemanager as pm
from xunit.src import loader
from xunit import tests
import colorama
import os


def main() -> None:
    if os.name == "nt":
        colorama.init()
    suite = TestSuite()
    suite.add(*loader.tests_from_package(tests, pm.ignore_name))
    TestRunner(suite=suite).run()
    if os.name == "nt":
        colorama.deinit()


if __name__ == "__main__":
    main()
