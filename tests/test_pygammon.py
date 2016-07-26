import unittest

from pygammon.pygammon import Board
from pygammon.pygammon import Color

class TestBoard(unittest.TestCase):

    def test_get_checkers(self):
        board = Board()
        self.assertEqual(board.get_checkers(Color.Black, 0), 0)
