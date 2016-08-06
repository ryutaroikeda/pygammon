"""Random player."""
import random

from pygammon.pygammon import Board
from pygammon.pygammon import Color
from pygammon.pygammon import DICE
from pygammon.pygammon import Move

class RandomPlayer:
    """Random backgammon player."""

    def make_move(self, color: Color, board: Board, dice: DICE) -> Move:
        """Generate a random move."""
        # Use an unused variable to keep pylint happy.
        self = self
        moves = board.list_moves(color, dice)
        move_index = random.randint(0, len(moves) - 1)
        return moves[move_index]
