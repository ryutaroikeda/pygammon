"""Command line interface."""
from pygammon.pygammon import Board
from pygammon.pygammon import Color
from pygammon.pygammon import DICE
from pygammon.pygammon import Move
from pygammon.pygammon import Player

class CommandLinePlayer(Player):
    """Command line interface."""
    def make_move(self, color: Color, board: Board, dice: DICE) -> Move:
        return Move([])
