'''
Classe reprise de matthieuberger sur github.
repositories : BallooChessEngine
'''

import chess
import numpy as np
import logging

class Evaluateur:
    """
    Simple value function that value a board
    """

    PIECES_VALUES = {
        chess.PAWN:100,
        chess.KNIGHT:320,
        chess.BISHOP:330,
        chess.ROOK:500,
        chess.QUEEN:900,
        chess.KING:20000 }

    PIECES_SQUARE_VALUES = {
        chess.PAWN: [[0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]],
        chess.KNIGHT: [[-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]],
        chess.QUEEN: [[-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]],
        chess.BISHOP: [[-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]],
        chess.ROOK: [[0,  0,  0,  0,  0,  0,  0,  0],
            [-5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]],
        chess.KING: [[-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]]}

    MAXVALUE = float('inf')
    MINVALUE = -MAXVALUE

    # Value for a zero board
    ZEROVALUE = 126.5


    def __init__(self):
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        logging.debug("On a init l'evaluateur")
        self.count = 0
        self.memory = {}
        
        

    def __call__(self, board):
        """
        Each time Valuator is called, we increment counter
        node: node with a chess board
        return: value of the board
        """

        self.count += 1
        if self.key(board) in self.memory:
            return self.memory[self.key(board)]

        board = board
        value = self.value(board)
        self.memory[self.key(board)] = value
        return value

    def piece_to_value(self, piece_type, color):
        """
        Return a value for a piece in the board
        return: int
        """
        pval = self.PIECES_VALUES[piece_type]
        if color == chess.BLACK:
            pval *= -1
        return pval

    def get_material_value(self, board):
        """
        This function compute the material value of a board
        board: chhess.Board
        return: float
        """
        value = 0
        pieces = board.piece_map()
        for i in pieces:
            value += self.piece_to_value(pieces[i].piece_type, pieces[i].color)
        return value

    def get_number_of_legal_moves_value(self, board):
        """
        This function return a value regarding of the number of legal moves
        This might be a cool feature
        return: float
        """
        scalar = 1
        if board.turn == chess.BLACK:
            scalar *= -1
        return scalar * board.legal_moves.count()


    def get_mask_value(self, board, piece_type, color):
        """
        Basicaly this function will give us a value depends on pieces position
        This feature is called Piece-Square Tables estimation
        piece_type: type of piece
        return: computed value for a board
        """
        val = 0
        indexes = list(board.pieces(piece_type, color))
        for idx in indexes:
            mask = np.array(self.PIECES_SQUARE_VALUES[piece_type], dtype=int)
            if color == chess.BLACK:
                mask = mask[::-1]

            x = idx//8
            y = idx % 8
            val += mask[x][y]

        if color == chess.BLACK:
            return -val

        return val

    def get_all_masks_value(self, board, color):
        """
        Compute value mask value for all pieces type
        color: chess.WHITE or chess.BLACK
        return: computed value for a board
        """
        val = 0
        for p in self.PIECES_SQUARE_VALUES.keys():
            val += self.get_mask_value(board, p, color)
        return val

    def value(self, board):
        """
        Function that value a board.
        node: node board
        return: float
        """
        # Check game over
        if board.is_game_over():
            #White win
            if board.result() == "1-0":
                return self.MAXVALUE
            elif board.result() == "0-1":
                return self.MINVALUE
            else:
                return 0

        value = 0
        value += self.get_material_value(board) * 10
        value += self.get_all_masks_value(board, board.turn) * 3
        value += self.get_number_of_legal_moves_value(board)

        return value

    def reset(self):
        """
        Reset counter
        """
        self.count = 0

    def key(self, board):
     """
     Return a hash of the board
     """
     return hash((board.board_fen(), board.turn,
         board.castling_rights, board.ep_square))    

eva = Evaluateur()
