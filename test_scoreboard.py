from unittest import TestCase

from scoreboard import ScoreBoard


class ScoreBoardTestCase(TestCase):
    def test_get_total(self):
        sb = ScoreBoard()
        sb.set_score(1, [1, 1, 1, 1, 1])
        self.assertEqual(5, sb.get_total())
