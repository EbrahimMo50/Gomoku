class Board:
    DIMENSIONS = 15
    BLACK = 1
    WHITE = 2

    def __init__(self):
        self.matrix = [[0 for _ in range(self.DIMENSIONS)] for _ in range(self.DIMENSIONS)]

    def display(self):
        for row_idx, row in enumerate(self.matrix):
            print(f"{row_idx:2}", end=" ")
            for cell in row:
                if cell == self.BLACK:
                    print(" ●", end="")  
                elif cell == self.WHITE:
                    print(" ○", end="")  
                else:
                    print(" .", end="") 
            print() 