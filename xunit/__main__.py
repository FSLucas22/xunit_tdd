from xunit.src import *
from xunit.src import packagemanager as pm
from xunit import tests
import colorama
import os


def main() -> None:
    if os.name == "nt":
        colorama.init()
    TestRunner(suite=NormalSuiteFactory().from_package(tests, pm.ignore_name)).run()
    if os.name == "nt":
        colorama.deinit()


if __name__ == "__main__":
    main()
