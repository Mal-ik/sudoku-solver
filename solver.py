import time

board = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
         [6, 8, 0, 0, 7, 0, 0, 9, 0],
         [1, 9, 0, 0, 0, 4, 5, 0, 0],
         [8, 2, 0, 1, 0, 0, 0, 4, 0],
         [0, 0, 4, 6, 0, 2, 9, 0, 0],
         [0, 5, 0, 0, 0, 3, 0, 2, 8],
         [0, 0, 9, 3, 0, 0, 0, 7, 4],
         [0, 4, 0, 0, 5, 0, 0, 3, 6],
         [7, 0, 3, 0, 1, 8, 0, 0, 0]]

board1 = [[0, 2, 0, 6, 0, 8, 0, 0, 0],
          [5, 8, 0, 0, 0, 9, 7, 0, 0],
          [0, 0, 0, 0, 4, 0, 0, 0, 0],
          [3, 7, 0, 0, 0, 0, 5, 0, 0],
          [6, 0, 0, 0, 0, 0, 0, 0, 4],
          [0, 0, 8, 0, 0, 0, 0, 1, 3],
          [0, 0, 0, 0, 2, 0, 0, 0, 0],
          [0, 0, 9, 8, 0, 0, 0, 3, 6],
          [0, 0, 0, 3, 0, 6, 0, 9, 0]]

board2 = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 6, 0, 0, 0, 0, 3],
          [0, 7, 4, 0, 8, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 3, 0, 0, 2],
          [0, 8, 0, 0, 4, 0, 0, 1, 0],
          [6, 0, 0, 5, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 0, 7, 8, 0],
          [5, 0, 0, 0, 0, 9, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 4, 0]]

# generates a sudoku puzzle


def gen_board():
    pass
    # choose valid numbers for each cell by making it choose out of (1..9) - (box) - (row) - (col)
    # randomly take some numbers out and save solution in case


def show(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print('---------------------')

        for j in range(len(bo)):

            if j % 3 == 0 and j != 0:
                print("| ", end='')

            if j == 8:
                print(bo[i][j])
            else:
                print(bo[i][j], end=' ')
    print('=====================')


def valid(bo, row, col, val):
    # find "box coordinates"
    xbox = (row // 3) * 3
    ybox = (col // 3) * 3

    # check box for value
    for i in range(3):
        for j in range(3):
            if bo[xbox + i][ybox + j] == val:
                return False

    # checks row and col to see if val already exists
    for i in range(len(bo)):
        if bo[i][col] == val or bo[row][i] == val:
            return False

    # if no matches are found
    return True


temp = 0


def solve(bo, row=0):  # vuild whole funnciton here but set a default value for iniital cordinates to ocntinue from when finding empty vars
    global temp
    for i in range(row, len(bo)):
        for j in range(len(bo)):
            if bo[i][j] == 0:
                for x in range(1, len(bo) + 1):
                    temp += 1
                    if valid(bo, i, j, x):
                        bo[i][j] = x
                        if solve(bo, i):  # checks if updated board and row is solvable
                            return True

                # reset value if dead end - could also put in if cond. but doesnt matter because new x wont conflict w previous
                bo[i][j] = 0
                return False
    show(bo)
   # print(f"Process took {temp} steps and finished in {time.time() - start_time} seconds")
    global more
    more = input('look for more? (Y for yes):')
    if more.lower() == 'y':
        print('searching ...')
        return False
    return True  # if no empty cells found
    # input('more?')  # can be used if there is more than one solution


"""# show(board1)
start_time = time.time()
show(board2)
solve(board2)
if(more.lower() == 'y'):
    print('no more possible solutions')"""
