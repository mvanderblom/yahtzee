from unittest import TestCase

from exceptions import GameException
from scoreboard import ScoreBoard


class ScoreBoardTestCase(TestCase):
    def test_get_total(self):
        sb = ScoreBoard()
        sb.set_score(1, [1, 1, 1, 1, 1])
        sb.set_score(2, [2, 2, 2, 2, 2])
        self.assertEqual(15, sb.get_total())

    def test_unknown_rule_key_raises(self):
        sb = ScoreBoard()
        with self.assertRaises(GameException):
            sb.set_score(14, [1, 1, 1, 1, 1])

    def test_set_score_twice_raises(self):
        sb = ScoreBoard()
        sb.set_score(1, [1, 1, 1, 1, 1])
        with self.assertRaises(GameException):
            sb.set_score(1, [1, 1, 1, 1, 1])

    def test_is_full(self):
        sb = ScoreBoard()
        self.assertFalse(sb.is_full())

    def test_is_not_full(self):
        sb = ScoreBoard()
        self.assertFalse(sb.is_full())

    def test_is_full(self):
        sb = ScoreBoard()
        for i in range(1,14):
            sb.set_score(i, [1])
        self.assertTrue(sb.is_full())