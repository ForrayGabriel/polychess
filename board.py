import chess
import random

from Chercheur import Chercheur

class Jeu:
	"""docstring for Jeu"""
	def __init__(self):
		self.board = chess.Board()
		self.ch = Chercheur()

	def getBoard(self):
		return self.board
	
	def mouv_entrant(self, move_uci):
		self.board.push(chess.Move.from_uci(move_uci))

	def mouv_sortant(self):
		#move_out = self.random_move()
		move_out = self.ch.minmax(self.board)
		self.board.push(move_out)
		return move_out.uci()


	def random_move(self):
   		moves = []
   		for i in self.board.legal_moves:
   			moves.append(i)
   		index = random.randint(0,len(moves)-1)
   		return moves[index]

x = Jeu()
print(x.mouv_sortant())