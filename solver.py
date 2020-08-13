board = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]]

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

    return False

#could also return first/ all cell that conflict occurs with
def valid(bo, row, col, val):
    #check box for to see if val already exists
    xbox = row // 3
    ybox = col // 3

    for i in range(xbox * 3, xbox * 3 + 3):
        for j in range(ybox * 3, ybox * 3 + 3):
            if (i, j) != (row, col) and bo[i][j] == val:
                return False
    
    #for i in list(range(xbox * 3) + range(xbox * 3 + 4, len(bo))): # might allow me to cut down 6 calculations evey iteration but severely affects readability
    
    #checks row and col to see if val already exists
    for i in range(len(bo)):
        if i != row and bo[i][col] == val:
            return False
        elif i!= col and bo[row][i] == val:
            return False

    #if no matches are found
    return True 


def solve(bo):
    show(board)
    loc = find_empty(bo) #finds location of next empty cell
    if loc: 
        row, col = loc
        print(row, col)
        # start solving.
        for n in range(1, len(bo) + 1): 
            if valid(bo, row, col, n):
                bo[row][col] = n
                solve(bo)
        bo[row][col] = 0
        return 
    else:
        return








#show(board)
solve(board)
#print(valid(board, 0, 0, 3))
#show(board)
#print('puzzle solved!')