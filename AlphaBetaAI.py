import chess
from math import inf
import sys
import random

class AlphaBetaAI():
    # this following code is the same as the one in minimax
    def __init__(self, depth, player1):
        self.depth = depth
        self.player1 = player1
    
    def choose_move(self, board):
        return self.minimax(board)


    def utility(self, board):
        if board.is_checkmate():
            # previous was white's turn
            if board.turn == self.player1:
                value = float(-inf)
            # previous was black's turn
            elif board.turn != self.player1:
                value = float(inf)
        elif board.is_stalemate():
            value = float(0)
        else:
            value = float(self.evaluateMove(board))
        return value

    def evaluateMove(self, board):
        Pwhite, Pblack = len(board.pieces(chess.PAWN, chess.WHITE)), len(board.pieces(chess.PAWN, chess.BLACK))
        Kwhite, Kblack = len(board.pieces(chess.KING, chess.WHITE)), len(board.pieces(chess.KING, chess.BLACK))
        Qwhite, Qblack = len(board.pieces(chess.QUEEN, chess.WHITE)), len(board.pieces(chess.QUEEN, chess.BLACK))
        Bwhite, Bblack = len(board.pieces(chess.BISHOP, chess.WHITE)), len(board.pieces(chess.BISHOP, chess.BLACK))
        Kgwhite, Kgblack = len(board.pieces(chess.KNIGHT, chess.WHITE)), len(board.pieces(chess.KNIGHT, chess.BLACK))
        Rwhite, Rblack = len(board.pieces(chess.ROOK, chess.WHITE)), len(board.pieces(chess.ROOK, chess.BLACK))
        evaluation = 1 * (Pwhite - Pblack) +  9 * (Qwhite - Qblack) + 3 * (Bwhite - Bblack) + 3* (Kgwhite - Kgblack) + 5 * (Rwhite - Rblack) + 20 * (Kwhite - Kblack)
        if self.player1:
            return evaluation
        else:
            return 1 * (Pblack - Pwhite) + 9*(Qblack - Qwhite) + 3 * (Bblack - Bwhite) + 3 * (Kgblack - Kgwhite) + 5 * (Rblack - Rwhite) + 20 * (Kblack - Kwhite)

    def minimax(self, board):
        v = float(-inf)
        moves = list(board.legal_moves)
        if len(moves) == 0:
            sys.exit(0)

        random.shuffle(moves)
        bestmove = moves[0]
        for a in moves:
            board.push(a)
            value = self.min_value(board, 0, alpha=-inf, beta=inf)
            if value > v:
                v = value
                bestmove = a
            board.pop()
        return bestmove

    # difference here is that now max_value takes in two more parameters - alpha and beta
    def max_value(self, board, depth, alpha, beta):
        if self.cutoff(board, depth):
            return self.utility(board)
        v = float(-inf)
        moves = self.node_reorder(board, max=True)
        random.shuffle(moves)
        for a in moves:
            board.push(a)
            v = max(v, self.min_value(board, depth=depth+1, alpha=alpha, beta=beta))
            board.pop()
            # if v is greater than beta return v else set alpha to be max of alpha and v
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    # the difference here is that min_value function now takes two more parameters - alpha and beta
    def min_value(self, board, depth, alpha, beta):
        if self.cutoff(board, depth):
            return self.utility(board)
        v = float(inf)
        moves = self.node_reorder(board, max=False)
        random.shuffle(moves)
        for a in moves:
            board.push(a)
            v = min(v, self.max_value(board, depth=depth+1, alpha=alpha, beta=beta))
            board.pop()
            # if v is less than alpha then return v else set beta equal to min of beta and v
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

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

    # reordering the nodes
    def node_reorder(self, board, max):
        # dictionary that will keep track of the utility of each move
        move_dict = {}
        moves = list(board.legal_moves)
        for a in moves:
            board.push(a)
            u = self.evaluateMove(board)
            board.pop()
            move_dict[a] = u

        # sorted the move dictionary according to the utilities
        sorted_dict = {k: v for k, v in sorted(move_dict.items(), key=lambda item:item[1])}
        # gets the moves in order of the utilities 
        sorted_list = list(sorted_dict.keys())
        # return reversed list if maximum first is true else return normal list
        if max:
            sorted_list.reverse()
        return sorted_list
