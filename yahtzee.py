import abc
import sys
import os
import random
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Die:
    value: int = None

    def roll(self):
        self.value = random.randint(1, 6)

    def clear(self):
        self.value = None

    def __str__(self):
        return f"Value: {self.value}"


class Hand:

    def __init__(self):
        self.dice = [Die() for i in range(0, 5)]

    def throw(self):
        for die in self.dice:
            die.roll()

    def clear(self):
        for die in self.dice:
            die.clear()

    def re_roll(self):
        rolls = 0
        while rolls < 2:
            try:
                reroll = input("\nChoose which dice to re-roll "
                               "(comma-separated or 'all'), or 0 to continue: ")

                if reroll.lower() == "all":
                    reroll = list(range(1, 6))
                else:
                    # Perform some clean-up of input
                    reroll = reroll.replace(" ", "")  # Remove spaces
                    reroll = re.sub('[^0-9,]', '', reroll)  # Remove non-numerals
                    reroll = reroll.split(",")  # Turn string into list
                    reroll = list(map(int, reroll))  # Turn strings in list to int
            except ValueError:
                print("You entered something other than a number.")
                print("Please try again")
                continue

            if [x for x in reroll if x > len(self.dice)]:
                print("You only have 5 dice!")
                continue

            if not reroll or 0 in reroll:
                break
            else:
                for i in reroll:
                    self.dice[i - 1].roll()
                print(self.dice)
                rolls += 1


class Rule(abc.ABC):
    @abc.abstractmethod
    def get_label(self) -> str:
        pass

    @abc.abstractmethod
    def get_score(self, dice: List[int]):
        pass

@dataclass
class SingleRule(Rule):
    value: int

    def get_label(self) -> str:
        return 'Aces' if self.value == 1 else f'{self.value}\'s'

    def get_score(self, dice: List[int]):
        return sum(filter(lambda die: die == self.value, dice))

@dataclass
class NOfAKindRule(Rule):
    value: int

    def get_label(self) -> str:
        return f'{self.value} of a kind'

    def get_score(self, dice: List[int]):
        for i in dice:
            if dice.count(i) >= 3:
                return sum(dice)
        return 0


class FulHouseRule(Rule):

    def get_label(self) -> str:
        return 'Full House'

    def get_score(self, dice: List[int]):
        count = {i: 0 for i in range(1, 7)}
        for die in dice:
            count[die] += 1

        counts = count.values()
        return 25 if 2 in counts and 3 in counts else 0

@dataclass
class StraightRule(Rule):
    length: int

    def get_label(self) -> str:
        labels = {
            3: "Small Straight",
            4: "Large Straight"
        }
        return labels[self.length] if self.length in labels else f"Anything-can-happen-Straight of length {self.length}"

    def get_score(self, dice: List[int]):
        sorted_die_values = sorted(set(dice))

        last_val = sorted_die_values[0]
        count = 1
        for val in sorted_die_values[1:]:
            if last_val is val - 1:
                count += 1

                if count >= self.length:
                    return self.length * 10
            else:
                count = 1
            last_val = val

        return 0


class YahtzeeRule(Rule):

    def get_label(self) -> str:
        return "Yahtzee"

    def get_score(self, dice: List[int]):
        if len(set(dice)) == 1:
            return 50
        return 0


class ChanceRule(Rule):

    def get_label(self) -> str:
        return "Chance"

    def get_score(self, dice: List[int]):
        return sum(dice)


scoreboard_rows = {
            1: SingleRule(1),
            2: SingleRule(2),
            3: SingleRule(3),
            4: SingleRule(4),
            5: SingleRule(5),
            6: SingleRule(6),
            7: NOfAKindRule(3),
            8: NOfAKindRule(4),
            9: FulHouseRule(),
            10: StraightRule(3),
            11: StraightRule(4),
            12: YahtzeeRule(),
            13: ChanceRule(),
        }

class ScoreBoard(object):

    def __init__(self):
        self._scoreboard_points = {}

    def set_scoreboard_row_value(self, row, value):
        if row not in scoreboard_rows.keys():
            print("Bad row index")
            return False

        if row in self._scoreboard_points.keys():
            print("ScoreBoard already saved!")
            return False

        print("Adding {} points to {}".format(
            value,
            scoreboard_rows[int(row)])
        )
        self._scoreboard_points[row] = value
        return True

    def get_scoreboard_points(self):
        return self._scoreboard_points

    def show_scoreboard_rows(self):
        for key, val in scoreboard_rows.items():
            print("{}. {}".format(key, val.get_label()))

    def show_scoreboard_points(self):
        print("\nSCOREBOARD")
        print("===================================")
        for idx, row in scoreboard_rows.items():
            try:
                print("{:<2} {:<21}| {:2} points".format(idx,
                                                         row.get_label(),
                                                         self._scoreboard_points[idx]))
            except KeyError:
                print("{:<2} {:<21}|".format(idx, row.get_label()))
        print("===================================")

    def select_scoring(self, hand):
        msg = "Choose which scoring to use  (leave empty to show available rows): "

        scoreboard_row = False
        score_saved = False
        while not scoreboard_row and not score_saved:
            scoreboard_row = input(msg)

            if scoreboard_row.strip() == "":
                self.show_scoreboard_points()
                scoreboard_row = False
                continue

            try:
                scoreboard_row = int(re.sub('[^0-9,]', '', scoreboard_row))
            except ValueError:
                print("You entered something other than a number.")
                print("Please try again")
                scoreboard_row = False
                continue

            if scoreboard_row > len(scoreboard_rows):
                print("Please select an existing scoring rule.")
                scoreboard_row = False
                continue

            score_saved = self.set_scoreboard_row_value(
                int(scoreboard_row),
                scoreboard_rows[int(scoreboard_row)].get_score(map(lambda die: die.value, hand.dice))
            )


def main():
    hand = Hand()
    scoreboard = ScoreBoard()

    # We keep going until the scoreboard is full
    while len(scoreboard.get_scoreboard_points()) < len(scoreboard_rows):
        hand.throw()
        print(hand.dice)
        hand.re_roll()
        scoreboard.select_scoring(hand)
        scoreboard.show_scoreboard_points()

        input("\nPress any key to continue")
        os.system('cls' if os.name == 'nt' else 'clear')

    print("\nCongratulations! You finished the game!\n")
    scoreboard.show_scoreboard_points()
    print("Total points: {}".format(sum(scoreboard.get_scoreboard_points().values())))


if __name__ == '__main__':
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
        YAHTZEE

        Welcome to the game. To begin, simply press [Enter]
        and follow the instructions on the screen.

        To exit, press [Ctrl+C]
        """)
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
