import random

from exceptions import GameException
from scoreboard import ScoreBoard
from view import YahtzeeView


class Yahtzee:
    def __init__(self, view: YahtzeeView, scoreboard: ScoreBoard) -> None:
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
