import random
import math
a = 100
#test to check push
rows, cols = (a, a)
board = [[False for i in range (cols)] for j in range (rows)]

cell = [random.randrange(1, rows-1) for i in range (2)]
board[cell[0]][cell[1]] = True
open_cells = [cell]
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
while True:
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
for cell in open_cells:
    if len(get_neighbours(cell, board)) == 3:
        dead_cells_dup.append(cell)
print (f"initial: {dead_cells_dup}")

[dead_cells.append(x) for x in dead_cells_dup if x not in dead_cells]
print (f"initial: {dead_cells}")
for i in range(math.floor(len(dead_cells)/2)):
    dead_cells.remove(random.choice(dead_cells))

print (f"initial: {dead_cells}")

for cell in dead_cells:
    list = get_neighbours(cell, board)
    delete_cell = random.choice(list)
    board[delete_cell[0]][delete_cell[1]] = True
    
for row in board:
    for col in row:
        if col is True:
            print("x", end="")
        else:
            print("o", end="")
    print()