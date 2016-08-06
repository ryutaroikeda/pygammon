from pygammon.pygammon import Board
from pygammon.commandlineplayer import CommandLinePlayer
from pygammon.randomplayer import RandomPlayer


board = Board()
board.setup()

random_player = RandomPlayer()
cmd_player = CommandLinePlayer()

board.play_game(random_player, cmd_player)
