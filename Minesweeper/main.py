from random import *
from graphics import *

def main():
    win = GraphWin("Minesweeper", 160, 210)
    matrix = [][]
    addBombs(matrix)
    
def addBombs(matrix):
    for i in range(10):
        x = randint(0, 9)-1
        y = randint(0, 9)-1
        matrix[x][y] = "b"
    
main()
    
    