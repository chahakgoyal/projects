from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI

def IterativeDeepening(depth, player1, method="MinimaxAI"):
    # loop over all depths and return the best move at the latest depth
        i = 0
        while i <= depth:
            best_move = MinimaxAI(i, player1)
            i += 1
        return best_move
    
