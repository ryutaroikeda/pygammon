"""Tests for backgammon engine."""
import unittest

from pygammon.pygammon import Board
from pygammon.pygammon import Color
from pygammon.pygammon import Submove

class TestBoard(unittest.TestCase):
    """Tests for Board."""

    def test_get_checkers(self):
        """Make sure we can get checkers."""
        board = Board()
        black_board = board.get_board(Color.Black)
        black_board[1] = 2
        self.assertEqual(board.get_checkers(Color.Black, 1), 2)

    def test_is_valid_submove(self):
        """Make sure legal moves are legal."""
        board = Board()
        black_board = board.get_board(Color.Black)
        black_board[1] = 1
        submove = Submove({'source': 1, 'die': 1})
        self.assertEqual(submove.destination(), 2)
        self.assertTrue(board.is_valid_submove(Color.Black, submove))

    def test_list_moves(self):
        """Make sure we return moves in both orders."""
        board = Board()
        black_board = board.get_board(Color.Black)
        black_board[1] = 1
        moves = board.list_moves(Color.Black, [1, 2])
        self.assertEqual(len(moves), 2)

    def test_list_moves_with_double(self):
        """Make sure we return moves for a double."""
        board = Board()
        black_board = board.get_board(Color.Black)
        black_board[1] = 1
        moves = board.list_moves(Color.Black, [1, 1])
        self.assertEqual(len(moves), 1)
        move = moves[0]
        self.assertEqual(move.size(), 4)
