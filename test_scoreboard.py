from unittest import TestCase

from exceptions import GameException
from rules import SingleRule
from scoreboard import ScoreBoard


class ScoreBoardTestCase(TestCase):

    def setUp(self) -> None:
        self.sb = ScoreBoard()
        self.sb.register_rules([
            SingleRule(1),
            SingleRule(2)
        ])

    def test_get_total(self):
        self.sb.set_score(0, [1, 1, 1, 1, 1])
        self.sb.set_score(1, [2, 2, 2, 2, 2])
        self.assertEqual(15, self.sb.get_total())

    def test_unknown_rule_key_raises(self):
        with self.assertRaises(GameException):
            self.sb.set_score(2, [1, 1, 1, 1, 1])

    def test_set_score_twice_raises(self):
        self.sb.set_score(0, [1, 1, 1, 1, 1])
        with self.assertRaises(GameException):
            self.sb.set_score(0, [1, 1, 1, 1, 1])

    def test_is_full(self):
        self.assertFalse(self.sb.is_full())

    def test_is_not_full(self):
        self.assertFalse(self.sb.is_full())

    def test_is_full(self):
        self.sb.set_score(0, [1])
        self.sb.set_score(1, [1])
        self.assertTrue(self.sb.is_full())