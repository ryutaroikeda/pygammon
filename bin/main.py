from pygammon.pygammon import Board
from pygammon.pygammon import Game
from pygammon.commandlineplayer import CommandLinePlayer
from pygammon.randomplayer import RandomPlayer

board = Board()

random_player = RandomPlayer()
random_player_2 = RandomPlayer()
cmd_player = CommandLinePlayer()
cmd_player_2 = CommandLinePlayer()

game = Game(board)
game.play_match(random_player, cmd_player)
