import random
import math
import numpy as np
import heapq
from collections import deque
#random.seed(900)
#random.seed(50)
D = 85

class Board():
    
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
    
    def get_open_cells(self):
        open_cell = []
        i = 0
        for row in self.board:
            j = 0
            for col in row:
                if col is True:
                    open_cell.append((i,j))
                j += 1
            i += 1
        return open_cell
    
    def get_closed_cells(self):
        open_cell = []
        i = 0
        for row in self.board:
            j = 0
            for col in row:
                if col is False:
                    open_cell.append((i,j))
                j += 1
            i += 1
        return open_cell
        
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
        
    def print_sim(self, fire_cells, bot, button):
        for i in range (self.D+2):
            print("_", end = "")
        print()
        m = 0
        for row in self.board:
            print("|", end = "")
            n = 0
            for col in row:
                if (m,n) in fire_cells:
                    print("F", end="")
                elif (m,n) == bot:
                    print("N", end="")
                elif (m,n) == button:
                    print("B", end="")
                else:
                    if col is True:
                        print("X", end="")
                    else:
                        print(" ", end="")
                n += 1
            print("|")
            m += 1

        for i in range (self.D+2):
            print("=", end = "")
        print() 

class Bot:
    def __init__(self, cell):
        self.row = cell[0]
        self.col = cell[1]
    
    def get_pos(self):
        cell = (self.row, self.col)
        return cell
    
    def set_pos(self, cell):
        self.row = cell[0]
        self.col = cell[1]

def fire_spread(Q, K):
    chance = float(1-(1-Q)**K)
    return chance

def bfs(board, start, end, fire_cells):
    isVisited = [[False for i in range (D)] for j in range (D)]
    queue = deque()
    blocked_cells = fire_cells
    isVisited[start[0]][start[1]] = True
    queue.append(start)
    parent_to_cell = {start : None}      
    while queue:
        cell = queue.popleft()
        if cell == end:
            break
        neighbours = board.get_open_neighbours(cell)
        for neighbour in neighbours:
            if neighbour in blocked_cells:
                continue
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

def heuristic(cell, goal, cell_intensity, goal_intensity):
    distance = ((cell[0] - goal[0]) ** 2 + (cell[1] - goal[1]) ** 2) ** 0.5
    influence1 = distance * (cell_intensity/100)
    influence2 = 2*(distance * (goal_intensity/100)) #to give a higher priority for riskier paths if fire is closer to button
    return influence1+influence2

def a_star(grid, start, goal):
    open_list = []
    open_set = set()
    heapq.heappush(open_list, (0, start))
    open_set.add(start)
    came_from = {}
    x1,y1 = start
    x2,y2 = goal
    
    g_score = {(x, y): float('inf') for x, row in enumerate(grid) for y, _ in enumerate(row)}
    g_score[start] = 0
    
    f_score = {(x, y): float('inf') for x, row in enumerate(grid) for y, _ in enumerate(row)}
    f_score[start] = heuristic(start, goal, grid[x1][y1], grid[x2][y2])

    while open_list:
        _, current = heapq.heappop(open_list)
        open_set.remove(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return the path from start to goal

        for neighbor in [(current[0], current[1]-1), (current[0], current[1]+1), (current[0]-1, current[1]), (current[0]+1, current[1])]:
            if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and 
                grid[neighbor[0]][neighbor[1]] != 100 and grid[neighbor[0]][neighbor[1]] != -1):
                tentative_g_score = g_score[current] + 0.1  # 1 is the cost to move each  cell
                x1, y1 = neighbor

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal, grid[x1][y1], grid[x2][y2])
                    if neighbor not in open_set:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
                        open_set.add(neighbor)

    return None  # If no path found


def cal_intensity(fire_cells):
    decay = 15
    propagation_limit = 15
    grid = [[0 for _ in range(D)] for _ in range(D)]
    for x,y in fire_cells:
        grid[x][y] = 100
    
    for _ in range(propagation_limit):
    # Create a deep copy of the grid to store the updated values
        new_grid = [row[:] for row in grid]
        for y in range(len(grid)):
            for x in range(len(grid)):
                if grid[y][x] > 0:
                    neighbors = [(nx, ny) for nx, ny in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)] 
                                if 0 <= nx < len(grid) and 0 <= ny < len(grid)]

                    for nx, ny in neighbors:
                        if new_grid[ny][nx] == 0:
                            surrounding_intensities = [grid[adj_y][adj_x] for adj_x, adj_y in [(nx, ny-1), (nx, ny+1), (nx-1, ny), (nx+1, ny)] 
                                                    if 0 <= adj_x < len(grid) and 0 <= adj_y < len(grid)]

                            total_intensity = sum(surrounding_intensities)
                            adjusted_decay = decay * (1 - total_intensity / 400)
                            adjusted_decay = max(0, adjusted_decay)
                            new_grid[ny][nx] = max(new_grid[ny][nx], math.ceil(grid[y][x] - adjusted_decay))
        grid = new_grid
        
    return grid   
