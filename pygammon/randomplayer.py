"""Random player."""
import random

from pygammon.pygammon import Color
from pygammon.pygammon import Command
from pygammon.pygammon import DICE
from pygammon.pygammon import Game
from pygammon.pygammon import Move
from pygammon.pygammon import Player
from pygammon.pygammon import ResignCommand
from pygammon.pygammon import RollCommand

class RandomPlayer(Player):
    """Random backgammon player."""

    def roll_or_double(self, _color: Color, _game: Game) -> Command:
        """Parse a command from the console."""
        return RollCommand()

    def make_move(self, color: Color, game: Game, dice: DICE) -> Move:
        """Generate a random move."""
        board = game.board
        moves = board.list_moves(color, dice)
        move_index = random.randint(0, len(moves) - 1)
        return moves[move_index]

    def accept_or_resign(self, _color: Color, _game: Game) -> Command:
        """Resign."""
        return ResignCommand()
