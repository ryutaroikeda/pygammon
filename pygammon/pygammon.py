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

class Board:

    BOARD_SIZE = 26
    BAR_POS = 0
    AWAY_POS = 18
    BEARED_OFF_POS = 25

    def __init__(self) -> None:
        self.black_board = np.zeros(self.BOARD_SIZE, dtype=int)
        self.white_board = np.zeros(self.BOARD_SIZE, dtype=int)

    def get_board(self, color: Color):
        if Color.Black == color:
            return self.black_board
        else:
            return self.white_board
            
    def get_checkers(self, color: Color, pos: int) -> bool:
        board = self.get_board(color)
        if Color.White == color:
            pos = self.BOARD_SIZE - pos
        return board[pos]

    def is_blocked(self, color: Color, pos: int) -> bool:
        checkers = self.get_checkers(color.opposite(), pos)
        return 1 < checkers

    def is_all_home(self, color: Color) -> bool:
        for pos in range(self.BAR_POS, self.AWAY_POS):
            if 0 < self.get_checkers(color, pos):
                return False
        return True

    def is_valid_submove(self, color: Color, submove: Submove) -> bool:
        if self.get_checkers(color, submove.source) < 1:
            return False

        return True
