from random import *
from graphics import *

def main():
    win = GraphWin("Minesweeper", 160, 210)
    
    #Variables
    matrix = []
    h = 9      #!
    w = 9      #!   Needs Level Set
    bombs = 9  #!
        
    #Methods
    initBoard(matrix, w, h)
    addBombs(matrix, bombs, w, h)
    addNumbers(matrix, w, h)
    
    #Print game to screen
    for i in range(len(matrix)):
        print(matrix[i])
        
        

##  All methods below this  ##

def initBoard(matrix, w, h):
    for i in range(h):
        matrix.append([" "] * w)

def addBombs(matrix, bombs, w, h):
    for i in range(bombs):
        y = randint(0, h)-1
        x = randint(0, w)-1
        while matrix[y][x] == "b":
            y = randint(0, h)-1
            x = randint(0, w)-1
        matrix[y][x] = "b"
        
def addNumbers(matrix, w, h):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == " ":
                matrix[i][j] = checkAround(matrix, i, j, w, h)
            
def checkAround(matrix, y, x, w, h):
    bombsFound = 0
    w = w-1
    h = h-1
    
    if x > 0 and x < w:
        if y == 0:
            bombsFound += topCheck(matrix, y, x)
        elif y == h:
            bombsFound += bottomCheck(matrix, y, x)
        else:
            bombsFound += fullCheck(matrix, y, x)
    else:
        if y == 0:
            if x == 0:
                bombsFound += topLeftCheck(matrix, y, x)
            else:
                bombsFound += topRightCheck(matrix, y, x)
        elif y == h:
            if x == 0:
                bombsFound += bottomLeftCheck(matrix, y, x)
            else:
                bombsFound += bottomRightCheck(matrix, y, x)
        else:
            if x == 0:
                bombsFound += leftCheck(matrix, y, x)
            else:
                bombsFound += rightCheck(matrix, y, x)
            
    return str(bombsFound)
            
def topCheck(matrix, i, j):
    return Check(matrix, i, j, 0, 2, -1, 2)
    
def bottomCheck(matrix, i, j):
    return Check(matrix, i, j, -1, 1, -1, 2)
    
def leftCheck(matrix, i, j):
    return Check(matrix, i, j, -1, 2, 0, 2)
    
def rightCheck(matrix, i, j):
    return Check(matrix, i, j, -1, 2, -1, 1)
    
def topLeftCheck(matrix, i, j):
    return Check(matrix, i, j, 0, 2, 0, 2)
    
def topRightCheck(matrix, i, j):
    return Check(matrix, i, j, 0, 2, -1, 1)
    
def bottomRightCheck(matrix, i, j):
    return Check(matrix, i, j, -1, 1, -1, 1)
    
def bottomLeftCheck(matrix, i, j):
    return Check(matrix, i, j, -1, 1, 0, 2)
    
def fullCheck(matrix, i, j):
    return Check(matrix, i, j, -1, 2, -1, 2)
    
def Check(matrix, i, j, s1, e1, s2, e2):
    value = []
    
    for line in range(s1, e1):
        for row in range(s2, e2):
            value.append(matrix[int(i+line)][int(j+row)])
    
    val = 0
    for i in range(len(value)):
        val += value[i].count("b")
        
    return val
        
main()
