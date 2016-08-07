from pygammon.pygammon import Board
from pygammon.pygammon import Game
from pygammon.commandlineplayer import CommandLinePlayer
from pygammon.randomplayer import RandomPlayer

board = Board()
board.setup()

random_player = RandomPlayer()
cmd_player = CommandLinePlayer()

game = Game(board)
game.play_round(random_player, cmd_player)
