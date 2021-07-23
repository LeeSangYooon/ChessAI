# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 14:45:09 2021

@author: samsung
"""

import chess
from copy import deepcopy

piece_score_dict = {chess.PAWN: 1, chess.KNIGHT: 3.05, chess.BISHOP: 3.33,
                    chess.ROOK: 5.63, chess.QUEEN: 9.5, chess.KING: 1000}

position_weights = []
for i in range(8):
    for j in range(8):
        value = (3.5-abs(j - 3.5)) ** 1.5 * 0.1 + (3.5-abs(i-3.5)) ** 2
        value *= 0.1
        if value <0.001:
            value = 0
        position_weights.append(value)
    print(position_weights[i*8:i*8+8])

class AI:
    def __init__(self, board: chess.Board, color, search_width):
        self.board = board
        self.color = color
        self.opp_color = 1 - color
        self.search_depth = len(search_width)
        self.search_width = search_width

        self.loading_func = None

    def score_func(self, board):
        score = sum([len(board.pieces(piece, self.color)) * score for piece, score in piece_score_dict.items()])
        score -= sum([len(board.pieces(piece, self.opp_color)) * score for piece, score in piece_score_dict.items()])
        #print("기물점수:",score)
        posS = 0
        for n in range(64):
            piece = board.piece_at(n)
            if piece is not None and piece.piece_type != chess.KING and piece.piece_type != chess.QUEEN:
                if piece.color == self.color:
                    posS += position_weights[n]
                else:
                    posS -= position_weights[n]
        score += posS
        #print("자리점수:",posS)
        """
        degrees_of_freedom = len(list(board.legal_moves))
        board.turn = 1 - board.turn
        degrees_of_freedom -= len(list(board.legal_moves))
        board.turn = 1 - board.turn
        degrees_of_freedom *= 0.005
        #print("자유도 점수:", degrees_of_freedom)

        if board.turn == self.color:
            score += degrees_of_freedom
        else:
            score -= degrees_of_freedom
        """
        if board.is_check():
            if board.turn == self.color:
                score -= 1
            else:
                score += 1

        return score

    def search_max(self, root_board, root_min, depth):
        moves = [[0, move] for move in list(root_board.legal_moves)]
        for move in moves:
            temp_board = deepcopy(root_board)
            temp_board.push(move[1])
            if temp_board.is_checkmate():
                move[0] = 10000
                return move
            else:
                move[0] = self.score_func(temp_board)
        moves.sort(key=lambda x: x[0], reverse=True)

        if len(moves) == 0:
            return [0, 0]

        if depth == self.search_depth:
            return moves[0]

        if len(moves) > self.search_width[depth]:
            moves = moves[0: self.search_width[depth - 1]]

        max_score = -100000
        max_index = 0
        i = 0

        for move in moves:
            if depth == 1:
                self.loading_func(i / len(moves))

            temp_board = deepcopy(root_board)
            temp_board.push(move[1])
            move[0] = self.search_min(temp_board, max_score, depth + 1)[0]

            if move[0] > root_min:
                return move

            if move[0] > max_score:
                max_score = move[0]
                max_index = i

            i += 1

        return moves[max_index]

    def search_min(self, root_board, root_max, depth):
        moves = [[0, move] for move in list(root_board.legal_moves)]
        for move in moves:
            temp_board = deepcopy(root_board)
            temp_board.push(move[1])

            if temp_board.is_checkmate():
                move[0] = -10000
                return move
            else:
                move[0] = self.score_func(temp_board)
        moves.sort(key=lambda x: x[0], reverse=False)

        if len(moves) == 0:
            return [0, 0]

        if depth == self.search_depth:
            return moves[0]

        if len(moves) > self.search_width[depth]:
            moves = moves[0: self.search_width[depth - 1]]

        # moves.reverse()

        min_score = 100000
        min_index = 0
        i = 0

        for move in moves:
            temp_board = deepcopy(root_board)
            temp_board.push(move[1])
            move[0] = self.search_max(temp_board, min_score, depth + 1)[0]

            if move[0] < root_max:
                return move

            if move[0] < min_score:
                min_score = move[0]
                min_index = i
            i += 1

        return moves[min_index]

    # return [move, score]
    def run(self):
        simulation_board = deepcopy(self.board)
        best_move = self.search_max(simulation_board, 10000, 1)
        return best_move

    pass