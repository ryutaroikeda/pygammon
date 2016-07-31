"""This module provides an engine for backgammon."""

from enum import Enum
import sys

import numpy as np

class Color(Enum):
    """Represent the colors of players."""

    Black = 0
    White = 1

    def opposite(self) -> 'Color':
        """Get the opponent's color."""
        if Color.Black == self.value:
            return Color.White
        else:
            return Color.Black

class Submove:
    """Represent each movement in a move."""

    def __init__(self) -> None:
        self.source = 0
        self.die = 0

    def destination(self) -> int:
        """This is where the checker moves to."""
        dst = self.source + self.die
        if Board.BEARING_OFF_POS < dst:
            dst = Board.BEARING_OFF_POS
        return dst

class Board:
    """Represent the game state."""

    BOARD_SIZE = 26
    BAR_POS = 0
    HOME_POS = 18
    BEARING_OFF_POS = 25

    def __init__(self) -> None:
        self.black_board = np.zeros(Board.BOARD_SIZE, dtype=int)
        self.white_board = np.zeros(Board.BOARD_SIZE, dtype=int)

    def get_board(self, color: Color) -> np.ndarray:
        """Get a board reference."""
        if Color.Black == color:
            return self.black_board
        else:
            return self.white_board

    def get_checkers(self, color: Color, pos: int) -> bool:
        """Get the number of checkers."""
        board = self.get_board(color)
        if Color.White == color:
            pos = Board.BOARD_SIZE - pos
        return board[pos]

    def is_blocked(self, color: Color, pos: int) -> bool:
        """Check if the point is blocked by the opponent."""
        if Board.BEARING_OFF_POS == pos:
            return False
        checkers = self.get_checkers(color.opposite(), pos)
        return 1 < checkers

    def is_all_home(self, color: Color) -> bool:
        """Check if we can start bearing off."""
        board = self.get_board(color)
        for pos in range(Board.BAR_POS, Board.HOME_POS):
            if 0 < board[pos]:
                return False
        return True

    def is_highest_home_point(self, color: Color, test_pos: int) -> bool:
        """Check this is the furthest from bearing off among home points."""
        for pos in range(Board.HOME_POS, test_pos):
            if 0 < self.get_checkers(color, pos):
                return False
        return True

    def is_valid_submove(self, color: Color, submove: Submove) -> bool:
        """Check if the submove is legal."""
        # Make sure there is a checker to move.
        if self.get_checkers(color, submove.source) < 1:
            return False
        # Make sure the destination is not blocked.
        if self.is_blocked(color, submove.source):
            return False
        # Make sure the bar is empty or we're getting out the bar.
        if (0 < self.get_checkers(color, submove.source)) and \
                (Board.BAR_POS != submove.source):
            return False
        # We're bearing off a checker.
        if Board.BEARING_OFF_POS == submove.destination:
            # Make sure everyone is home.
            if not self.is_all_home(color):
                return False
            # If there's no checker on the point rolled, make sure we're
            # bearing off from the highest point.
            if (submove.source + submove.die != Board.BEARING_OFF_POS) and \
                    (not self.is_highest_home_point(color, submove.source)):
                return False
        return True

    def do_submove(self, color: Color, submove: Submove) -> None:
        """Move checkers according to the submove."""
        board = self.get_board(color)
        # Move the checker
        destination = submove.destination()
        board[submove.source] -= 1
        board[destination] += 1
        # If we're hitting a blot, send it to the bar.
        # But don't hit anything in the opponent's bar.
        if (Board.BEARING_OFF_POS != destination) and \
                (1 == self.get_checkers(color.opposite(), destination)):
            other_board = self.get_board(color.opposite())
            other_board[Board.BAR_POS] += 1
            other_board[Board.BOARD_SIZE - destination] = 0

    def print_checker(self, pos: int) -> None:
        """Print a point."""
        black_checkers = self.get_checkers(Color.Black, pos)
        white_checkers = self.get_checkers(Color.White, pos)
        if 0 < black_checkers:
            sys.stdout.write('B{:<2} '.format(black_checkers))
        elif 0 < white_checkers:
            sys.stdout.write('W{:<2} '.format(white_checkers))
        else:
            sys.stdout.write(' __ ')

    def print(self) -> None:
        """Print the board."""
        for pos in range(13, 19):
            sys.stdout.write(' {:>2} '.format(pos))
        sys.stdout.write('    ')
        for pos in range(19, 25):
            sys.stdout.write(' {:>2} '.format(pos))
        sys.stdout.write('    ')
        sys.stdout.write('Black bar: {}'.format(self.get_checkers(
            Color.Black, Board.BAR_POS)))
        sys.stdout.write('\n')
        for pos in range(13, 19):
            self.print_checker(pos)
        sys.stdout.write('    ')
        for pos in range(19, 25):
            self.print_checker(pos)
