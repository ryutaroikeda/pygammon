from enum import Enum

import numpy as np

class Color(Enum):

    Black = 0
    White = 1

    def opposite(self) -> Color:
        if Color.Black == self.value:
            return Color.White
        else:
            return Color.Black

class Submove:

    def __init__(self) -> None:
        self.source = 0
        self.die = 0

    def destination(self) -> int:
        dst = self.source + self.die
        if Board.BEARING_OFF_POS < dst:
            dst = Board.BEARING_OFF_POS
        return dst

class Board:

    BOARD_SIZE = 26
    BAR_POS = 0
    AWAY_POS = 18
    BEARING_OFF_POS = 25

    def __init__(self) -> None:
        self.black_board = np.zeros(Board.BOARD_SIZE, dtype=int)
        self.white_board = np.zeros(Board.BOARD_SIZE, dtype=int)

    def get_board(self, color: Color):
        if Color.Black == color:
            return self.black_board
        else:
            return self.white_board

    def get_checkers(self, color: Color, pos: int) -> bool:
        board = self.get_board(color)
        if Color.White == color:
            pos = Board.BOARD_SIZE - pos
        return board[pos]

    def is_blocked(self, color: Color, pos: int) -> bool:
        if Board.BEARING_OFF_POS == pos:
            return False
        checkers = self.get_checkers(color.opposite(), pos)
        return 1 < checkers

    def is_all_home(self, color: Color) -> bool:
        for pos in range(Board.BAR_POS, Board.AWAY_POS):
            if 0 < self.get_checkers(color, pos):
                return False
        return True

    def is_valid_submove(self, color: Color, submove: Submove) -> bool:
        # Make sure there is a checker to move.
        if self.get_checkers(color, submove.source) < 1:
            return False
        # Make sure the destination is not blocked.
        if self.is_blocked(color, submove.source):
            return False
        # Make sure the bar is empty or we're moving from the bar.
        if (0 < self.get_checkers(color, submove.source)) and \
                (Board.BAR_POS != submove.source):
            return False
        # Make sure everyone is home if bearing off.
        if (Board.BEARING_OFF_POS == submove.destination) and \
                (not self.is_all_home(color)):
            return False
        return True