class Sim():
    
    def __init__(self, bot_cell, fire_cell, button_cell, board): #entries should be tuples
        self.bot_cell = bot_cell
        self.fire_cell = fire_cell
        self.button_cell = button_cell
        self.board = board
        
    def bot1(self):
        print(Q)
        t = 0
        bot = Bot(self.bot_cell)
        fire_cells = [self.fire_cell]
        #self.board.print_sim(fire_cells,bot.get_pos(),self.button_cell)
        path = bfs(self.board, self.bot_cell, self.button_cell, fire_cells)
        print(bot.get_pos())
        print(self.button_cell)
        
        if path == None:
            print("No path to button was found")
            return 0
        
        disabled_cells = []
        while (bot.get_pos() != self.button_cell):
            t+=1
            if (bot.get_pos() in fire_cells):
                print("bot was consumed by fire!")
                return 1
            
            if (self.button_cell in fire_cells):
                print("button was destroyed by fire!")
                return 2
            
            bot.set_pos(path.pop(0))
            eval = []
            new_fire_cells = []
            for cell in fire_cells:
                if cell not in disabled_cells:
                    neighbours = self.board.get_open_neighbours(cell)
                    L = 0
                    for neighbour in neighbours:
                        if neighbour not in eval:
                            K = 0 
                            if neighbour in fire_cells:
                                L += 1
                                continue 
                            b_neighbours = self.board.get_open_neighbours(neighbour)
                            for b in b_neighbours:
                                if b in fire_cells:
                                    K += 1

                            if random.uniform(0,1) <= fire_spread(Q, K):
                                new_fire_cells.append(neighbour)
                                if K == len(b_neighbours):
                                    if neighbour not in disabled_cells:
                                        disabled_cells.append(neighbour)      
                            eval.append(neighbour)
                        
                        if neighbour in new_fire_cells:
                            L += 1

                if L == len(neighbours):
                    if cell not in disabled_cells:
                        disabled_cells.append(cell)
                
            fire_cells.extend(new_fire_cells)

            # self.board.print_sim(fire_cells,bot.get_pos(),self.button_cell)
            # input("Press eneter for to run next time step")
            
        if (bot.get_pos() == self.button_cell):
            print("bot got to the button and extuinguised the fire")
            return 3
            
    def bot2(self):
        t = 0
        bot = Bot(self.bot_cell)
        fire_cells = [self.fire_cell]
        print(Q)
        print(bot.get_pos())
        print(self.button_cell)
        disabled_cells = []
        while (bot.get_pos() != self.button_cell):
            t+=1

            if (bot.get_pos() in fire_cells):
                print("bot was consumed by fire!")
                return 1
            
            if (self.button_cell in fire_cells):
                print("button was destroyed by fire!")
                return 2
            
            step = (bfs(self.board, bot.get_pos(), self.button_cell, fire_cells) or [None, None]).pop(1)
            if step != None:
                bot.set_pos(step)
            else:
                print("No path can be found")
                return 0
            eval = []
            new_fire_cells = []
            for cell in fire_cells:
                if cell not in disabled_cells:
                    neighbours = self.board.get_open_neighbours(cell)
                    L = 0
                    for neighbour in neighbours:
                        if neighbour not in eval:
                            K = 0 
                            if neighbour in fire_cells:
                                L += 1
                                continue 
                            b_neighbours = self.board.get_open_neighbours(neighbour)
                            for b in b_neighbours:
                                if b in fire_cells:
                                    K += 1

                            if random.uniform(0,1) <= fire_spread(Q, K):
                                new_fire_cells.append(neighbour)
                                if K == len(b_neighbours):
                                    if neighbour not in disabled_cells:
                                        disabled_cells.append(neighbour)     
                            eval.append(neighbour) 

                        if neighbour in new_fire_cells:
                            L += 1
                if L == len(neighbours):
                    if cell not in disabled_cells:
                        disabled_cells.append(cell)
                
            fire_cells.extend(new_fire_cells)

            #self.board.print_sim(fire_cells,bot.get_pos(),self.button_cell)
            #input("Press eneter for to run next time step")
        if (bot.get_pos() == self.button_cell):
            print("bot got to the button and extuinguised the fire")
            return 3
        
    def bot3(self):
        t = 0
        bot = Bot(self.bot_cell)
        fire_cells = [self.fire_cell]
        print(Q)
        print(bot.get_pos())
        print(self.button_cell)
        disabled_cells = []
        cells_to_avoid = [self.fire_cell]
        cells_to_avoid.extend(self.board.get_open_neighbours(self.fire_cell))
        while (bot.get_pos() != self.button_cell):
            t+=1
            print(t)
            if (bot.get_pos() in fire_cells):
                print("bot was consumed by fire!")
                return 1
            
            if (self.button_cell in fire_cells):
                print("button was destroyed by fire!")
                return 2

            step = (bfs(self.board, bot.get_pos(), self.button_cell, cells_to_avoid) or [None, None]).pop(1)
            if step != None:
                bot.set_pos(step)
            else:
                step = (bfs(self.board, bot.get_pos(), self.button_cell, fire_cells) or [None, None]).pop(1)
                if step != None:
                    bot.set_pos(step)
                else:
                    print("No path can be found")
                    return 0
            eval = []
            new_fire_cells = []
            for cell in fire_cells:
                if cell not in disabled_cells:
                    neighbours = self.board.get_open_neighbours(cell)
                    L = 0
                    for neighbour in neighbours:
                        if neighbour not in eval:
                            K = 0 
                            if neighbour in fire_cells:
                                L += 1
                                continue 
                            b_neighbours = self.board.get_open_neighbours(neighbour)
                            for b in b_neighbours:
                                if b in fire_cells:
                                    K += 1

                            if random.uniform(0,1) <= fire_spread(Q, K):
                                new_fire_cells.append(neighbour)
                                if K == len(b_neighbours):
                                    if neighbour not in disabled_cells:
                                        disabled_cells.append(neighbour) 
                                for b in b_neighbours:
                                    if b not in cells_to_avoid and b != self.button_cell:
                                        cells_to_avoid.append(b)
                            eval.append(neighbour)

                        if neighbour in new_fire_cells:
                            L += 1
                if L == len(neighbours):
                    if cell not in disabled_cells:
                        disabled_cells.append(cell)
                
            fire_cells.extend(new_fire_cells)

            #self.board.print_sim(fire_cells,bot.get_pos(),self.button_cell)
            #input("Press eneter for to run next time step")
        if (bot.get_pos() == self.button_cell):
            print("bot got to the button and extuinguised the fire")
            return 3
    
    def bot4(self):
        t = 0
        bot = Bot(self.bot_cell)
        fire_cells = [self.fire_cell]
        disabled_cells = []
        print(Q)
        print(bot.get_pos())
        print(self.button_cell)        
        grid = cal_intensity(fire_cells)
        
        while (bot.get_pos() != self.button_cell):
            t+=1
            #print(t)
            if (bot.get_pos() in fire_cells):
                print("bot was consumed by fire!")
                return 1
            
            if (self.button_cell in fire_cells):
                print("button was destroyed by fire!")
                return 2
            
            for cell in self.board.get_closed_cells():
                x,y = cell
                grid[x][y] = -1
            
            #print(np.matrix(grid))    
            step = (a_star(grid, bot.get_pos(), self.button_cell) or [None,None]).pop(1)
            if step != None:
                bot.set_pos(step)
            else:
                print("No path can be found")
                return 0
            eval = []
            new_fire_cells = []
            
            for cell in fire_cells:
                if cell not in disabled_cells:
                    neighbours = self.board.get_open_neighbours(cell)
                    L = 0
                    for neighbour in neighbours:
                        if neighbour not in eval:
                            K = 0 
                            if neighbour in fire_cells:
                                L += 1
                                continue 
                            b_neighbours = self.board.get_open_neighbours(neighbour)
                            for b in b_neighbours:
                                if b in fire_cells:
                                    K += 1

                            if random.uniform(0,1) <= fire_spread(Q, K):
                                new_fire_cells.append(neighbour)
                                if K == len(b_neighbours):
                                    if neighbour not in disabled_cells:
                                        disabled_cells.append(neighbour)     
                            eval.append(neighbour) 

                        if neighbour in new_fire_cells:
                            L += 1
                if L == len(neighbours):
                    if cell not in disabled_cells:
                        disabled_cells.append(cell)
                
            fire_cells.extend(new_fire_cells)

            grid = cal_intensity(fire_cells)
        if (bot.get_pos() == self.button_cell):
            print("bot got to the button and extuinguised the fire")
            return 3
            
    def new_sim(self, bot_cell, fire_cell, button_cell):
        self.bot_cell = bot_cell
        self.fire_cell = fire_cell
        self.button_cell = button_cell
    
    
    


board = Board(D)
board.open_ship()
board.clear_dead_cells()
open_cells = board.get_open_cells()
board.print_ship()
sim = Sim(random.choice(open_cells),random.choice(open_cells),random.choice(open_cells), board)
# sim = Sim((9,5),(6,8),(1,9),board)

# results = [[0]*50 for i in range(10)]
# for i in range (1,11):
#     Q = i/10 #q value
#     for j in range (50): #50 sims
#         sim.new_sim(random.choice(open_cells),random.choice(open_cells),random.choice(open_cells))
#         results[i-1][j] = sim.bot4()
        
# for row in results:
#     for col in row:
#         print(col, end = "")
#     print()
    
Q= 0.7
# sim.bot4()

result = []
for i in range (100):
    sim.new_sim(random.choice(open_cells),random.choice(open_cells),random.choice(open_cells))
    result.append(sim.bot4())
print(result)