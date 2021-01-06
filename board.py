import chess
import chess.pgn
import random
import datetime
import os

import logging

from Chercheur import Chercheur

class Jeu:
	"""docstring for Jeu"""
	def __init__(self):
		self.board = chess.Board()
		self.ch = Chercheur()
		self.game = chess.pgn.Game()
		self.game.headers["Event"] = "Partie contre un joueur"
		self.game.headers["Date"] = datetime.datetime.now()
		self.game.headers["Black"] = "Moteur du Proj531"
		self.node = False


	def getBoard(self):
		return self.board
	
	def mouv_entrant(self, move_uci):
		self.board.push(chess.Move.from_uci(move_uci))
		if self.node == False :
			self.node = self.game.add_variation(chess.Move.from_uci(move_uci))
		else :
			self.node = self.node.add_variation(chess.Move.from_uci(move_uci))

	def mouv_sortant(self):
		#move_out = self.random_move()
		move_out = self.ch.cherche(self.board)
		self.board.push(move_out)
		self.node = self.node.add_variation(chess.Move.from_uci(move_out.uci()))
		return move_out.uci()


	def random_move(self):
   		moves = []
   		for i in self.board.legal_moves:
   			moves.append(i)
   		index = random.randint(0,len(moves)-1)
   		return moves[index]

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
		
