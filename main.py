import os
import sys

from rules import SingleRule, NOfAKindRule, FulHouseRule, StraightRule, YahtzeeRule, ChanceRule
from scoreboard import ScoreBoard
from view import ConsoleView
from yahtzee import Yahtzee

if __name__ == '__main__':
    try:
        view = ConsoleView()
        scoreboard = ScoreBoard()
        scoreboard.register_rules([
            SingleRule(1),
            SingleRule(2),
            SingleRule(3),
            SingleRule(4),
            SingleRule(5),
            SingleRule(6),
            NOfAKindRule(3),
            NOfAKindRule(4),
            FulHouseRule(),
            StraightRule(3),
            StraightRule(4),
            YahtzeeRule(),
            ChanceRule(),
        ])

        Yahtzee(view).start()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
