import os
import re
from abc import ABC
from typing import List

from exceptions import InputException
from scoreboard import ScoreBoard


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
        print(f"Total points: {scoreboard.get_total()}")

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