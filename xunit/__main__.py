from .src import *
from .src import loader
from . import tests
import colorama
import os


def main() -> None:
    if os.name == "nt":
        colorama.init()
    suite = loader.load(TestSuite(), loader.suites_from_package(tests))
    TestRunner(runnable=suite).run()
    if os.name == "nt":
        colorama.deinit()


if __name__ == "__main__":
    main()
