import random

D = 100 #number of rows, cols in the ship grid
board = [[False for i in range (D)] for j in range (D)] #creation of ship

cell = [random.randrange(1, D-1) for i in range (2)]
board[cell[0]][cell[1]] = True
open_cells = [cell]

#method to get neighbours of an opened cell
def get_neighbours(cell,arr):
    list = []
    row, col = cell[0], cell[1]
    if row != 0 and arr[row-1][col] != True:
        list.append([row-1,col])
    if col+1 != len(arr[0]) and arr[row][col+1] != True:
        list.append([row, col+1])
    if row+1 != len(arr) and arr[row+1][col] != True:
        list.append([row+1, col])
    if col != 0 and arr[row][col-1] != True:
        list.append([row, col-1])
    return list

#method to add two neighbour cells list together
def extend_list(arr1, arr2, arr3):
    for item in arr2[::-1]:
        if item in arr1:
            arr1.remove(item)
            arr3.append(item)
        if item in arr3:
            arr2.remove(item)
    arr1.extend(arr2)
    return arr1, arr3

cells_avail_to_open = []
banned_cells = []

while True: #loop keeps opening cells until there are no more to open
    list = get_neighbours(cell, board)

    cells_avail_to_open, banned_cells = extend_list(cells_avail_to_open, list, banned_cells)
    if len(cells_avail_to_open) == 0:
        break
    cell = random.choice(cells_avail_to_open)
    cells_avail_to_open.remove(cell)
    board[cell[0]][cell[1]] = True
    open_cells.append(cell)
    if len(cells_avail_to_open) == 0:
        break


dead_cells_dup = []
dead_cells = []
for cell in open_cells: #adds deadcells to a list
    x, y = cell[0], cell[1]
    if x!=0 and x!= (D-1) and y!=0 and y!=(D-1):
        if len(get_neighbours(cell, board)) == 3:
            dead_cells_dup.append(cell)
    else:
        if len(get_neighbours(cell, board)) == 2:
             dead_cells_dup.append(cell)

[dead_cells.append(x) for x in dead_cells_dup if x not in dead_cells]

i = int(len(dead_cells)/2)
while(i>0 and len(dead_cells)!=0):
    while True:
        cell = random.choice(dead_cells)
        list = get_neighbours(cell, board)
        if len(list) != 0: 
            delete_cell = random.choice(list)
            board[delete_cell[0]][delete_cell[1]] = True
            dead_cells.remove(cell)
            i -= 1
            break
        else:
            if len(dead_cells) > 1:
                dead_cells.remove(cell)
                continue
        break


#board printer    
for row in board:
    for col in row:
        if col is True:
            print("x", end="")
        else:
            print("o", end="")
    print()