from dataclasses import dataclass
from typing import List

from exceptions import GameException
from rules import SingleRule, NOfAKindRule, FulHouseRule, StraightRule, YahtzeeRule, ChanceRule


# @dataclass
class ScoreBoard:
    # rules: List[YahtzeeRule]
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
        return sum(filter(lambda score: score is not None, map(lambda val: val[1], self.rules.values())))