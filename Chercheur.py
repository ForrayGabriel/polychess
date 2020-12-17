# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 08:04:47 2020

@author: cleme
"""
import chess
import chess.polyglot
board = chess.Board()

class Chercheur:
    def __init__(self):
        pass
          
    def minmax(self,b):     
        with chess.polyglot.open_reader("/Users/cleme/OneDrive/Documents/POLYTECH\PROJ 531/TP CHESS/polychess/bookfish.bin") as reader:
            best_entry = reader.find(b)
            print(best_entry.move, best_entry.weight)
        return best_entry.move




            
