#Fichier contenant la classe jeu qui gère une partie

import chess
import chess.pgn
import random
import datetime
import os

import logging

from chercheur import Chercheur

#Classe qui gère la planche de jeu
class Jeu:
	
	#En initialisant un Jeu on crée une board, chercheur et une game pour la sauvegarde en PGN
	def __init__(self):
		self.board = chess.Board()
		self.ch = Chercheur()
		self.game = chess.pgn.Game()
		self.game.headers["Event"] = "Partie contre un joueur"
		self.game.headers["Date"] = datetime.datetime.now()
		self.game.headers["Black"] = "Moteur du Proj531"
		self.node = False

	#Fonction pour récupérer la board
	def getBoard(self):
		return self.board
	
	#Fonction qui prend un move en uci en paramètre et qui le joue sur la board
	def mouv_entrant(self, move_uci):
		self.board.push(chess.Move.from_uci(move_uci))
		if self.node == False :
			self.node = self.game.add_variation(chess.Move.from_uci(move_uci))
		else :
			self.node = self.node.add_variation(chess.Move.from_uci(move_uci))

	#Fonction qui cherche le mouvement le plus adapter, le joue et le retourne
	def mouv_sortant(self):
		#move_out = self.random_move()
		move_out = self.ch.cherche(self.board)
		self.board.push(move_out)
		self.node = self.node.add_variation(chess.Move.from_uci(move_out.uci()))
		return move_out.uci()

	#Fonction qui retourne un mouvement aléatoire
	#N'est plus utilisé
	def random_move(self):
   		moves = []
   		for i in self.board.legal_moves:
   			moves.append(i)
   		index = random.randint(0,len(moves)-1)
   		return moves[index]

   	#Fonction qui enregistre la gmae au format PGN dans le dossier Saved Game
	def save(self):
		try:
			os.mkdir("Saved Games")
		except OSError as error:
			print(error)
		name = str(self.game.headers["Date"])[0:19] + ".pgn"
		res = ""
		for i in range(0, len(name)):
			if name[i] == (":"):
				res = res + "-"
			else :
				res = res + name[i]
		pgn = open("Saved Games/"+ res, 'w', encoding="utf-8")
		exporter = chess.pgn.FileExporter(pgn)
		self.game.accept(exporter)
		
