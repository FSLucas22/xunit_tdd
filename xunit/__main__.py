from xunit.src import *
from xunit import tests
import colorama
import os


def main() -> None:
    TestRunner().runForPackage(tests)
    

if __name__ == "__main__":
    if os.name == "nt":
        colorama.init()
    main()
    if os.name == "nt":
        colorama.deinit()
