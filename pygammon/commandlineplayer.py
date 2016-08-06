"""Command line interface for backgammon player."""
import sys
from typing import Union

from pygammon.pygammon import Board
from pygammon.pygammon import Color
from pygammon.pygammon import DICE
from pygammon.pygammon import Move
from pygammon.pygammon import Player
from pygammon.pygammon import Submove

class Error:
    """Represent user input errors."""

    def __init__(self, message: str) -> None:
        self.message = message

    def get_message(self) -> str:
        """Get the error message."""
        return self.message

class CommandLinePlayer(Player):
    """Command line interface."""
    def make_move(self, color: Color, board: Board, dice: DICE) -> Move:
        """Parse a move from the console."""
        if dice[0] == dice[1]:
            dice.append(dice[0])
            dice.append(dice[0])

        while True:
            sys.stdout.write('Rolled {}-{}, enter {} move: '.format(
                dice[0], dice[1], color))
            feed = input()
            move = self._parse_command(feed, color, board, dice)
            if isinstance(move, Error):
                sys.stdout.write('{}\n'.format(move.get_message()))
                continue
            return move

    @staticmethod
    def _parse_submove(feed: str, color: Color) -> Union[Submove, Error]:
        """Parse a submove.
        Each submove is a pair of points separated by /.
        Assume the board is viewed from Black's perspective.
        """
        parts = feed.split('/')

        if 2 != len(parts):
            return Error(
                'Invalid submove {}. Needs to be a/b.'.format(feed))

        if parts[0].isdigit():
            source = int(parts[0])
        elif 'bar' == parts[0].lower():
            source = 0
        else:
            return Error('Invalid submove source {}'.format(parts[0]))

        if parts[1].isdigit():
            destination = int(parts[1])
        elif 'off' == parts[1].lower():
            destination = Board.BEARING_OFF_POS
        else:
            return Error('Invalid submove destination {}'.format(parts[1]))

        if source < 0 or Board.BEARING_OFF_POS < source:
            return Error('Submove source out of range {}'.format(parts[0]))

        if destination < 0 or Board.BEARING_OFF_POS < destination:
            return Error(
                'Submove destination out of range {}'.format(parts[1]))

        if Color.White == color:
            source = Board.get_opposite_pos(source)
            destination = Board.get_opposite_pos(destination)

        die = destination - source
        return Submove(source, die)

    def _parse_move(
            self, feed: str, color: Color, dice: DICE) -> Union[Move, Error]:
        """Parse a move.
        A move is a list of submoves separated by whitespace.
        """
        submove_feeds = feed.split()
        submoves = [] # type: List[Submove]
        for submove_feed in submove_feeds:
            submove = self._parse_submove(submove_feed, color)
            if isinstance(submove, Error):
                return submove
            submoves.append(submove)

        # Make sure dice are correct when bearing off.
        sorted_dice = list(dice)
        sorted_dice.sort()
        for submove in submoves:
            # If we're not bearing off, the die is correct.
            if Board.BEARING_OFF_POS != submove.destination():
                if submove.die in sorted_dice:
                    sorted_dice.remove(submove.die)
                    continue
                return Error('There\'s no die for submove {}'.format(submove))

            # If we're bearing off, pick the smallest legal die.
            did_find_die = False
            for die in sorted_dice:
                if die < submove.die:
                    continue
                did_find_die = True
                submove.die = die
                sorted_dice.remove(die)
                break

            if did_find_die:
                continue

            return Error('There\'s no die for submove {}'.format(submove))

        return Move(submoves)

    @staticmethod
    def _format_submove(submove: Submove, color: Color) -> str:
        source = submove.source
        destination = submove.destination()
        if Color.White == color:
            source = Board.get_opposite_pos(source)
            destination = Board.get_opposite_pos(destination)
        return '{}/{}'.format(source, destination)

    @staticmethod
    def _format_move(move: Move, color: Color) -> str:
        result = '['
        for submove in move.submoves:
            result += ' {} '.format(CommandLinePlayer._format_submove(
                submove, color))
        result += ']'
        return result

    def _parse_command(
            self, feed: str, color: Color, board: Board, dice: DICE) \
                -> Union[Move, Error]:
        """Parse a command."""
        feed = feed.strip()
        if 'help' == feed:
            return Error('help -- show this message\n' + \
                'list -- list all moves\n' + \
                'show -- show the board\n')

        if 'list' == feed:
            moves = board.list_moves(color, dice)

            for move_index in range(0, len(moves)):
                sys.stdout.write('{}: {}\n'.format(
                    move_index, CommandLinePlayer._format_move(
                        moves[move_index], color)))
            # cleanup: This is a bad name.
            return Error('listed {} moves'.format(len(moves)))

        if 'show' == feed:
            board.print()
            return Error('')

        return self._parse_move(feed, color, dice)