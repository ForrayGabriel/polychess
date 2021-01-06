# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:08:37 2020

@author: Gabriel
"""

import sys
import logging

import chess
import chess.pgn
import random

from board import Jeu

def random_move():
    moves = []
    for i in board.legal_moves:
        moves.append(i)
    index = random.randint(0,len(moves)-1)
    return moves[index]

board = chess.Board()


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
        sys.stderr.write(data)
        sys.stderr.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

logging.basicConfig(filename='test.log', level=logging.DEBUG)
out = Unbuffered(sys.stdout)
partie_en_cours = False

def output(ligne):
    print(ligne, file=out)


while True:
    ligne = input()
    logging.debug(ligne)
    
    liste = ligne.split(' ')
    
    for i in range(len(liste)):
        if liste[i].startswith('move'):
            logging.debug("On try le move " + liste[len(liste)-1])
            jeu.mouv_entrant(liste[len(liste)-1])
    
    if ligne == 'uci':    
        output('id name Moteur 0.1')
        output('id author IDU3')
        output('uciok')
         
    elif ligne == 'isready':
        output('readyok')

    elif ligne == 'ucinewgame':
        logging.debug("Nouvelle partie")
        if partie_en_cours:
            logging.debug("On a déja une partie")
            jeu.save()
        else :
            logging.debug("On n'a pas encore de partie")
            partie_en_cours = True
        jeu = Jeu()
        logging.debug("On a fait un nouveau jeu")
    
    elif ligne == 'quit':
        jeu.save()
        
    if ligne.startswith('go'):
        logging.debug("C'est a l'IA")
        move = jeu.mouv_sortant()
        logging.debug("On joue " + 'bestmove ' + move + ' ponder b4a5')
        output('bestmove ' + move + ' ponder b4a5')
