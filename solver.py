board = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]]

board1= [[0, 2, 0, 6, 0, 8, 0, 0, 0],
    [5, 8, 0, 0, 0, 9, 7, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [3, 7, 0, 0, 0, 0, 5, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 8, 0, 0, 0, 0, 1, 3],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 9, 8, 0, 0, 0, 3, 6],
    [0, 0, 0, 3, 0, 6, 0, 9, 0]]

board2= [[0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 3],
    [0, 7, 4, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 0, 2],
    [0, 8, 0, 0, 4, 0, 0, 1, 0],
    [6, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 7, 8, 0],
    [5, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0]]

def show(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print ('---------------------')  
        
        for j in range(len(bo)):

            if j % 3 == 0 and j != 0:
                print ("| ",end='')

            if j == 8:
                print(bo[i][j])
            else:
                print(bo[i][j], end=' ')
    print ('=====================') 
  
def find_empty(bo): #takes board and current row
    for i in range(len(bo)): #starts checking from current row so as not to go over already checked rows
        for j in range(len(bo)):
            if bo[i][j] == 0:
                return (i, j)

    return (-1, -1) #simplifies stuff in solve()

#could also return first/ all cell that conflict occurs with
def valid(bo, row, col, val):
    #check box for to see if val already exists
    xbox = row // 3
    ybox = col // 3

    for i in range(xbox * 3, xbox * 3 + 3):
        for j in range(ybox * 3, ybox * 3 + 3):
            if (i, j) != (row, col) and bo[i][j] == val:
                return False
    
    #checks row and col to see if val already exists
    for i in range(len(bo)):
        if i != row and bo[i][col] == val:
            return False
        elif i!= col and bo[row][i] == val:
            return False

    #if no matches are found
    return True 

temp = 0
def solve(bo):
    global temp
    temp += 1
    show(bo)
    row, col = find_empty(bo) #finds location of next empty cell
    if row > - 1:
        print(row, col)

        # start solving.
        for n in range(1, len(bo) + 1): 
            if valid(bo, row, col, n):
                bo[row][col] = n
                solve(bo)

            if find_empty(bo)[0] == -1 :
                return 

        bo[row][col] = 0
        return 
    else:
        return
    









#show(board1)
solve(board1)
print(temp)
temp = 0
