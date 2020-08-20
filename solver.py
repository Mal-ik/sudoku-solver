import pygame
from sys import exit
import time

# Set to False to drastically increase solve speed
visuals = True


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
            # index comparison with row, col is necessary for app_class checkAllCells()
            if (xbox + i, ybox + j) != (row, col) and bo[xbox + i][ybox + j] == val:
                return False

    # checks row and col to see if val already exists
    for i in range(len(bo)):
        if (i != row and bo[i][col] == val) or (i != col and bo[row][i] == val):
            return False

    # if no matches are found
    return True


temp = 0


# vuild whole funnciton here but set a default value for iniital cordinates to ocntinue from when finding empty vars
def solve(bo, draw, incorrect, valList, length, diff, row=0):
    # pygame.event.pump()  # not necessary because for loop after it checks for every event
    # allows us to leave game at any time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for i in range(row, len(bo)):
        for j in range(len(bo)):
            if bo[i][j] == 0:
                for x in range(1, len(bo) + 1):
                    if valid(bo, i, j, x):
                        # turns current cell green
                        bo[i][j] = x
                        valList.append([i, j])

                        # just comment this out to solve boards instantly
                        if visuals and abs(len(valList) - length) > diff:
                            draw()
                            length = len(valList)

                        try:
                            incorrect.remove([i, j])
                        except:
                            pass

                        # checks if updated board and is solvable
                        if solve(bo, draw, incorrect, valList, length, i):
                            return True
                        incorrect.append(valList.pop())
                # reset value if dead end - could also put in if cond. but doesnt matter because new x wont conflict w previous
                bo[i][j] = 0
                return False
    return True  # if no empty cell found

   # if you want the option of seeing more solutions
"""    global more
    more = input('look for more? (Y for yes):')
    if more.lower() == 'y':
        print('searching ...')
        return False 
    return True  """
