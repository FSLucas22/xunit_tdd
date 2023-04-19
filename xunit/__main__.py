from xunit.src import *
from xunit import tests
import colorama
import os


if __name__ == "__main__":
    if os.name == "nt":
        colorama.init()
    TestRunner().run_for_package(tests)
    if os.name == "nt":
        colorama.deinit()
