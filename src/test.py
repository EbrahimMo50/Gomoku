import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
BOARD_SIZE = 15  # 15x15 standard Gomoku board
CELL_SIZE = 40
MARGIN = 50
PIECE_RADIUS = CELL_SIZE // 2 - 2
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (210, 180, 140)
LINE_COLOR = (0, 0, 0)
BLACK_PIECE = (0, 0, 0)
WHITE_PIECE = (255, 255, 255)
HIGHLIGHT = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Gomoku")

# Game state
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = "black"  # black goes first
game_over = False
winner = None

def draw_board():
    """Draw the Gomoku board"""
    screen.fill(BROWN)
    
    # Draw grid lines
    for i in range(BOARD_SIZE+1):
        # Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, 
                         (MARGIN, MARGIN + i * CELL_SIZE), 
                         (WINDOW_SIZE - MARGIN, MARGIN + i * CELL_SIZE), 2)
        # Vertical lines
        pygame.draw.line(screen, LINE_COLOR, 
                         (MARGIN + i * CELL_SIZE, MARGIN), 
                         (MARGIN + i * CELL_SIZE, WINDOW_SIZE - MARGIN), 2)
    
    # Draw center dot (traditional in Gomoku)
    center = BOARD_SIZE // 2
    pygame.draw.circle(screen, BLACK, 
                      (MARGIN + center * CELL_SIZE, MARGIN + center * CELL_SIZE), 5)

def draw_pieces():
    """Draw all the pieces on the board"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == "black":
                pygame.draw.circle(screen, BLACK_PIECE, 
                                  (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE), 
                                  PIECE_RADIUS)
            elif board[row][col] == "white":
                pygame.draw.circle(screen, WHITE_PIECE, 
                                  (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE), 
                                  PIECE_RADIUS)
                pygame.draw.circle(screen, BLACK, 
                                  (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE), 
                                  PIECE_RADIUS, 1)

def check_win(row, col):
    """Check if the last move resulted in a win"""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # horizontal, vertical, diagonal
    for dr, dc in directions:
        count = 1  # the piece just placed
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == current_player:
            count += 1
            r += dr
            c += dc
            
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == current_player:
            count += 1
            r -= dr
            c -= dc
            
        if count >= 5:
            return True
    return False

def show_game_over():
    """Display the game over message"""
    font = pygame.font.Font(None, 36)
    if winner:
        text = font.render(f"{winner.capitalize()} wins! Click to restart.", True, BLACK)
    else:
        text = font.render("Game Over! Click to restart.", True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
    screen.blit(text, text_rect)

def reset_game():
    """Reset the game state"""
    global board, current_player, game_over, winner
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = "black"
    game_over = False
    winner = None

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # Get mouse position and convert to board coordinates
            x, y = event.pos
            col = round((x - MARGIN) / CELL_SIZE)
            row = round((y - MARGIN) / CELL_SIZE)
            
            # Check if the move is valid
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] is None:
                board[row][col] = current_player
                
                # Check for win
                if check_win(row, col):
                    game_over = True
                    winner = current_player
                else:
                    # Switch player
                    current_player = "white" if current_player == "black" else "black"
        
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # Restart the game if clicked after game over
            reset_game()
    
    # Draw everything
    draw_board()
    draw_pieces()
    
    if game_over:
        show_game_over()
    
    pygame.display.flip()

pygame.quit()
sys.exit()