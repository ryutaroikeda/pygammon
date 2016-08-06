"""An engine for backgammon."""

from abc import ABCMeta
from abc import abstractmethod
import copy
from enum import Enum
from typing import List
from typing import Union
import sys

import numpy as np

DICE = List[int]

class Error:
    """Represent errors."""

class Color(Enum):
    """Represent the colors of players."""

    Black = 0
    White = 1

    def opposite(self) -> 'Color':
        """Get the opponent's color."""
        if Color.Black == self:
            return Color.White
        else:
            return Color.Black

class Submove:
    """Represent each movement in a move."""

    def __init__(self, source: int, die: int) -> None:
        self.source = source
        self.die = die

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Submove):
            return False
        return self.source == other.source and self.die == other.die

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def destination(self) -> int:
        """This is where the checker moves to."""
        dst = self.source + self.die
        if Board.BEARING_OFF_POS < dst:
            dst = Board.BEARING_OFF_POS
        return dst

    def print(self) -> None:
        """Print the submove."""
        sys.stdout.write('({}, {})'.format(self.source, self.destination()))

class Move:
    """Represent a player's move."""

    def __init__(self, submoves: List[Submove]) -> None:
        self.submoves = submoves

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return False
        if self.size() != other.size():
            return False
        for submove_index in range(0, self.size()):
            if self.submoves[submove_index] != other.submoves[submove_index]:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def size(self) -> int:
        """Return the number of submoves in the move."""
        return len(self.submoves)

    def push(self, submove: Submove) -> None:
        """Add a submove to the move."""
        self.submoves.append(submove)

    def pop(self) -> Submove:
        """Get the next submove of this move and remove it."""
        return self.submoves.pop()

    def print(self) -> None:
        """Print the move."""
        sys.stdout.write('[')
        for submove in reversed(self.submoves):
            submove.print()
            sys.stdout.write(', ')
        sys.stdout.write(']\n')

