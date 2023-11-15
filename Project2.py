import random
import heapq
import math
from decimal import *
import numpy as np
from collections import deque
import sys


sys.setrecursionlimit(1500)
getcontext().prec = 50
random.seed(150)
D = 50
#K = 1
#alpha = 0.3


class Board():
    
    def __init__(self, D): #initialises ship to set row and col value
        self.D = D
        self.board = [[False for i in range (D)] for j in range (D)] #creation of ship
        self.cell = [random.randrange(1, D-1) for i in range (2)]
        self.board[self.cell[0]][self.cell[1]] = True
        self.open_cells = [self.cell]

    #method to return surrounding blocked cells of a cell
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
    
    #method to return surrounding open cells of a cell
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
    
    #method to create ship
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
    
    #method to return all open cells in the ship
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
    
    #method to return all closed cells in the ship
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
    
    def get_cell_value(self, cell):
        x, y = cell
        return self.board[x][y]
        
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
        
    # prints the ship to show where fire_cells, bot and button are located
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
    
    def get_pos(self): # returns position
        cell = (self.row, self.col)
        return cell
    
    def set_pos(self, cell): # set's position
        self.row = cell[0]
        self.col = cell[1]

def DFS(start, visited, board, t):
    
    visited[start] = t
    neighbours = board.get_open_neighbours(start)
    for x in neighbours:
        if x not in visited:
            t += 1
            t, visited = DFS(x, visited, board, t)
    t += 1
    return t, visited

def BFS(start, goal_locations, board):
    isVisited = [[False for i in range (D)] for j in range (D)]
    isVisited[start[0]][start[1]] = True
    queue = deque()
    queue.append(start)
    parent_to_cell = {start : None}      
    
    while queue:
        cell = queue.popleft()
        if cell in goal_locations:
            break
        neighbours = board.get_open_neighbours(cell)
        for neighbour in neighbours:
            if isVisited[neighbour[0]][neighbour[1]] == False:
                isVisited[neighbour[0]][neighbour[1]] = True
                queue.append(neighbour)
                parent_to_cell[neighbour] = cell
                
    if cell not in goal_locations:  # If destination wasn't reached.
        return None
    
    path = []
    while cell:
        path.append(cell)
        cell = parent_to_cell[cell]
    
    return path[::-1]

def detection_square(cell):
    list = []
    x1,y1 = cell
    for x in range (x1-K, (x1+K+1)):
        for y in range (y1-K, (y1+K+1)):
            if 0 <= x < D and 0 <= y < D:
                list.append((x,y))
    return list

def calculate_distances(grid, source):
    rows = D
    cols = D
    distances = [[-1] * cols for _ in range(rows)]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Up, Down, Left, Right
    queue = deque()
    queue.append(source)
    distances[source[0]][source[1]] = 0  # Distance to the source is 0

    while queue:
        x, y = queue.popleft()

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < rows and 0 <= new_y < cols and distances[new_x][new_y] == -1 and grid.get_cell_value((new_x,new_y)) == True:
                distances[new_x][new_y] = distances[x][y] + 1
                queue.append((new_x, new_y))

    return distances

def sense(distance):
    probability_beep = math.exp(-alpha * (distance - 1))
    return (random.random() < probability_beep)

def sense_two_leaks(distance1, distance2):
    beep_probablity_1 = math.exp(-alpha * (distance1 - 1))
    beep_probablity_2 = math.exp(-alpha * (distance2 - 1))
    beep_1 = random.random() < beep_probablity_1
    beep_2 = random.random() < beep_probablity_2
    return(beep_1 or beep_2)
    
