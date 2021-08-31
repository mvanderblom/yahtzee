import sys
import os
import random
import re
from rules import *


class Hand:

    def __init__(self):
        self.dice = [0 for i in range(0, 5)]

    def roll(self):
        self.dice = [random.randint(1, 6) for i in range(0, 5)]

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
                    self.dice[i - 1] = random.randint(1, 6)
                print(self.dice)
                rolls += 1


class GameException(Exception):
    pass


class InputException(Exception):
    pass


class ScoreBoard(object):

    def __init__(self):
        self.rules = {
            1: (SingleRule(1), None),
            2: (SingleRule(2), None),
            3: (SingleRule(3), None),
            4: (SingleRule(4), None),
            5: (SingleRule(5), None),
            6: (SingleRule(6), None),
            7: (NOfAKindRule(3), None),
            8: (NOfAKindRule(4), None),
            9: (FulHouseRule(), None),
            10: (StraightRule(3), None),
            11: (StraightRule(4), None),
            12: (YahtzeeRule(), None),
            13: (ChanceRule(), None),
        }

    def set_score(self, rule_key, dice):
        if rule_key not in self.rules.keys():
            raise GameException(f'Unknown rule key {rule_key}')

        rule, score = self.rules[rule_key]
        if score is not None:
            raise GameException(f'Score for rule {rule.get_label()} allready saved')

        self.rules[rule_key] = (rule, rule.get_score(dice))

    def is_full(self):
        return len(list(filter(lambda val: val[1] is None, self.rules.values()))) == 0

    def get_total(self):
        return sum(filter(lambda  val: val[1] is not None, map(lambda _, score: score, self.rules.values())))


class ConsoleGame:

    def __init__(self, hand=Hand(), scoreboard=ScoreBoard()) -> None:
        self.hand = hand
        self.scoreboard = scoreboard

    def start(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
                    YAHTZEE

                    Welcome to the game. To begin, simply press [Enter]
                    and follow the instructions on the screen.

                    To exit, press [Ctrl+C]
                    """)

        self.main_loop()

        print("\nCongratulations! You finished the game!\n")
        print(f"Total points: {self.scoreboard.get_total()}")

    def main_loop(self):
        while not self.scoreboard.is_full():
            self.rol_dice()
            self.hand.re_roll()
            self.show_scoreboard()
            self.select_scoring_rule(self.hand.dice)
            self.show_scoreboard()

            input("\nPress any key to continue")
            os.system('cls' if os.name == 'nt' else 'clear')

    def rol_dice(self):
        print("Rolling the dice...")
        self.hand.roll()
        print(self.hand.dice)

    def select_scoring_rule(self, dice):
        while True:
            try:
                row_number = self._get_int_input("Choose which rule to use (leave empty to show available rules): ", 1, len(self.scoreboard.rules))
            except InputException as exception:
                print(exception)
                continue

            try:
                self.scoreboard.set_score(row_number, dice)
                break
            except GameException as exception:
                print(exception)

    def show_scoreboard(self):
        print("\nSCOREBOARD")
        print("===================================")
        for idx, row in self.scoreboard.rules.items():
            try:
                print("{:<2} {:<21}| {:2} points".format(idx,
                                                         row[0].get_label(),
                                                         row[1] if row[1] is not None else ""))
            except KeyError:
                print("{:<2} {:<21}|".format(idx, row.get_label()))
        print("===================================")

    @staticmethod
    def _get_int_input(message: str, lower_bound: int = None, upper_bound: int = None):
        user_value = input(message)

        if user_value.strip() == "":
            raise InputException("No value provided")

        try:
            user_value = int(user_value)
        except ValueError:
            raise InputException("You entered something other than a number.")

        if lower_bound is not None and user_value < lower_bound:
            raise InputException(f"Value should be higher than {lower_bound}")

        if upper_bound is not None and user_value > upper_bound:
            raise InputException(f"Value should be lower than {upper_bound}")

        return user_value


if __name__ == '__main__':
    try:
        ConsoleGame().start()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
