import sys
import os
import random
import re

from rules import *


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
            raise GameException(f'Score for rule {rule.get_label()} is allready used')

        self.rules[rule_key] = (rule, rule.get_score(dice))

    def is_full(self):
        return len(list(filter(lambda val: val[1] is None, self.rules.values()))) == 0

    def get_total(self):
        return sum(filter(lambda val: val[1] is not None, map(lambda _, score: score, self.rules.values())))


class YahtzeeView(ABC):

    def show_start_message(self) -> None:
        pass

    def show_dice_roll(self, dice: List[int], roll_num: int) -> None:
        pass

    def show_score_board(self, scoreboard: ScoreBoard) -> None:
        pass

    def show_end_message(self, scoreboard: ScoreBoard) -> None:
        pass

    def show_after_turn(self, scoreboard: ScoreBoard) -> None:
        pass

    def get_re_roll_dice_nums(self) -> List[int]:
        pass

    def get_score_rule_num(self, dice: List[int], scoreboard: ScoreBoard) -> int:
        pass


class ConsoleView(YahtzeeView):

    def show_start_message(self):
        print("YAHTZEE")
        print("\nWelcome to the game. To begin, simply press [Enter]")
        print("and follow the instructions on the screen.\n")
        input()

    def show_dice_roll(self, dice, roll_num):
        print(f"Rolling the dice for the {self._display_roll_num(roll_num)} time ...")
        print(dice)

    def show_score_board(self, scoreboard):
        print("SCOREBOARD")
        print("===================================")
        for idx, row in scoreboard.rules.items():
            try:
                print("{:<2} {:<21}| {:2} points".format(idx,
                                                         row[0].get_label(),
                                                         row[1] if row[1] is not None else ""))
            except KeyError:
                print("{:<2} {:<21}|".format(idx, row.get_label()))
        print("===================================")

    def show_after_turn(self, scoreboard):
        input("Turn finished, Press any key to continue")
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_end_message(self, scoreboard):
        print("Congratulations! You finished the game!")
        print(f"Total points: {self.scoreboard.get_total()}")

    def get_re_roll_dice_nums(self) -> List[int]:
        while True:
            user_value = input("\nChoose which dice to re-roll (123 or '*' for all), or enter to continue: ")

            if user_value == "*":
                return list(range(1, 6))

            if user_value == "":
                return None

            if not re.search('^[1-5]{0,5}$', user_value):
                print(f"Invalid vaule '{user_value}' provided. Try again!")
                continue

            break

        return list(map(int, user_value))

    def get_score_rule_num(self, dice: List[int], scoreboard: ScoreBoard) -> int:
        print(dice)
        while True:
            try:
                return self._get_int_input("Choose which rule to use: ", 1, len(scoreboard.rules))
            except InputException as exception:
                print(exception)
                continue

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

    @staticmethod
    def _display_roll_num(roll_num):
        if roll_num == 1:
            return "first"
        elif roll_num == 2:
            return "second"
        elif roll_num == 3:
            return "third"
        return f"{roll_num}th"


class YahtzeeGame:
    def __init__(self, view: YahtzeeView, scoreboard=ScoreBoard()) -> None:
        self.dice = [0 for i in range(0, 5)]
        self.view = view
        self.scoreboard = scoreboard

    def start(self):
        self.view.show_start_message()

        while not self.scoreboard.is_full():
            self._handle_turn()

        self.view.show_end_message(self.scoreboard)

    def _handle_turn(self):
        roll_num = 1
        dice_nums_to_roll = range(1, 6)
        while roll_num <= 3:
            self._rol_dice(dice_nums_to_roll)
            self.view.show_dice_roll(self.dice, roll_num)

            dice_nums_to_roll = self.view.get_re_roll_dice_nums()
            if not dice_nums_to_roll:
                break
            roll_num += 1

        self._record_score()

        self.view.show_after_turn(self.scoreboard)

    def _record_score(self):
        self.view.show_score_board(self.scoreboard)
        while True:
            score_num = self.view.get_score_rule_num(self.dice, self.scoreboard)
            try:
                self.scoreboard.set_score(score_num, self.dice)
                break
            except GameException as exception:
                print(exception)

        self.view.show_score_board(self.scoreboard)

    def _rol_dice(self, die_nums_to_roll):
        for die_num in die_nums_to_roll:
            self.dice[die_num - 1] = random.randint(1, 6)


if __name__ == '__main__':
    try:
        YahtzeeGame(ConsoleView()).start()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