def move(move_cost, probablity_matrix):
    max_cost = 99999
    b_cell = None
    maxval = None
    for x, row in enumerate(probablity_matrix):
        for y, val in enumerate(row):
            if maxval is None or val > maxval:
                indices = [(x,y)]
                maxval = val
            elif val == maxval:
                indices.append((x,y))
    
    for cell in indices:
        if move_cost[cell[0]][cell[1]] < max_cost:
            max_cost = move_cost[cell[0]][cell[1]]
            b_cell = cell
        elif move_cost[cell[0]][cell[1]] == max_cost:
            if random.random() < 0.5:
                b_cell = cell
    
    return b_cell

def improved_move(move_cost, probability_matrix): #write a condition for equal combined score
    max_combined_score = -1
    next_cell = None
    
    for x in range(D):
        for y in range(D):
            if probability_matrix[x][y] > 0:  # Consider only cells with non-zero probability
                distance = move_cost[x][y]
                probability = probability_matrix[x][y]
                
                # Experiment with different weightings for distance and probability
                combined_score = 0.8 * distance + 5 * probability
                
                if combined_score > max_combined_score:
                    max_combined_score = combined_score
                    next_cell = (x, y)
    
    return next_cell

def beep_update(move_cost, probablity_mat):
    new_matrix = [[0 for j in range(D)] for i in range(D)]
    
    p_beep = sum((probablity_mat[a][b] * math.exp(-alpha * (move_cost[a][b] - 1))) 
                 for a in range (D) for b in range (D))
    
    for x,row in enumerate(probablity_mat):
        for y,cell in enumerate(row):
            if cell != 0:
                p_beep_leak = math.exp(-alpha * (move_cost[x][y] - 1))
                new_matrix[x][y] = ((cell * p_beep_leak) / p_beep)
     
    return new_matrix

def no_beep_update(move_cost, probablity_mat):
    new_matrix = [[0 for j in range(D)] for i in range(D)]
    
    p_beep = sum((probablity_mat[a][b] * math.exp(-alpha * (move_cost[a][b] - 1)))
                 for a in range (D) for b in range (D))
    
    p_no_beep = 1-p_beep
    
    for x,row in enumerate(probablity_mat):
        for y,cell in enumerate(row):
            if cell != 0 and move_cost[x][y] != 0:
                p_beep_leak = 1 - (math.exp(-alpha * (move_cost[x][y] - 1)))
                new_matrix[x][y] = (cell * p_beep_leak) / p_no_beep     
    return new_matrix

def bot_movement_update(probablity_mat, bot_pos):
    new_matrix = [[0 for j in range(D)] for i in range(D)]
    p_x, p_y = bot_pos
    p = probablity_mat[p_x][p_y]
    
    for x,row in enumerate(probablity_mat):
        for y,cell in enumerate(row):
            new_matrix[x][y] = cell/(1-p)
    
    new_matrix[p_x][p_y] = 0
            
    return new_matrix

