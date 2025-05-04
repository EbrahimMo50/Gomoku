class Manager:

    DRAW = 1
    BLACK_WIN = 2
    WHITE_WIN = 3

    def __init__(self, board):
        self.board = board
    
    def play(self, x, y, color):
        
        if(self.board.matrix[x][y] != 0):
            return -1
        
        self.board.matrix[x][y] = color
        
        result = self.__is_over(x, y, color)

        if result == self.WHITE_WIN:
            return self.WHITE_WIN
        
        elif result == self.BLACK_WIN:
            return self.BLACK_WIN
        
        elif self.__is_board_full():
            return self.DRAW
        
        return 0


    def __is_over(self, last_x, last_y, color):

        directions = [
            [(1, 0), (-1, 0)],    # vertical
            [(0, 1), (0, -1)],    # horizontal
            [(1, 1), (-1, -1)],   # diagonal \
            [(1, -1), (-1, 1)]    # diagonal /
        ]

        for axis in directions:
            count = 1  # the stone just placed
            for dx, dy in axis:
                nx, ny = last_x + dx, last_y + dy
                while 0 <= nx < self.board.DIMENSIONS and 0 <= ny < self.board.DIMENSIONS:
                    if self.board.matrix[nx][ny] == color:
                        count += 1
                        nx += dx
                        ny += dy
                    else:
                        break
            if count >= 5:
                return self.WHITE_WIN if color == self.board.WHITE else self.BLACK_WIN
        return self.DRAW

    def __is_board_full(self):
        # no defination for blank place in board so will use 0
        for row in self.board.matrix:
            if 0 in row:
                return False
        return True