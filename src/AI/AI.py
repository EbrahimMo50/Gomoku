from typing import Tuple, List, Optional
from Engine.Board import Board

# Notes: As the depth of the minimax algorithm increases, the time complexity increases exponentially.
# So plz be careful with the depth you choose.
# The depth of the minimax algorithm is set to 3 by default, which is a good balance between performance and accuracy.
# BTW the AI is not very strong, so you can increase the depth to 4 or 5 if you want a stronger AI. (Be careful with the time it takes to calculate the move)
# The AI uses a simple heuristic evaluation function to evaluate the board state.
class AI:
    def __init__(self, board_size: int = 15, win_length: int = 5, player_stone: int = 2, opponent_stone: int = 1, max_depth: int = 2):
        """
        Args:
            board_size: Size of the Gomoku board (typically 15x15)
            win_length: Number of stones in a row needed to win (typically 5)
            player_stone: Stone value for the AI player (typically 1 or 2)
            opponent_stone: Stone value for the opponent (typically 2 or 1)
            max_depth: Maximum depth for the minimax algorithm
        """
        self.board_size = board_size
        self.win_length = win_length
        self.player_stone = player_stone
        self.opponent_stone = opponent_stone
        self.max_depth = max_depth
        
        # Evaluation weights for different patterns
        self.weights = {
            'five': 100000,        # Win
            'open_four': 10000,    # Four in a row with open ends
            'four': 1000,          # Four in a row with one end blocked
            'open_three': 500,     # Three in a row with open ends
            'three': 100,          # Three in a row with one end blocked
            'open_two': 50,        # Two in a row with open ends
            'two': 10              # Two in a row with one end blocked
        }
    
    def ai_move(self, board: Board) -> Tuple[int, int]:
        """
        Args:
            board: Current state of the board
            
        Returns:
            Tuple of (row, col) for the best move
        """
        # Get all valid moves (empty cells)
        valid_moves = self._get_valid_moves(board)
        
        # If this is the first move, play in the center or near center
        if self._is_board_empty(board):
            center = self.board_size // 2
            return (center, center)
        
        # If there's only one valid move, take it
        if len(valid_moves) == 1:
            return valid_moves[0]
        
        # Use minimax with alpha-beta pruning to find the best move
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in valid_moves:
            row, col = move
            # Make the move
            board.matrix[row][col] = self.player_stone
            
            # Calculate score using minimax
            score = self._minimax(board, self.max_depth - 1, False, alpha, beta)
            
            # Undo the move
            board.matrix[row][col] = 0
            
            # Update best move if needed
            if score > best_score:
                best_score = score
                best_move = move
            
            # Update alpha
            alpha = max(alpha, best_score)
        
        return best_move
    
    def _minimax(self, board: Board, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        """
        Args:
            board: Current state of the board
            depth: Current depth in the search tree
            is_maximizing: True if maximizing player's turn, False otherwise
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            Score for the current board state
        """
        # Check if game is over or max depth reached
        if depth == 0 or self._is_terminal_state(board):
            return self._evaluate_board(board)
        
        valid_moves = self._get_valid_moves(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                row, col = move
                board.matrix[row][col] = self.player_stone
                eval = self._minimax(board, depth - 1, False, alpha, beta)
                board.matrix[row][col] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                row, col = move
                board.matrix[row][col] = self.opponent_stone
                eval = self._minimax(board, depth - 1, True, alpha, beta)
                board.matrix[row][col] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def _get_valid_moves(self, board: Board) -> List[Tuple[int, int]]:
        """
        Args:
            board: Current state of the board
            
        Returns:
            List of (row, col) tuples representing valid moves
        """
        valid_moves = []
        
        # If the board is empty, return the center position
        if self._is_board_empty(board):
            center = self.board_size // 2
            return [(center, center)]
        
        # Consider cells that are adjacent to existing stones
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board.matrix[i][j] == 0:  # Empty cell
                    # Check if this cell is adjacent to any existing stone
                    if self._has_neighbor(board, i, j):
                        valid_moves.append((i, j))
        
        # If no valid moves found (unlikely), return all empty cells
        if not valid_moves:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board.matrix[i][j] == 0:
                        valid_moves.append((i, j))
        
        return valid_moves
    
    def _is_board_empty(self, board: Board) -> bool:
        #Check if the board is empty (all cells are 0)
        for row in board.matrix:
            for cell in row:
                if cell != 0:
                    return False
        return True
    
    def _has_neighbor(self, board: Board, row: int, col: int, distance: int = 2) -> bool:
        """
        Args:
            board: Current state of the board
            row: Row index
            col: Column index
            distance: Maximum distance to check for neighbors
            
        Returns:
            True if the cell has at least one neighbor, False otherwise
        """
        for i in range(max(0, row - distance), min(self.board_size, row + distance + 1)):
            for j in range(max(0, col - distance), min(self.board_size, col + distance + 1)):
                if board.matrix[i][j] != 0:  # Non-empty cell
                    return True
        return False
    
    def _is_terminal_state(self, board: Board) -> bool:
        """
        Args:
            board: Current state of the board
            
        Returns:
            True if game is over, False otherwise
        """
        # Check if either player has won
        for stone in [self.player_stone, self.opponent_stone]:
            if self._check_win(board, stone):
                return True
        
        # Check if board is full
        for row in board.matrix:
            if 0 in row:
                return False
        return True
    
    def _check_win(self, board: Board, stone: int) -> bool:
        """
        Args:
            board: Current state of the board
            stone: Stone value to check for win
            
        Returns:
            True if the player has won, False otherwise
        """
        # Check horizontal
        for i in range(self.board_size):
            for j in range(self.board_size - self.win_length + 1):
                if all(board.matrix[i][j+k] == stone for k in range(self.win_length)):
                    return True
        
        # Check vertical
        for i in range(self.board_size - self.win_length + 1):
            for j in range(self.board_size):
                if all(board.matrix[i+k][j] == stone for k in range(self.win_length)):
                    return True
        
        # Check diagonal (top-left to bottom-right)
        for i in range(self.board_size - self.win_length + 1):
            for j in range(self.board_size - self.win_length + 1):
                if all(board.matrix[i+k][j+k] == stone for k in range(self.win_length)):
                    return True
        
        # Check diagonal (bottom-left to top-right)
        for i in range(self.win_length - 1, self.board_size):
            for j in range(self.board_size - self.win_length + 1):
                if all(board.matrix[i-k][j+k] == stone for k in range(self.win_length)):
                    return True
        
        return False
    
    def _evaluate_board(self, board: Board) -> float:
        """
        Args:
            board: Current state of the board
            
        Returns:
            Score for the current board state
        """
        # Check if AI player has won
        if self._check_win(board, self.player_stone):
            return float('inf')
        
        # Check if opponent has won
        if self._check_win(board, self.opponent_stone):
            return float('-inf')
        
        # Count patterns for both players
        ai_score = self._count_patterns(board, self.player_stone)
        opponent_score = self._count_patterns(board, self.opponent_stone)
        
        # Return the difference (positive is good for AI)
        return ai_score - opponent_score
    
    def _count_patterns(self, board: Board, stone: int) -> float:
        """
        Args:
            board: Current state of the board
            stone: Stone value to count patterns for
            
        Returns:
            Score based on the patterns found
        """
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Horizontal, vertical, diagonal
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board.matrix[i][j] != stone:
                    continue
                
                # Check in all directions
                for dx, dy in directions:
                    score += self._check_pattern(board, i, j, dx, dy, stone)
        
        return score
    
    def _check_pattern(self, board: Board, row: int, col: int, dx: int, dy: int, stone: int) -> float:
        """
        Args:
            board: Current state of the board
            row: Starting row
            col: Starting column
            dx: Row direction
            dy: Column direction
            stone: Stone value to check for
            
        Returns:
            Score for the pattern found
        """
        # Check bounds
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return 0
        
        # Check if the current cell has the stone
        if board.matrix[row][col] != stone:
            return 0
        
        # Count consecutive stones
        count = 1
        r, c = row + dx, col + dy
        
        while 0 <= r < self.board_size and 0 <= c < self.board_size and board.matrix[r][c] == stone:
            count += 1
            r += dx
            c += dy
        
        # Check if the pattern is open or blocked
        is_open_start = False
        is_open_end = False
        
        # Check if start is open
        r_start, c_start = row - dx, col - dy
        if 0 <= r_start < self.board_size and 0 <= c_start < self.board_size and board.matrix[r_start][c_start] == 0:
            is_open_start = True
        
        # Check if end is open
        if 0 <= r < self.board_size and 0 <= c < self.board_size and board.matrix[r][c] == 0:
            is_open_end = True
        
        # Calculate score based on pattern
        if count >= 5:
            return self.weights['five']
        elif count == 4:
            if is_open_start and is_open_end:
                return self.weights['open_four']
            elif is_open_start or is_open_end:
                return self.weights['four']
        elif count == 3:
            if is_open_start and is_open_end:
                return self.weights['open_three']
            elif is_open_start or is_open_end:
                return self.weights['three']
        elif count == 2:
            if is_open_start and is_open_end:
                return self.weights['open_two']
            elif is_open_start or is_open_end:
                return self.weights['two']
        
        return 0