class Part1():
    def __init__(self, bot_cell, leak_cell, board): #initialising values
        self.bot_cell = bot_cell
        self.leak_cell = leak_cell
        self.board = board
    
    def Bot1(self):
        path = {}
        senses = 0
        moves = 0
        t = 0
        p_leak_locations = []
        detection_grid = [[0 for i in range (D)] for j in range (D)]
        leak_detected = False
        bot = Bot(self.bot_cell)
        final_t, visited_nodes = DFS(self.bot_cell, path, self.board, t)
        path = list(visited_nodes.keys())
        path_of_bot = []
        while (leak_detected != True):
            bot.set_pos(path.pop(0))
            path_of_bot.append(bot.get_pos())
            
            cells = detection_square(bot.get_pos())
            for cell in cells:
                if self.board.get_cell_value(cell) == False:
                    cells.remove(cell)

            if self.leak_cell in cells:
                for cell in cells:
                    if detection_grid[cell[0]][cell[1]] == 0 and cell != bot.get_pos():
                        detection_grid[cell[0]][cell[1]] = 2
                        p_leak_locations.append(cell)
                leak_detected = True
            else:
                for cell in cells:
                    detection_grid[cell[0]][cell[1]] = 1
            senses += 1
        moves = visited_nodes[bot.get_pos()]
            
        while (True):
            path = BFS(bot.get_pos(), p_leak_locations, self.board)
            bot.set_pos(path.pop(-1))
            moves += len(path)
            path_of_bot.append(bot.get_pos())
            if self.leak_cell != bot.get_pos():
                p_leak_locations.remove(bot.get_pos())
            else:
                break
        
        t = moves + senses
    
        print(f"bot found leak at {bot.get_pos()} after {t} steps")
    
    def Bot2(self):          
        path = {}
        senses = 0
        moves = 0
        t = 0
        p_leak_locations = []
        detection_grid = [[0 for i in range (D)] for j in range (D)]
        leak_detected = False
        bot = Bot(self.bot_cell)
        final_t, visited_nodes = DFS(self.bot_cell, path, self.board, t)
        path = list(visited_nodes.keys())
        path_of_bot = []
        while (leak_detected != True):
            while(True):
                move_cell = path.pop(0)
                if detection_grid[move_cell[0]][move_cell[1]] != 1:
                    bot.set_pos(move_cell)
                    path_of_bot.append(bot.get_pos())
                    moves += len(BFS(bot.get_pos(), [move_cell], self.board))
                    break
            
            cells = detection_square(bot.get_pos())
            for cell in cells:
                if self.board.get_cell_value(cell) == False:
                    cells.remove(cell)

            if self.leak_cell in cells:
                for cell in cells:
                    if detection_grid[cell[0]][cell[1]] == 0:
                        detection_grid[cell[0]][cell[1]] = 2
                        p_leak_locations.append(cell)
                leak_detected = True
            else:
                for cell in cells:
                    detection_grid[cell[0]][cell[1]] = 1
            senses += 1
        
        while (True):
            path = BFS(bot.get_pos(), p_leak_locations, self.board)
            bot.set_pos(path.pop(-1))
            moves += len(path)
            path_of_bot.append(bot.get_pos())
            if self.leak_cell != bot.get_pos():
                p_leak_locations.remove(bot.get_pos())
            else:
                break
        
        t = moves + senses
    
        print(f"bot found leak at {bot.get_pos()} after {t} steps")
            
class Part2():
    def __init__(self, bot_cell, leak_cell, board): #initialising values
        self.bot_cell = bot_cell
        self.leak_cell = leak_cell
        self.board = board
        
    def Bot3(self):
        t = 0
        bot = Bot(self.bot_cell)
        len_open_cells = len(self.board.get_open_cells())
        probabilities = [[0.0 if self.board.get_cell_value((i,j)) == False 
                          else 1 / len_open_cells for j in range(D)] for i in range(D)]
        
        while (True):
            move_cost = calculate_distances(self.board, bot.get_pos())
            distance_to_leak = move_cost[self.leak_cell[0]][self.leak_cell[1]]
            probabilities = bot_movement_update(probabilities, bot.get_pos())
            
            if sense(distance_to_leak):
                probabilities = beep_update(move_cost, probabilities)     
            else:
                probabilities = no_beep_update(move_cost, probabilities)
            t += 1
                
            move_cell = move(move_cost, probabilities)
            
            planned_path = BFS(bot.get_pos(), [move_cell], self.board)
            planned_path.pop(0)
            
            t += len(planned_path) - 1
            
            for i in planned_path:
                if i == self.leak_cell:
                    bot.set_pos(i)
                    return t
                else:
                    probabilities = bot_movement_update(probabilities, i)
                
            bot.set_pos(planned_path.pop(-1))
               
    def Bot4(self):
        t = 0
        bot = Bot(self.bot_cell)
        len_open_cells = len(self.board.get_open_cells())
        probabilities = [[0 if self.board.get_cell_value((i,j)) == False 
                          else 1 / len_open_cells for j in range(D)] for i in range(D)]
        
        while (True):
            move_cost = calculate_distances(self.board, bot.get_pos())
            distance_to_leak = move_cost[self.leak_cell[0]][self.leak_cell[1]]
            probabilities = bot_movement_update(probabilities, bot.get_pos())
            
            
            sense_list = []
            for i in range(4):
                sense_list.append(sense(distance_to_leak))
                t += 1
                
            senses = sense_list.count(True)
            
            if senses > 0:
                probabilities = beep_update(move_cost, probabilities)     
            else:
                probabilities = no_beep_update(move_cost, probabilities)
                
            move_cell = move(move_cost, probabilities)
            move_cell2 = improved_move(move_cost, probabilities)
            
            planned_path = BFS(bot.get_pos(), [move_cell], self.board)
            planned_path.pop(0)
            
            t += len(planned_path) - 1
            
            for i in planned_path:
                if i == self.leak_cell:
                    bot.set_pos(i)
                    return t
                else:
                    probabilities = bot_movement_update(probabilities, i)
            
            bot.set_pos(planned_path.pop(-1))
            
