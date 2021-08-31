from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class Rule(ABC):
    @abstractmethod
    def get_label(self) -> str:
        pass

    @abstractmethod
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