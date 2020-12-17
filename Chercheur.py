# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 08:04:47 2020

@author: cleme
"""
import chess
import chess.polyglot

import logging
import random

class Chercheur:
    def __init__(self):
        logging.basicConfig(filename='cherche.log', level=logging.DEBUG)

    def minmax(self,b):
    	logging.debug("Minmax :")
    	try:  
	    	with chess.polyglot.open_reader("bookfish.bin") as reader:
	    		best_entry = reader.find(b)
	    		logging.debug("L'entré est :")
	    		logging.debug(best_entry)
	    		print(best_entry.move, best_entry.weight)
	    	return best_entry.move
    	except:
	    	logging.debug("Erreur")
	    	print(self.random_move(b))
	    	return self.random_move(b)

    def random_move(self, b):
    	moves = []
    	for i in b.legal_moves:
    		moves.append(i)
    	index = random.randint(0,len(moves)-1)
    	return moves[index]


