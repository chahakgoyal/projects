# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from IterativeDeepening import IterativeDeepening


import sys


player1 = MinimaxAI(2, True)
player2 = AlphaBetaAI(3, False)

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()
print(game)
print(game.board.result())

#print(hash(str(game.board)))
