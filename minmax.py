'''
Classe reprise de matthieuberger sur github.
repositories : matthieuberger/BalooChessEngine 
'''

import time
import chess
import logging

from evaluateur import Evaluateur

class MinMax:

    #profondeur de recherche par défaut
    DEFAULT_MAX_DEPTH = 3

    #On lance minmax avec l'évaluateur de notre choix
    def __init__(self, max_depth=DEFAULT_MAX_DEPTH, evaluateur=None):
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        self.max_depth = max_depth
        if evaluateur is None:
            raise Exception("MinMax need a evaluateur.")
        self.evaluateur = evaluateur
        logging.debug("On a init MinMax")

    #Fonciton qui applique les algorythme min max et alpha beta pour trouver le meilleur coup
    def minmax(self, board, depth, alpha, beta):
        """
        AI function that choice the best move
        :param node: current node of the board
        :param depth: node index in the tree
        :param count: int that is the number of times the minmax func is called
        :return: best value depends of who's turn it is
        """
        b = board

        # check if depth is max depth or if game is over
        # then we return the value of the board
        if depth == self.max_depth or b.is_game_over():
            return self.evaluateur(b)

        if b.turn == chess.BLACK:
            best_val = self.evaluateur.MINVALUE
        else:
            best_val = self.evaluateur.MAXVALUE


        # check value for each moves
        for m in b.legal_moves:

            b.push(m)
            tval = self.minmax(b, depth+1, alpha, beta)
            b.pop()

            # if it's black turn then your goal is to maximize
            if b.turn == chess.BLACK:
                best_val = max(best_val, tval)
                alpha = max(alpha, best_val)
                if (alpha <= beta):
                    return best_val

            # if it's white turn then you want to minimize
            else:
                best_val = min(best_val, tval)
                beta = min(best_val, beta)
                if (alpha >= beta):
                    return best_val

        return best_val

    def next_move(self, board):
        b = board
        depth = 0
        best_move = None

        start = time.time()

        if b.turn == chess.BLACK:
            best_val = self.evaluateur.MINVALUE
        else:
            best_val = self.evaluateur.MAXVALUE

        for m in b.legal_moves:
            b.push(m)
            tval = self.minmax(b, depth, self.evaluateur.MINVALUE,
                    self.evaluateur.MAXVALUE)
            b.pop()

            if b.turn == chess.BLACK:
                if tval >= best_val:
                    best_val = tval
                    best_move = m
            else:
                if tval <= best_val:
                    best_val = tval
                    best_move = m

        eta = time.time() - start
        print("Best value: %.2f -> %s : explored %d nodes in %.3f seconds" %
                (best_val, str(best_move), self.evaluateur.count, eta))

        return best_move