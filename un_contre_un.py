# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 11:00:53 2020

@author: Gabriel
"""

import chess
import chess.svg
import random


#Fonction qui demander un mouvement dans la console et le retourn sous la forme d'un chess move
def recup_move():
    case_dep = input("Case départ :")
    case_arr = input("Case arrivée :")
    move = chess.Move.from_uci(case_dep+case_arr)
    while move not in board.legal_moves:
        print("Mouvement illégal, merci de recommencer")
        case_dep = input("Case départ :")
        case_arr = input("Case arrivée :")
        move = chess.Move.from_uci(case_dep+case_arr)
    return move

#Fonction qui retourne un coup au hasard dans la liste des coups possibles
def random_move():
    moves = []
    for i in board.legal_moves:
        moves.append(i)
    index = random.randint(0,len(moves)-1)
    return moves[index]


choix = input("Choix du mode de jeu :\n1 - Joueur contre Joueur\n2 - Joueur contre ordinateur aléatoire\n3 - Ordinateur contre lui même en aléatoire\n")

#set the board to its initial position
#corresponding to: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
board = chess.Board()

#Fonction pour jouer en joueur contre joueur
def un_contre_un():
    white = True
    print(board)
    while board.is_game_over() == False:
        if white :
            print("\nWhite to play :")
            white = False
            board.push(recup_move())
        else :
            print("\nBlack to play :")
            white = True
            board.push(recup_move())
        print(board)

#Fonction pour jouer contre un bot jouant aléatoirement
def bot_random():
    white = True
    print(board)
    while board.is_game_over() == False:
        if white :
            print("\nWhite to play :")
            white = False
            board.push(recup_move())
        else :
            print("\nBlack to play :")
            white = True
            board.push(random_move())
        print(board)

#Fonction pour faire s'affronter deux bots jouant aléatoirement
def autoplay_random():
    white = True
    print(board)
    while board.is_game_over() == False:
        if white :
            print("\nWhite to play :")
            white = False
            board.push(random_move())
        else :
            print("\nBlack to play :")
            white = True
            board.push(random_move())
        input("Appuyer sur entrée pour continuer")
        print(board)
        
        
if choix == "1":
    un_contre_un()
elif choix == "2":
    bot_random()
elif choix == "3":
    autoplay_random()
else :
    print("Choix non valide")