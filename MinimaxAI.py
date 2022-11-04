from math import inf
import chess
import random
import sys



class MinimaxAI():
    def __init__(self, depth, player1):
        # max depth
        self.depth = depth
        # true if player is white and false otherwise
        self.player1 = player1

    # returns minimax function
    def choose_move(self, board):
        return self.minimax(board)

    # utility function that takes in board as a parameter
    def utility(self, board):
        if board.is_checkmate():
            # previous was white's turn
            if board.turn == self.player1:
                value = float(-inf)
            # previous was black's turn
            elif board.turn != self.player1:
                value = float(inf)
        # if game ends in a draw
        elif board.is_stalemate(): 
            value = float(0)
        else:
            value = float(self.evaluateMove(board))
        return value


    # evaluation function that takes in board as a parameter
    def evaluateMove(self, board):
        # number of white and black pawns on current board
        Pwhite, Pblack = len(board.pieces(chess.PAWN, chess.WHITE)), len(board.pieces(chess.PAWN, chess.BLACK))
        # number of white and black kings on current board
        Kwhite, Kblack = len(board.pieces(chess.KING, chess.WHITE)), len(board.pieces(chess.KING, chess.BLACK))
        # number of white and black queens on current board
        Qwhite, Qblack = len(board.pieces(chess.QUEEN, chess.WHITE)), len(board.pieces(chess.QUEEN, chess.BLACK))
        # number of white and black bishops on current board
        Bwhite, Bblack = len(board.pieces(chess.BISHOP, chess.WHITE)), len(board.pieces(chess.BISHOP, chess.BLACK))
        # number of white and black knights on current board
        Kgwhite, Kgblack = len(board.pieces(chess.KNIGHT, chess.WHITE)), len(board.pieces(chess.KNIGHT, chess.BLACK))
        # number of white and black rooks on current board
        Rwhite, Rblack = len(board.pieces(chess.ROOK, chess.WHITE)), len(board.pieces(chess.ROOK, chess.BLACK))
        # evaluation that takes in the scores of each pieces and returns the utility
        evaluation = 1 * (Pwhite - Pblack) +  9 * (Qwhite - Qblack) + 3 * (Bwhite - Bblack) + 3* (Kgwhite - Kgblack) + 5 * (Rwhite - Rblack) + 200 * (Kwhite - Kblack)
        if self.player1:
            return evaluation
        else:
            # reverse evaluation if the player is black
            return 1 * (Pblack - Pwhite) + 9 * (Qblack - Qwhite) + 3 * (Bblack - Bwhite) + 3 * (Kgblack - Kgwhite) + 5 * (Rblack - Rwhite) + 200 * (Kblack - Kwhite)

    # minimax function that takes in board as a parameter
    def minimax(self, board):
        # set value equal to negative infinity
        v = float(-inf)
        # get all the list of moves
        moves = list(board.legal_moves)
        # if no moves, exit
        if len(moves) == 0:
            sys.exit(0)
        # randomly shuffle the moves so it doesn't get stuck in a loop
        random.shuffle(moves)
        # assign bestmove 
        bestmove = moves[0]

        for a in moves:
            board.push(a)
            value = self.min_value(board, 0)
            if value > v:
                v = value
                bestmove = a
            board.pop()

        return bestmove

    # used by minimax function and takes in depth as a parameter
    def max_value(self, board, depth):
        # if the cutoff test returns true, return the utility of the board
        if self.cutoff(board, depth):
            return self.utility(board)
        v = float(-inf)
        moves = list(board.legal_moves)
        random.shuffle(moves)
        for a in moves:
            board.push(a)
            # else proceed by calling min_value function with depth + 1
            v = max(v, self.min_value(board, depth=depth+1))
            board.pop()
        return v

    # min_value function that is used by minimax and takes in depth as a parameter
    def min_value(self, board, depth):
        # if cutoff test returns true then return utility of the board
        if self.cutoff(board, depth):
            return self.utility(board)
        v = float(inf)
        moves = list(board.legal_moves)
        random.shuffle(moves)
        for a in moves:
            board.push(a)
            # else call max_value function with depth + 1
            v = min(v, self.max_value(board, depth=depth+1))
            board.pop()
        return v

    # cutoff test that checks if the game ends in checkmate or stalemate or if max depth is received
    def cutoff(self, board, depth):
        if board.is_checkmate():
            return True
        elif board.is_stalemate():
            return True
        elif board.is_game_over():
            return True
        elif depth >= self.depth:
            return True
        return False

