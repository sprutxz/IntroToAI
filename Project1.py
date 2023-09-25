import random
from collections import deque
random.seed(10)
D = 20
Q = 0.5
class board():
    
    def __init__(self, D): #initialises ship to set row and col value
        self.D = D
        self.board = [[False for i in range (D)] for j in range (D)] #creation of ship
        self.cell = [random.randrange(1, D-1) for i in range (2)]
        self.board[self.cell[0]][self.cell[1]] = True
        self.open_cells = [self.cell]

    def get_closed_neighbours(self, cell):
        list = []
        row, col = cell[0], cell[1]
        if row != 0 and self.board[row-1][col] == False:
            list.append([row-1,col])
        if col+1 != self.D and self.board[row][col+1] == False:
            list.append([row, col+1])
        if row+1 != self.D and self.board[row+1][col] == False:
            list.append([row+1, col])
        if col != 0 and self.board[row][col-1] == False:
            list.append([row, col-1])
        return list
    
    def get_open_neighbours(self, cell):
        list = []
        row, col = cell[0], cell[1]
        if row != 0 and self.board[row-1][col] == True:
            list.append((row-1,col))
        if col+1 != self.D and self.board[row][col+1] == True:
            list.append((row, col+1))
        if row+1 != self.D and self.board[row+1][col] == True:
            list.append((row+1, col))
        if col != 0 and self.board[row][col-1] == True:
            list.append((row, col-1))
        return list
    
    def extend_list(self, arr1, arr2, arr3):
        for item in arr2[::-1]:
            if item in arr1:
                arr1.remove(item)
                arr3.append(item)
            if item in arr3:
                arr2.remove(item)
        arr1.extend(arr2)
        return arr1, arr3
    
    def open_ship(self):
        cells_avail_to_open = []
        banned_cells = []
        while True: #loop keeps opening cells until there are no more to open
            list = self.get_closed_neighbours(self.cell)

            cells_avail_to_open, banned_cells = self.extend_list(cells_avail_to_open, list, banned_cells)
            if len(cells_avail_to_open) == 0:
                break
            self.cell = random.choice(cells_avail_to_open)
            cells_avail_to_open.remove(self.cell)
            self.board[self.cell[0]][self.cell[1]] = True
            self.open_cells.append(self.cell)
            if len(cells_avail_to_open) == 0:
                break

    def clear_dead_cells(self):
        dead_cells_dup = []
        dead_cells = []
        for cell in self.open_cells: #adds deadcells to a list
            x, y = cell[0], cell[1]
            if x!=0 and x!= (self.D-1) and y!=0 and y!=(self.D-1):
                if len(self.get_closed_neighbours(cell)) == 3:
                    dead_cells_dup.append(cell)
            else:
                if len(self.get_closed_neighbours(cell)) == 2:
                    dead_cells_dup.append(cell)

        [dead_cells.append(x) for x in dead_cells_dup if x not in dead_cells]

        i = int(len(dead_cells)/2)
        while(i>0 and len(dead_cells)!=0):
            while True:
                cell = random.choice(dead_cells)
                list = self.get_closed_neighbours(cell)
                if len(list) != 0: 
                    delete_cell = random.choice(list)
                    self.board[delete_cell[0]][delete_cell[1]] = True
                    dead_cells.remove(cell)
                    i -= 1
                    break
                else:
                    if len(dead_cells) > 1:
                        dead_cells.remove(cell)
                        continue
                break
        
    def print_ship(self):
        for i in range (self.D+2):
            print("_", end = "")
        print()

        for row in self.board:
            print("|", end = "")
            for col in row:
                if col is True:
                    print("X", end="")
                else:
                    print(" ", end="")
            print("|")

        for i in range (self.D+2):
            print("=", end = "")
        print() 

board = board(D)
board.open_ship()
board.clear_dead_cells()
board.print_ship()

class Bot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def get_pos(self):
        cell = (self.row, self.col)
        return cell

def fire_spread(Q, K):
    chance = float(1-(1-Q)**K)
    return chance

def bfs(board, start, end):
    isVisited = [[False for i in range (D)] for j in range (D)]
    queue = deque()
    isVisited[start[0]][start[1]] = True
    queue.append(start)
    parent_to_cell = {start : None}
            
    while queue: #convert list to tuple
        cell = queue.popleft()
        if cell == end:
            break
        neighbours = board.get_open_neighbours(cell)
        for neighbour in neighbours:
            if isVisited[neighbour[0]][neighbour[1]] == False:
                isVisited[neighbour[0]][neighbour[1]] = True
                queue.append(neighbour)
                parent_to_cell[neighbour] = cell
                
    if cell != end:  # If destination wasn't reached.
        return None
    path = []
    while cell:
        path.append(cell)
        cell = parent_to_cell[cell]
    
    return path[::-1]
    
    #pop queue and do the list thing
    #set parents for each cell to keep track of path
    
bot = Bot(5,8)
print(bfs(board, bot.get_pos(), (6,11)))

fire = fire_spread(Q, 1)
print(fire)
