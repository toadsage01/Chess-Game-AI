import pygame
from chess_engine import GameState
from ai import ChessAI

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 512, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Chess")

def draw_game_state(screen, gs, images):
    """Draw the complete game state"""
    # Draw squares
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[(r+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*64, r*64, 64, 64))
    
    # Draw pieces
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(c*64, r*64, 64, 64))

def load_images():
    """Load piece images with optional flag textures"""
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    images = {}
    for piece in pieces:
        try:
            # Try to load custom flag textures
            if piece == 'wK' and usa_flag:
                images[piece] = pygame.image.load("assets/flags/usa.png")
            elif piece == 'bK' and china_flag:
                images[piece] = pygame.image.load("assets/flags/china.png")
            else:
                images[piece] = pygame.image.load(f"assets/pieces/{piece}.svg")
        except:
            # Fallback to simple colored pieces
            images[piece] = pygame.Surface((64, 64))
            images[piece].fill((255, 255, 255) if piece[0] == 'w' else (0, 0, 0))
    return images

def main():
    global usa_flag, china_flag
    usa_flag = False
    china_flag = False
    
    gs = GameState()
    ai = ChessAI(difficulty=1)  # 1 = Easy, 2 = Medium, 3 = Hard
    images = load_images()
    
    running = True
    player_one = True  # White = Human
    player_two = False  # Black = AI or Human
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                
            # Easter egg toggle (F1 for USA, F2 for China)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F1:
                    usa_flag = not usa_flag
                if e.key == pygame.K_F2:
                    china_flag = not china_flag
                images = load_images()
                
            # Handle mouse clicks for moves
            if e.type == pygame.MOUSEBUTTONDOWN and (player_one or player_two):
                # ... (add move logic here)
                pass
                
        # AI move if it's their turn
        if not player_one and not player_two:
            ai.make_move(gs)
            player_one, player_two = player_two, player_one
            
        draw_game_state(screen, gs, images)
        pygame.display.flip()

if __name__ == "__main__":
    main()
