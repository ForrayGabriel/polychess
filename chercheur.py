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

DEPTH = 1


class Chercheur:
    def __init__(self):
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        self.evaluateur = Evaluateur()
        self.MM = MinMax(max_depth=DEPTH, evaluateur=self.evaluateur)

    def cherche(self,b):
        try:  
            with chess.polyglot.open_reader("bookfish.bin") as reader:
                best_entry = reader.find(b)
                logging.debug("L'entré est :")
                logging.debug(best_entry)
                print(best_entry.move, best_entry.weight)
            return best_entry.move
        except:
            next_move = self.MM.next_move(b)
            print(next_move)
            logging.debug("Le move de l'IA est ")
            logging.debug(next_move)
            return next_move
    """
    def random_move(self, b):
        moves = []
    	for i in b.legal_moves:
    		moves.append(i)
    	index = random.randint(0,len(moves)-1)
    	return moves[index]"""


