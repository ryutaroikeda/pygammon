"""Tests for command line player."""
import unittest

from pygammon.commandlineplayer import CommandLinePlayer
from pygammon.pygammon import Board
from pygammon.pygammon import Color
from pygammon.pygammon import Game
from pygammon.pygammon import Move

class TestCommandLinePlayer(unittest.TestCase):
    """Tests for CommandLinePlayer."""

    def test_bear_off_last_checker(self):
        """Test we can bear off last checker."""
        board = Board()
        board.set_checkers(Color.White, 24, 1)
        game = Game(board)

        player = CommandLinePlayer()
        feed = '1/0'
        dice = [1, 2]

        move = player.parse_command(feed, Color.White, game, dice)
        # mypy doesn't understand this.
        self.assertTrue(isinstance(move, Move))
        # make mypy happy
        if isinstance(move, Move):
            self.assertTrue(board.is_valid_move(Color.White, dice, move))
