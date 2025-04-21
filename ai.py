import random

class ChessAI:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty  # 1-3
        
    def make_move(self, game_state):
        valid_moves = self.get_all_valid_moves(game_state)
        
        # Different difficulty levels
        if self.difficulty == 1:  # Random moves
            return random.choice(valid_moves)
        elif self.difficulty == 2:  # Captures pieces when possible
            capturing_moves = [m for m in valid_moves if m.piece_captured != "--"]
            return random.choice(capturing_moves) if capturing_moves else random.choice(valid_moves)
        else:  # Level 3 - Simple evaluation
            best_move = None
            best_score = -9999
            for move in valid_moves:
                # Simple material count evaluation
                score = 0
                if move.piece_captured != "--":
                    score += self.piece_value[move.piece_captured[1]]
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move if best_move else random.choice(valid_moves)
    
    @property
    def piece_value(self):
        return {'p': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
