# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 08:04:47 2020

@author: cleme
"""
import chess
import chess.polyglot

import logging
import random

from minmax import MinMax
from Evaluateur import Evaluateur

class Chercheur:
    def __init__(self):
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        logging.debug("On essaye d'init un evaluateur")
        self.evaluateur = Evaluateur()
        logging.debug("On essaye d'init un MinmAx")
        self.MM = MinMax(max_depth=3, evaluateur=self.evaluateur)

    def cherche(self,b):
        try:  
            with chess.polyglot.open_reader("bookfish.bin") as reader:
                best_entry = reader.find(b)
                logging.debug("L'entré est :")
                logging.debug(best_entry)
                print(best_entry.move, best_entry.weight)
            return best_entry.move
        except:
            logging.debug("Pas dans l'opening book")
            next_move = self.MM.next_move(b)
            logging.debug("On a calculer le move")
            print(next_move)
            return next_move
    """
    def random_move(self, b):
        moves = []
    	for i in b.legal_moves:
    		moves.append(i)
    	index = random.randint(0,len(moves)-1)
    	return moves[index]"""


