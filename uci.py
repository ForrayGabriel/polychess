#Fichier qui permet la communication entre le GUI et le moteur

import sys
import logging

import chess
import chess.pgn
import random

from board import Jeu

#Fonction qui choisit un movement aléatoire dans la liste des mouvements disponibles
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

#Fonction qui permet d'envoyer la lignepassée en paramètre au GUI
def output(ligne):
    print(ligne, file=out)


while True:
    #On récupère ce que nous envoie le GUI
    ligne = input()
    logging.debug(ligne)
    
    liste = ligne.split(' ')
    
    #Si l'utilisateur à bouger une pièce
    for i in range(len(liste)):
        if liste[i].startswith('move'):
            logging.debug("Le mouvement reçu est : " + liste[len(liste)-1])
            jeu.mouv_entrant(liste[len(liste)-1])
    
    #Que le GUI demande les infos de jeu 
    if ligne == 'uci':    
        output('id name Moteur 0.1')
        output('id author IDU3')
        output('uciok')
         
    #Si le GUI demande si le moteur est prêt, lui répondre oui
    elif ligne == 'isready':
        output('readyok')

    #Le GUI lance une nouvelle partie
    elif ligne == 'ucinewgame':
        logging.debug("Nouvelle partie")
        #Si une partie etéait en cours, on la sauvegarde en PGN
        if partie_en_cours:
            logging.debug("On a déja une partie")
            jeu.save()
        else :
            logging.debug("On n'a pas encore de partie")
            partie_en_cours = True
        jeu = Jeu()
        logging.debug("On a fait un nouveau jeu")
    
    #Si l'utilisateur quit, on sauvegarde la partie en PGN
    elif ligne == 'quit':
        jeu.save()
        
    #Si le GUI indique que c'est au mmoteur de jouer
    if ligne.startswith('go'):
        logging.debug("C'est a l'IA")
        #On récupère le meilleur mouvement
        move = jeu.mouv_sortant()
        logging.debug("On joue " + 'bestmove ' + move + ' ponder b4a5')
        #On l'envoi
        output('bestmove ' + move + ' ponder b4a5')
