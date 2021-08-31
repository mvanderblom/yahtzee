from dataclasses import dataclass
from typing import List

from exceptions import GameException
from rules import Rule


class ScoreBoard:
    rules: List[Rule] = []
    scores: List[int] = []

    def register_rules(self, rules: List[Rule]):
        self.rules = rules
        self.scores = [None] * len(rules)

    def set_score(self, rule_index, dice):
        if 0 > rule_index or rule_index >= len(self.rules):
            raise GameException(f'Unknown rule key {rule_index}')
        rule = self.rules[rule_index]

        score = self.scores[rule_index]
        if score is not None:
            raise GameException(f'Score for rule {rule.get_label()} is allready used')

        self.scores[rule_index] = rule.get_score(dice)

    def is_full(self):
        return len(list(filter(lambda score: score is None, self.scores))) == 0

    def get_total(self):
        return sum(filter(lambda score: score is not None, self.scores))