class Part3():
    def __init__(self, bot_cell, first_leak_cell, second_leak_cell, board): #initialising values
        self.bot_cell = bot_cell
        self.first_leak_cell = first_leak_cell
        self.second_leak_cell = second_leak_cell
        self.board = board
        
    def Bot5(self):
        path = {}
        senses = 0
        moves = 0
        t = 0
        p_leak_locations = []
        leaks = [self.first_leak_cell, self.second_leak_cell]
        detection_grid = [[0 for i in range (D)] for j in range (D)]
        bot = Bot(self.bot_cell)
        final_t, visited_nodes = DFS(self.bot_cell, path, self.board, t)
        path = list(visited_nodes.keys())
        path_of_bot = []
        while (True):
            bot.set_pos(path.pop(0))
            path_of_bot.append(bot.get_pos())
            
            cells = detection_square(bot.get_pos())
            for cell in cells:
                if self.board.get_cell_value(cell) == False:
                    cells.remove(cell)

            if any(i in cells for i in leaks):
                for cell in cells:
                    if detection_grid[cell[0]][cell[1]] == 0 and cell != bot.get_pos():
                        detection_grid[cell[0]][cell[1]] = 2
                        p_leak_locations.append(cell)
                break
            else:
                for cell in cells:
                    detection_grid[cell[0]][cell[1]] = 1
            senses += 1
        moves = visited_nodes[bot.get_pos()]
            
        while (len(p_leak_locations)!=0):
            grid_path = BFS(bot.get_pos(), p_leak_locations, self.board)
            bot.set_pos(grid_path.pop(-1))
            moves += len(grid_path)
            path_of_bot.append(bot.get_pos())
            if all(i != bot.get_pos() for i in leaks):
                p_leak_locations.remove(bot.get_pos())
            else:
                leaks.remove(bot.get_pos())
        
        moves += len(BFS(bot.get_pos(), [path[0]], self.board)) - 1
        
        while (True):
            bot.set_pos(path.pop(0))
            path_of_bot.append(bot.get_pos())
            
            cells = detection_square(bot.get_pos())
            for cell in cells:
                if self.board.get_cell_value(cell) == False:
                    cells.remove(cell)

            if any(i in cells for i in leaks):
                p_leak_locations = []
                for cell in cells:
                    if detection_grid[cell[0]][cell[1]] == 0 and cell != bot.get_pos():
                        detection_grid[cell[0]][cell[1]] = 2
                        p_leak_locations.append(cell)
                break
            else:
                for cell in cells:
                    detection_grid[cell[0]][cell[1]] = 1
            senses += 1
        moves = visited_nodes[bot.get_pos()]
        
        while (True):
            grid_path = BFS(bot.get_pos(), p_leak_locations, self.board)
            bot.set_pos(grid_path.pop(-1))
            moves += len(grid_path)
            path_of_bot.append(bot.get_pos())
            if all(i != bot.get_pos() for i in leaks):
                p_leak_locations.remove(bot.get_pos())
            else:
                leaks.remove(bot.get_pos())
                break
        t = moves + senses
    
        print(f"bot found leaks after {t} steps")
        
    def Bot6(self):      
        path = {}
        senses = 0
        moves = 0
        t = 0
        p_leak_locations = []
        leaks = [self.first_leak_cell, self.second_leak_cell]
        detection_grid = [[0 for i in range (D)] for j in range (D)]
        bot = Bot(self.bot_cell)
        final_t, visited_nodes = DFS(self.bot_cell, path, self.board, t)
        path = list(visited_nodes.keys())
        path_of_bot = []
        while (True):
            while(True):
                move_cell = path.pop(0)
                if detection_grid[move_cell[0]][move_cell[1]] != 1:
                    bot.set_pos(move_cell)
                    path_of_bot.append(bot.get_pos())
                    moves += len(BFS(bot.get_pos(), [move_cell], self.board))
                    break
            
            cells = detection_square(bot.get_pos())
            for cell in cells:
                if self.board.get_cell_value(cell) == False:
                    cells.remove(cell)

            if any(i in cells for i in leaks):
                if any(i == bot.get_pos() for i in leaks):
                    leaks.remove(bot.get_pos())
                    senses += 1
                    break
                for cell in cells:
                    if detection_grid[cell[0]][cell[1]] == 0 and cell != bot.get_pos():
                        detection_grid[cell[0]][cell[1]] = 2
                        p_leak_locations.append(cell)
                break
            else:
                for cell in cells:
                    detection_grid[cell[0]][cell[1]] = 1
            senses += 1
        
        while (len(p_leak_locations)!=0):
            grid_path = BFS(bot.get_pos(), p_leak_locations, self.board)
            bot.set_pos(grid_path.pop(-1))
            moves += len(grid_path)
            path_of_bot.append(bot.get_pos())
            if all(i != bot.get_pos() for i in leaks):
                p_leak_locations.remove(bot.get_pos())
            else:
                leaks.remove(bot.get_pos())
        
        
        while (True):
            while(True):
                move_cell = path.pop(0)
                if detection_grid[move_cell[0]][move_cell[1]] != 1:
                    bot.set_pos(move_cell)
                    path_of_bot.append(bot.get_pos())
                    moves += len(BFS(bot.get_pos(), [move_cell], self.board))
                    break
            
            cells = detection_square(bot.get_pos())
            for cell in cells:
                if self.board.get_cell_value(cell) == False:
                    cells.remove(cell)

            if any(i in cells for i in leaks):
                p_leak_locations = []
                for cell in cells:
                    if detection_grid[cell[0]][cell[1]] == 0:
                        detection_grid[cell[0]][cell[1]] = 2
                        p_leak_locations.append(cell)
                break
            else:
                for cell in cells:
                    detection_grid[cell[0]][cell[1]] = 1
            senses += 1
        
        while (True):
            path = BFS(bot.get_pos(), p_leak_locations, self.board)
            bot.set_pos(path.pop(-1))
            moves += len(path)
            path_of_bot.append(bot.get_pos())
            if all(i != bot.get_pos() for i in leaks):
                p_leak_locations.remove(bot.get_pos())
            else:
                leaks.remove(bot.get_pos())
                break
        
        t = moves + senses
    
        print(f"bot found leaks after {t} steps")
        
    def Bot7(self):
        t = 0
        bot = Bot(self.bot_cell)
        total_leaks_found = 0
        leak = [self.first_leak_cell, self.second_leak_cell]
        len_open_cells = len(self.board.get_open_cells())
        probabilities = [[Decimal('0.0') if self.board.get_cell_value((i,j)) == False 
                          else 1 / Decimal(str(len_open_cells)) for j in range(D)] for i in range(D)]
        
        while (total_leaks_found<2):
            move_cost = calculate_distances(self.board, bot.get_pos())
            distance_to_first_leak = move_cost[self.first_leak_cell[0]][self.first_leak_cell[1]]
            distance_to_second_leak = move_cost[self.second_leak_cell[0]][self.second_leak_cell[1]]
            probabilities = bot_movement_update(probabilities, bot.get_pos())
            
            if sense_two_leaks(distance_to_first_leak, distance_to_second_leak):
                probabilities = beep_update(move_cost, probabilities, 1)     
            else:
                probabilities = no_beep_update(move_cost, probabilities)
            t += 1
                
            move_cell = move(move_cost, probabilities)
            
            planned_path = BFS(bot.get_pos(), [move_cell], self.board)
            planned_path.pop(0)
            
            t += len(planned_path) - 1
            
            for i in planned_path:
                if any(i in [leak]):
                    leak.remove(i)
                    total_leaks_found += 1
                    probabilities = bot_movement_update(probabilities, i)
                    if total_leaks_found == 2:
                        bot.set_pos(i)
                else:
                    probabilities = bot_movement_update(probabilities, i)
                
            bot.set_pos(planned_path.pop(-1))        
        
    

