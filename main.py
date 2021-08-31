import os
import sys

from view import ConsoleView
from yahtzee import Yahtzee

if __name__ == '__main__':
    try:
        view = ConsoleView()
        Yahtzee(view).start()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
