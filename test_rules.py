import unittest
from rules import *


class SingleRuleTestCase(unittest.TestCase):

    def test_single_one(self):
        dice = [1]
        self.assertEqual(1, SingleRule(1).get_score(dice))

    def test_single_six(self):
        dice = [6]
        self.assertEqual(6, SingleRule(6).get_score(dice))

    def test_sixes(self):
        dice = [6, 6, 1]
        self.assertEqual(12, SingleRule(6).get_score(dice))

    def test_get_label_aces(self):
        self.assertEqual('Aces', SingleRule(1).get_label())

    def test_get_label_sixes(self):
        self.assertEqual('6\'s', SingleRule(6).get_label())


class NOfAKindRuleTestCase(unittest.TestCase):
    def test_non_of_a_kind(self):
        dice = [1]
        self.assertEqual(0, NOfAKindRule(3).get_score(dice))

    def test_three_of_a_kind(self):
        dice = [2, 3, 4, 4, 4]
        self.assertEqual(17, NOfAKindRule(3).get_score(dice))

    def test_yathzee_as_three_of_a_kind(self):
        dice = [4, 4, 4, 4, 4]
        self.assertEqual(20, NOfAKindRule(3).get_score(dice))


class FullHouseRuleTestCase(unittest.TestCase):
    def test_empty_house(self):
        dice = [1]
        self.assertEqual(0, FulHouseRule().get_score(dice))

    def test_full_house(self):
        dice = [1, 1, 1, 2, 2]
        self.assertEqual(25, FulHouseRule().get_score(dice))


class StraightRuleTestCase(unittest.TestCase):
    def test_no_straight(self):
        dice = [1, 2, 4, 4, 5]
        self.assertEqual(0, StraightRule(3).get_score(dice))

    def test_small_straight(self):
        dice = [1, 2, 3, 3, 3]
        self.assertEqual(30, StraightRule(3).get_score(dice))

    def test_small_straight_with_large_straight_dice(self):
        dice = [1, 2, 3, 4, 3]
        self.assertEqual(30, StraightRule(3).get_score(dice))

    def test_large_straight_at_the_start(self):
        dice = [1, 2, 3, 4, 3]
        self.assertEqual(40, StraightRule(4).get_score(dice))

    def test_large_straight_at_the_end(self):
        dice = [1, 1, 2, 3, 4]
        self.assertEqual(40, StraightRule(4).get_score(dice))

    def test_large_straight_al_the_way(self):
        dice = [1, 2, 3, 4, 5]
        self.assertEqual(40, StraightRule(4).get_score(dice))


class YahtzeeRuleTestCase(unittest.TestCase):
    def test_no_yahtzee(self):
        dice = [1, 2, 3, 4, 5]
        self.assertEqual(0, YahtzeeRule().get_score(dice))

    def test_yahtzee(self):
        dice = [5, 5, 5, 5, 5]
        self.assertEqual(50, YahtzeeRule().get_score(dice))


class ChanceRuleTestCase(unittest.TestCase):
    def test_no_yahtzee(self):
        dice = [1, 2, 3, 4, 5]
        self.assertEqual(15, ChanceRule().get_score(dice))