x = input( 
'''1: Bot 1 and 2
2: Bot 3 and 4
3: Bot 5 and 6
4: Bot 7 and 8 and 9
Choose a number: 
''')
x = int(x)
if (x == 1):
    for K in range (0,8,2):
        K = K
        print(K)
        t_total = 0
        for i in range(500): #change for total trials
            if i%100 == 0:
                board = Board(D)
                board.open_ship()
                board.clear_dead_cells()
            open_cells = board.get_open_cells()
            bot_location = random.choice(open_cells)
            open_cells.remove(bot_location)
            leak_locaion = random.choice(open_cells)
            part1 = Part1(bot_location, leak_locaion, board)
            t = part1.Bot1()
            t_total += t
            
            print(f"{i+1}: {t}    avg steps: {t_total/(i+1)}")
            
if (x==2):
    for a in range (50,100,10):
        alpha = a/1000
        print(alpha)
        t1_total = 0
        t2_total = 0
        for i in range(500): #change for total trials
            if i%100 == 0:
                board = Board(D)
                board.open_ship()
                board.clear_dead_cells()
            open_cells = board.get_open_cells()
            bot_location = random.choice(open_cells)
            open_cells.remove(bot_location)
            leak_locaion = random.choice(open_cells)
            part2 = Part2(bot_location, leak_locaion, board)
            t1 = part2.Bot3()
            t2 = part2.Bot4()
            t1_total += t1
            print(f"{i+1}: {t1}    avg steps: {t1_total/(i+1)}") 
            t2_total += t2
            print(f"{i+1}: {t2}    avg steps: {t2_total/(i+1)}") 

if(x==3):
    for K in range (0,8,2):
        K = K
        print(K)
        t1_total = 0
        t2_total = 0
        for i in range(500): #change for total trials
            if i%100 == 0:
                board = Board(D)
                board.open_ship()
                board.clear_dead_cells()
            open_cells = board.get_open_cells()
            bot_location = random.choice(open_cells)
            open_cells.remove(bot_location)
            first_leak_locaion = random.choice(open_cells)
            open_cells.remove(first_leak_locaion)
            second_leak_location = random.choice(open_cells)
            part3 = Part3(bot_location, first_leak_locaion, second_leak_location, board)
            t1 = part3.Bot5()
            t2 = part3.Bot6()
            t1_total += t1
            print(f"{i+1}: {t1}    avg steps: {t1_total/(i+1)}") 
            t2_total += t2
            print(f"{i+1}: {t2}    avg steps: {t2_total/(i+1)}") 
             
            
            
#part2.Bot3()
#part2.Bot4()
#part3 = Part3(random.choice(open_cells), random.choice(open_cells), random.choice(open_cells), board)
#part3.Bot5()
#part3.Bot6()
#part3.Bot7()