import pygame
from Engine import Board, Manager
from GUI import UtilizationGui

class Gui:
    # Measures are in px
    BOARD_SIZE = 15  
    CELL_SIZE = 40
    MARGIN = 50
    PIECE_RADIUS = (CELL_SIZE // 2) - 2
    WINDOW_SIZE = BOARD_SIZE * CELL_SIZE + 2 * MARGIN

    # Avilable modes
    _MODES = [
        {"rect": pygame.Rect((WINDOW_SIZE-WINDOW_SIZE/2)/2, 200, WINDOW_SIZE/2, 80), "color": UtilizationGui.Constants.LIGHT_BLUE, "text": "Player vs Player"},
        {"rect": pygame.Rect((WINDOW_SIZE-WINDOW_SIZE/2)/2, 300, WINDOW_SIZE/2, 80), "color": UtilizationGui.Constants.LIGHT_GREEN, "text": "Player vs AI "},
        {"rect": pygame.Rect((WINDOW_SIZE-WINDOW_SIZE/2)/2, 400, WINDOW_SIZE/2, 80), "color": UtilizationGui.Constants.LIGHT_RED, "text": "AI vs AI"}
    ]

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gomoku")
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        self.draw_select_mode()

    # A method to draw the lines and cover the old mode selection menu
    def draw_board(self):
        self.screen.fill(UtilizationGui.Constants.BROWN)
        for i in range(self.BOARD_SIZE+1):
            pygame.draw.line(self.screen, UtilizationGui.Constants.BLACK, 
                            (self.MARGIN, self.MARGIN + i * self.CELL_SIZE), 
                            (self.WINDOW_SIZE - self.MARGIN, self.MARGIN + i * self.CELL_SIZE), 2)
            pygame.draw.line(self.screen, UtilizationGui.Constants.BLACK, 
                            (self.MARGIN + i * self.CELL_SIZE, self.MARGIN), 
                            (self.MARGIN + i * self.CELL_SIZE, self.WINDOW_SIZE - self.MARGIN), 2)
        center = self.BOARD_SIZE // 2
        pygame.draw.circle(self.screen, UtilizationGui.Constants.BLACK, 
                        (self.MARGIN + center * self.CELL_SIZE, self.MARGIN + center * self.CELL_SIZE), 5)
        
    def draw_select_mode(self):
        self.screen.fill(UtilizationGui.Constants.WHITE)
        title = pygame.font.SysFont('Arial', 36).render("Select Gomoku Game Mode", True, UtilizationGui.Constants.BLACK)
        self.screen.blit(title, (self.WINDOW_SIZE//2 - title.get_width()//2, 100))
        
        # Draw mode boxes
        for box in self._MODES:
            pygame.draw.rect(self.screen, box["color"], box["rect"])
            pygame.draw.rect(self.screen, UtilizationGui.Constants.BLACK, box["rect"], 2)  # Border
            
            text = pygame.font.SysFont('Arial', 36).render(box["text"], True, UtilizationGui.Constants.BLACK)
            text_rect = text.get_rect(center=box["rect"].center)
            self.screen.blit(text, text_rect)

    def select_mode(self, pos):
        x, y = pos
        # Dyncamically getting rectangles dimensions from modes
        if(x >= (self.WINDOW_SIZE-self.WINDOW_SIZE/2)/2 and x <= (self.WINDOW_SIZE-self.WINDOW_SIZE/2)/2 + self.WINDOW_SIZE/2):
            if(y >= self._MODES[0]["rect"][1] and y <= self._MODES[0]["rect"][1] + self._MODES[0]["rect"][3]):
                return UtilizationGui.Constants.HUMAN_VS_HUMAN
            if(y >= self._MODES[1]["rect"][1] and y <= self._MODES[1]["rect"][1] + self._MODES[2]["rect"][3]):
                return UtilizationGui.Constants.HUMAN_VS_AI
            if(y >= self._MODES[2]["rect"][1] and y <= self._MODES[2]["rect"][1] + self._MODES[2]["rect"][3]):
                return UtilizationGui.Constants.AI_VS_AI
            
        return UtilizationGui.Constants.INVALID_MODE

    def update_board(self, board):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if board[row][col] == Board.Board.BLACK:
                    pygame.draw.circle(self.screen, UtilizationGui.Constants.BLACK, 
                                    (self.MARGIN + col * self.CELL_SIZE, self.MARGIN + row * self.CELL_SIZE), 
                                    self.PIECE_RADIUS)
                    
                elif board[row][col] == Board.Board.WHITE:
                    pygame.draw.circle(self.screen, UtilizationGui.Constants.WHITE, 
                                    (self.MARGIN + col * self.CELL_SIZE, self.MARGIN + row * self.CELL_SIZE), 
                                    self.PIECE_RADIUS)
                    pygame.draw.circle(self.screen, UtilizationGui.Constants.BLACK, 
                                    (self.MARGIN + col * self.CELL_SIZE, self.MARGIN + row * self.CELL_SIZE), 
                                    self.PIECE_RADIUS, 1)

    def convert_pos_to_index(self, pos):
        x,y = pos
        col = round((x - self.MARGIN) / self.CELL_SIZE)
        row = round((y - self.MARGIN) / self.CELL_SIZE)
        return col, row
    
    def show_game_over(self, state):
        font = pygame.font.Font(None, 36)

        if(state == Manager.Manager.DRAW):
            text = font.render("DRAW!", True, UtilizationGui.Constants.BLACK)
        elif(state == Manager.Manager.BLACK_WIN):
            text = font.render("BLACK WINS!", True, UtilizationGui.Constants.BLACK)
        elif(state == Manager.Manager.WHITE_WIN):
            text = font.render("WHITE WINS!", True, UtilizationGui.Constants.BLACK)

        text_rect = text.get_rect(center=(self.WINDOW_SIZE//2, self.WINDOW_SIZE//2))
        pygame.draw.rect(self.screen, UtilizationGui.Constants.WHITE, text_rect.inflate(20, 20))
        self.screen.blit(text, text_rect)