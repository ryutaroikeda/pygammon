"""Random player."""
import random

from pygammon.pygammon import Board
from pygammon.pygammon import Color
from pygammon.pygammon import Command
from pygammon.pygammon import DICE
from pygammon.pygammon import Game
from pygammon.pygammon import Move
from pygammon.pygammon import Player
from pygammon.pygammon import RollCommand

class RandomPlayer(Player):
    """Random backgammon player."""

    def make_command(self, _color: Color, _game: Game) -> Command:
        """Parse a command from the console."""
        return RollCommand()

    def make_move(self, color: Color, board: Board, dice: DICE) -> Move:
        """Generate a random move."""
        moves = board.list_moves(color, dice)
        move_index = random.randint(0, len(moves) - 1)
        return moves[move_index]