class Player(metaclass=ABCMeta):
    """Represent the player."""
    @abstractmethod
    def make_move(self, color: 'Color', board: 'Board', dice: DICE) -> Move:
        """Make a move."""

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

    @staticmethod
    def get_opposite_pos(pos: int) -> int:
        """Get the position from the point of view of the other player."""
        return Board.BEARING_OFF_POS - pos

    def get_checkers(self, color: Color, pos: int) -> bool:
        """Get the number of checkers of color."""
        board = self.get_board(color)
        return board[pos]

    def get_opposite_checkers(self, color: Color, pos: int) -> bool:
        """Get the number of checkers of opposite color."""
        board = self.get_board(color.opposite())
        return board[self.get_opposite_pos(pos)]

    def set_checkers(self, color: Color, pos: int, checkers: int) -> None:
        """Set the number of checkers."""
        board = self.get_board(color)
        board[pos] = checkers

    def set_opposite_checkers(
            self, color: Color, pos: int, checkers: int) -> None:
        """Set the number of opposite colored checkers."""
        board = self.get_board(color.opposite())
        board[self.get_opposite_pos(pos)] = checkers

    def is_blocked(self, color: Color, pos: int) -> bool:
        """Check if the point is blocked by the opponent."""
        if Board.BEARING_OFF_POS == pos:
            return False
        return 1 < self.get_opposite_checkers(color, pos)

    def is_all_home(self, color: Color) -> bool:
        """Check if we can start bearing off."""
        for pos in range(Board.BAR_POS, Board.HOME_POS):
            if 0 < self.get_checkers(color, pos):
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
        if self.is_blocked(color, submove.destination()):
            return False
        # Make sure the bar is empty or we're getting out the bar.
        if (0 < self.get_checkers(color, Board.BAR_POS)) and \
                (Board.BAR_POS != submove.source):
            return False
        # We're bearing off a checker.
        if Board.BEARING_OFF_POS == submove.destination():
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
                (1 == self.get_opposite_checkers(color, destination)):
            other_board = self.get_board(color.opposite())
            other_board[Board.BAR_POS] += 1
            other_board[Board.get_opposite_pos(destination)] = 0

    def list_submoves(self, color: Color, die: int) -> List[Submove]:
        """List legal submoves given the die roll."""
        submoves = [] # type: List[Submove]
        for pos in range(Board.BAR_POS, Board.BEARING_OFF_POS):
            submove = Submove(pos, die)
            if self.is_valid_submove(color, submove):
                submoves.append(submove)
        return submoves

    def list_moves_with_ordered_dice_r(
            self, color: Color, dice: DICE) -> List[Move]:
        """List moves using the given order of dice. The moves are not always
        legal."""
        result = [] # type: List[Move]
        if 0 == len(dice):
            return result
        die = dice[0]
        rest = dice[1:]
        submoves = self.list_submoves(color, die)
        for submove in submoves:
            board = copy.deepcopy(self)
            board.do_submove(color, submove)
            moves = board.list_moves_with_ordered_dice_r(color, rest)
            # We didn't find any moves. Create an empty move to add submoves.
            if 0 == len(moves):
                moves.append(Move([]))
            for move in moves:
                move.push(submove)
            result += moves
        return result

    def list_moves(self, color: Color, dice: DICE) -> List[Move]:
        """List legal moves."""
        # We rolled a double.
        if dice[0] == dice[1]:
            # When we roll a double, the order doesn't matter.
            return self.list_moves_with_ordered_dice_r(color, [dice[0]] * 4)
        # We didn't roll a double.
        high_roll = max(dice)
        low_roll = min(dice)
        high_moves = self.list_moves_with_ordered_dice_r(
            color, [high_roll, low_roll])
        low_moves = self.list_moves_with_ordered_dice_r(
            color, [low_roll, high_roll])
        both_dice_moves = []
        can_play_both_dice = False

        for move in high_moves:
            if 2 == move.size():
                can_play_both_dice = True
                both_dice_moves.append(move)

        for move in low_moves:
            if 2 == move.size():
                can_play_both_dice = True
                both_dice_moves.append(move)

        # Make sure we use all possible dice.
        if can_play_both_dice:
            return both_dice_moves

        # Make sure we play the highest possible die.
        if 0 < len(high_moves):
            return high_moves
        return low_moves

    def is_valid_move(self, color: Color, dice: DICE, move: Move) -> bool:
        """Check if the move is legal."""
        moves = self.list_moves(color, dice)
        for legal_move in moves:
            if legal_move == move:
                return True
        return False

    def do_move(self, color: Color, move: Move) -> None:
        """Play a move."""
        for submove in reversed(move.submoves):
            self.do_submove(color, submove)

    def is_winner(self, color: Color) -> bool:
        """Check if the player won the game."""
        return 15 <= self.get_checkers(color, Board.BEARING_OFF_POS)

    def prompt_move(self, color: Color, dice: DICE, player: Player) -> Union[
            Move, Error]:
        """Try to ask the player to make a move."""
        for _ in range(1, 100):
            sys.stdout.write(
                'Rolled {}, {}, enter move: '.format(dice[0], dice[1]))
            sys.stdout.flush()
            move = player.make_move(color, self, dice)
            if self.is_valid_move(color, dice, move):
                return move
            sys.stdout.write('Illegal move. ')
        return Error()

    #def play_game(self, black: Player, white: Player) -> None:
        #"""The main game loop."""
        #for _ in range(1, 100000):



    def _print_checkers(self, pos: int) -> None:
        """Print a point from Black's point of view."""
        black_checkers = self.get_checkers(Color.Black, pos)
        white_checkers = self.get_opposite_checkers(Color.Black, pos)
        if 0 < black_checkers:
            sys.stdout.write(' B{:<2}'.format(black_checkers))
        elif 0 < white_checkers:
            sys.stdout.write(' W{:<2}'.format(white_checkers))
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
            self._print_checkers(pos)
        sys.stdout.write('    ')
        for pos in range(19, 25):
            self._print_checkers(pos)
        sys.stdout.write('    ')
        sys.stdout.write('Black off: {}'.format(self.get_checkers(
            Color.Black, Board.BEARING_OFF_POS)))
        sys.stdout.write('\n')
        for pos in range(12, 6, -1):
            self._print_checkers(pos)
        sys.stdout.write('    ')
        for pos in range(6, 0, -1):
            self._print_checkers(pos)
        sys.stdout.write('    ')
        sys.stdout.write('White bar: {}'.format(self.get_checkers(
            Color.White, Board.BAR_POS)))
        sys.stdout.write('\n')
        for pos in range(12, 6, -1):
            sys.stdout.write(' {:>2} '.format(pos))
        sys.stdout.write('    ')
        for pos in range(6, 0, -1):
            sys.stdout.write(' {:>2} '.format(pos))
        sys.stdout.write('    ')
        sys.stdout.write('White off: {}'.format(self.get_checkers(
            Color.White, Board.BEARING_OFF_POS)))
        sys.stdout.write('\n')
