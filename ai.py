import random
import numpy as np

class ChessAI:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty  # 1 = Easy, 2 = Medium, 3 = Hard
        self.piece_values = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
        
        # Piece square tables for positional evaluation
        self.pawn_table = np.array([
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [10,10, 20, 30, 30, 20, 10, 10],
            [50,50, 50, 50, 50, 50, 50, 50],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ])
        
        self.knight_table = np.array([
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ])
        
        self.king_table = np.array([
            [20, 30, 10,  0,  0, 10, 30, 20],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30]
        ])

    def make_move(self, game_state):
        valid_moves = game_state.get_valid_moves()
        
        if self.difficulty == 1:  # Random moves
            return random.choice(valid_moves)
        elif self.difficulty == 2:  # Captures and checks
            capturing_moves = [m for m in valid_moves if m.piece_captured != "--"]
            if capturing_moves:
                # Prioritize higher value captures
                capturing_moves.sort(key=lambda x: self.piece_values.get(x.piece_captured[1], 0), reverse=True)
                return capturing_moves[0]
            else:
                return random.choice(valid_moves)
        else:  # Level 3 - MiniMax with simple evaluation
            best_move = None
            best_score = -9999
            for move in valid_moves:
                game_state.make_move(move)
                score = -self.evaluate_board(game_state)
                game_state.undo_move()
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move if best_move else random.choice(valid_moves)

    def evaluate_board(self, game_state):
        score = 0
        # Material evaluation
        for r in range(8):
            for c in range(8):
                piece = game_state.board[r][c]
                if piece != "--":
                    value = self.piece_values[piece[1]]
                    if piece[0] == 'w':
                        score += value
                        # Positional evaluation
                        if piece[1] == 'p':
                            score += self.pawn_table[r][c]
                        elif piece[1] == 'N':
                            score += self.knight_table[r][c]
                        elif piece[1] == 'K':
                            score += self.king_table[r][c]
                    else:
                        score -= value
                        # Positional evaluation for black (flipped board)
                        if piece[1] == 'p':
                            score -= self.pawn_table[7-r][c]
                        elif piece[1] == 'N':
                            score -= self.knight_table[7-r][c]
                        elif piece[1] == 'K':
                            score -= self.king_table[7-r][c]
        
        # King safety evaluation
        if game_state.in_check():
            if game_state.white_to_move:
                score -= 50  # Black just put white in check
            else:
                score += 50  # White just put black in check
        
        return score
