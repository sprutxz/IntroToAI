import random

class board():
    
    def __init__(self, D): #initialises ship to set row and col value
        self.D = D
        self.board = [[False for i in range (D)] for j in range (D)] #creation of ship
        self.cell = [random.randrange(1, D-1) for i in range (2)]
        self.board[self.cell[0]][self.cell[1]] = True
        self.open_cells = [self.cell]

    
    def print(self):
        print(self.cell)
        print(self.board[self.cell[0]][self.cell[1]])
        print(self.open_cells)

board = board(10)
board.print()