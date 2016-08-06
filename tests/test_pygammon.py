"""Tests for backgammon engine."""
import unittest

from pygammon.pygammon import Board
from pygammon.pygammon import Color
from pygammon.pygammon import Submove

class TestColor(unittest.TestCase):
    """Tests for Color."""

    def test_opposite(self):
        """Make sure getting opposite color works."""
        self.assertEqual(Color.Black.opposite(), Color.White)

class TestBoard(unittest.TestCase):
    """Tests for Board."""

    def test_get_checkers(self):
        """Make sure we can get checkers."""
        board = Board()
        black_board = board.get_board(Color.Black)
        black_board[1] = 2
        self.assertEqual(board.get_checkers(Color.Black, 1), 2)

    def test_set_checkers(self):
        """Make sure we can set checkers."""
        board = Board()
        board.set_checkers(Color.Black, 1, 2)
        board.set_opposite_checkers(Color.Black, 3, 4)
        self.assertEqual(board.get_checkers(Color.Black, 1), 2)
        self.assertEqual(board.get_opposite_checkers(Color.Black, 3), 4)
        self.assertEqual(board.get_opposite_checkers(Color.White, 3), 0)
        self.assertEqual(board.get_checkers(
            Color.White, board.get_opposite_pos(3)), 4)

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

    def test_list_moves_high(self):
        """Make sure we return the high move when possible."""
        board = Board()
        board.set_checkers(Color.Black, 1, 1)
        board.set_opposite_checkers(Color.Black, 4, 2)
        board.set_opposite_checkers(Color.Black, 5, 2)

        moves = board.list_moves(Color.Black, [1, 2])
        self.assertEqual(len(moves), 1)
        move = moves[0]
        self.assertEqual(move.size(), 1)
        submove = move.pop()
        self.assertEqual(submove.source, 1)
        self.assertEqual(submove.die, 2)


    def test_list_moves_low(self):
        """Make sure we return the low move when possible."""
        board = Board()
        board.set_checkers(Color.Black, 1, 1)
        board.set_opposite_checkers(Color.Black, 3, 2)
        board.set_opposite_checkers(Color.Black, 4, 2)

        moves = board.list_moves(Color.Black, [1, 2])
        self.assertEqual(len(moves), 1)
        move = moves[0]
        self.assertEqual(move.size(), 1)
        submove = move.pop()
        self.assertEqual(submove.source, 1)
        self.assertEqual(submove.die, 1)

    def test_list_moves_both_dice(self):
        """Make sure we use both dice when possible."""
        board = Board()
        board.set_checkers(Color.Black, 1, 1)
        board.set_opposite_checkers(Color.Black, 3, 2)

        moves = board.list_moves(Color.Black, [1, 2])
        self.assertEqual(len(moves), 1)
        move = moves[0]
        self.assertEqual(move.size(), 2)
        first = move.pop()
        self.assertEqual(first.die, 1)
        second = move.pop()
        self.assertEqual(second.die, 2)
