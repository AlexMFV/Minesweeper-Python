from random import *
from graphics import *
import time
import pygame as game
import sys

def main():
    sys.setrecursionlimit(2000) #Default 1000 (Stack overflow sometimes when board is at maximum size possible)
    game.init()

    #Variables
    matrix = []
    h = 24 #max: 24
    w = 30 #max: 30
    bombs = 10 #min 10
    plates = [] # Buttons on top of the numbers
    isPlaying = True
    hasStarted = True
    click = 0
    clickPos = [0, 0]
    clickState = None

    if h > 24:
        h = 24

    if w > 30:
        w = 30

    win = drawWindow(w, h)
    game.display.update()

    #Start loading time...
    time_start = time.perf_counter()

    #Methods
    initBoard(matrix, w, h)
    addBombs(matrix, bombs, w, h)

    #End loading time
    time_end = time.perf_counter() - time_start
    print("Time to load:",time_end)

    #Main Game
    #while hasStarted:
    while isPlaying:
        clearScreen(win)

        '''Gets the current state of the mouse presses'''
        clickState = game.mouse.get_pressed()

        #Main of all the events like button presses and mouse
        for event in game.event.get():
            if event.type == game.QUIT:
                exit()
            if event.type == game.MOUSEBUTTONDOWN:
                click = event.button #1 = Left, 2 = Middle, 3 = Right, 4 = Scroll Up, 5 = Scroll Down
                clickPos = game.mouse.get_pos()

        #Draws the emoji face when clicked
        if clickState[0] == 1:
            pass

        if clickPos[0] >= 12 and clickPos[1] >= 55 and clickPos[0] < w*16+12 and clickPos[1] < h*16+55:
            print(clickPos)
            clickPos = processClick(clickPos)
            if click == 1:
                isPlaying = checkNumber(win, matrix, int(clickPos.getX()), int(clickPos.getY()), w, h, plates)
                #checkWin()
            elif click == 3:
                changeFlag(win, matrix, int(clickPos.getX()), int(clickPos.getY()))

        drawFullCover(win, w, h)
        drawCoverPlates(win, matrix, w, h, plates)
        drawNumber(win, matrix)
        drawGameBorders(win, w, h)

        click = 0
        clickPos = [0, 0]
        game.display.update()

    showAllBombs(win, matrix, plates, w)
    game.display.update()
    #game.display.quit()

##  All methods below this  ##

def clearScreen(win):
    win.fill(game.Color("black"))

def changeFlag(win, matrix, x, y):
    if matrix[y][x] == "f":
        matrix[y][x] = " "
    elif matrix[y][x] == " ":
        matrix[y][x] = "f"
    elif matrix[y][x] == "b":
        matrix[y][x] = "fb"
    elif matrix[y][x] == "fb":
        matrix[y][x] = "b"

'''(Recursive Funtion)'''
def revealAdjacentTiles(win, matrix, i, j, w, h, plates):
    if matrix[i][j] == "0":
        #Checks the position of the clicked button
        if j > 0 and j < w-1:
            if i == 0:
                topCheck(win, matrix, j, i, plates, w, h) #Top check
            elif i == h-1:
                bottomCheck(win, matrix, j, i, plates, w, h)
            else:
                fullCheck(win, matrix, j, i, plates, w, h) #Full Check
        else:
            if i == 0:
                if j == 0:
                    topLeftCheck(win, matrix, j, i, plates, w, h) #Top Left Check
                else:
                    topRightCheck(win, matrix, j, i, plates, w, h) #Top Right Check
            elif i == h-1:
                if j == 0:
                    bottomLeftCheck(win, matrix, j, i, plates, w, h) #Bottom Left Check
                else:
                    bottomRightCheck(win, matrix, j, i, plates, w, h) #Bottom Right Check
            else:
                if j == 0:
                    leftCheck(win, matrix, j, i, plates, w, h) #Left Check
                else:
                    rightCheck(win, matrix, j, i, plates, w, h) #Right Check\
    else:
        undrawCover(Point(j, i), plates, w)

'''When the player loses the game all the bombs are revealed'''
def showAllBombs(win, matrix, plates, w):
    for a in range(len(matrix)):
        for b in range(len(matrix[a])):
            if matrix[a][b] == "f":
                matrix[a][b] = "wbf"

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "b":
                drawBomb(win, i, j)
            elif matrix[i][j] == "wbf":
                drawWrongFlag(win, i, j)

'''Transforms the clicked position to a grid position'''
def processClick(click):
    if click != None:
        x = click[0]-12
        y = click[1]-55
        x = int(x / 16)
        y = int(y / 16)
        return Point(x, y)
    return None

'''Draws the window, dynamic to the number of squares'''
def drawWindow(w, h):
    game.display.set_caption('Minesweeper')
    win = game.display.set_mode((20+w*16, 64+h*16))
    return win

'''Draws all the cover buttons of the grid'''
def drawCoverPlates(win, matrix, w, h, plates):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            drawPlate(win, matrix, i, j)

def drawFullCover(win, w, h):
    ##Full Background Shade
    full = game.draw.rect(win, (192, 192, 192), (0, 0, 20+w*16, 64+h*16), 0)

def drawGameBorders(win, w, h):

    #Grey Shades
    grey1 = game.draw.rect(win, (192, 192, 192), (3, 3, 17+w*16, 6), 0)
    grey2 = game.draw.rect(win, (192, 192, 192), (3, 3, 6, 61+h*16), 0)
    grey3 = game.draw.rect(win, (192, 192, 192), (3, 3, w*16, -6), 0)
    grey4 = game.draw.rect(win, (192, 192, 192), (3, 3, 6, 61+h*16), 0)

    #White Shades
    white1 = game.draw.rect(win, (255, 255, 255), (0, 0, 20+w*16, 3), 0)
    white2 = game.draw.rect(win, (255, 255, 255), (0, 0, 3, 64+h*16), 0)

    ##Inner Shades
    white3 = game.draw.rect(win, (255, 255, 255), (10, 57+h*16, 1+w*16, 57+h*16), 0)
    white4 = game.draw.rect(win, (255, 255, 255), (11, 56+h*16, 1+w*16, 57+h*16), 0)
    white5 = game.draw.rect(win, (255, 255, 255), (12, 55+h*16, 1+w*16, 57+h*16), 0)

    white6 = game.draw.rect(win, (255, 255, 255), (12+w*16, 55, 1, 54+h*16), 0)
    white7 = game.draw.rect(win, (255, 255, 255), (13+w*16, 54, 1, 54+h*16), 0)
    white8 = game.draw.rect(win, (255, 255, 255), (14+w*16, 53, 1, 54+h*16), 0)

    ##Inner Grey Shades
    grey5 = game.draw.rect(win, (128, 128, 128), (9, 52, 5+w*16, 1), 0)
    grey6 = game.draw.rect(win, (128, 128, 128), (9, 53, 4+w*16, 1), 0)
    grey7 = game.draw.rect(win, (128, 128, 128), (9, 54, 3+w*16, 1), 0)

    grey8 = game.draw.rect(win, (128, 128, 128), (9, 55, 1, 2+h*16), 0)
    grey9 = game.draw.rect(win, (128, 128, 128), (10, 55, 1, 1+h*16), 0)
    grey10 = game.draw.rect(win, (128, 128, 128), (11, 55, 1, h*16), 0)

    #Left Grey Shades
    grey11 = game.draw.rect(win, (192, 192, 192), (16+w*16, 3, 18+w*16, 64+h*16), 0)

    #Bottom Grey Shades
    grey12 = game.draw.rect(win, (192, 192, 192), (2, 58+h*16, 18+w*16, 64+h*16), 0)
    #white4 = game.draw.rect(win, (255, 255, 255), (), 0)

'''Draws the cover button in the position retrieved'''
def drawPlate(win, matrix, i, j):
    list = []
    #Shades serve as a 3D effect
    #Main Cover
    cover = game.draw.rect(win, (192, 192, 192), (j*16+12, i*16+55, 16, 16), 0)

    #White Shades
    white1 = game.draw.rect(win, (255, 255, 255), (j*16+12, i*16+55, 16-1, 1), 0)
    white2 = game.draw.rect(win, (255, 255, 255), (j*16+12, i*16+56, 16-2, 1), 0)
    white3 = game.draw.rect(win, (255, 255, 255), (j*16+12,i*16+55, 1, 16-1), 0)
    white4 = game.draw.rect(win, (255, 255, 255), (j*16+13, i*16+55, 1, 16-2), 0)

    #Grey Shades #...This is so confusing...
    grey1 = game.draw.rect(win, (128, 128, 128), ((j+1)*16+12, (i+1)*16+54, -16+3, 0), 0)
    grey2 = game.draw.rect(win, (128, 128, 128), ((j+1)*16+12, (i+1)*16+55, -16+2, 0), 0)
    grey3 = game.draw.rect(win, (128, 128, 128), ((j+1)*16+12, (i+1)*16+55, 0, -16+2), 0)
    grey4 = game.draw.rect(win, (128, 128, 128), ((j+1)*16+11, (i+1)*16+55, 0, -16+3), 0)

    list.append(white1)
    list.append(white2)
    list.append(white3)
    list.append(white4)
    list.append(grey1)
    list.append(grey2)
    list.append(grey3)
    list.append(grey4)
    list.append(cover)

    return list

'''Draws the flags that are placed wrongly'''
def drawWrongFlag(win, i, j):
    pic = "../Resources/wbf.gif"
    img = game.image.load(pic)
    win.blit(img, (j*16+12, i*16+55))

'''Draws the remaining bombs after the player lost the game'''
def drawBomb(win, i, j):
    pic = "../Resources/b.gif"
    img = game.image.load(pic)
    win.blit(img, (j*16+12, i*16+55))

'''Draws the number on the screen (also applies for bombs)'''
def drawNumber(win, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            num = matrix[i][j]
            if num != "b" and num != " " and num != "f" and num != "fb" and num != "0":
                pic = "../Resources/" + num + ".gif"
                img = game.image.load(pic)
                win.blit(img, (j*16+12, i*16+55))
            if num == "f" or num == "fb":
                pic = "../Resources/flag.gif"
                img = game.image.load(pic)
                win.blit(img, (j*16+12, i*16+55))
            if num == "0":
                drawBlackSpace(win, i, j)

def drawBlackSpace(win, y, x):
    grey = game.draw.rect(win, (128, 128, 128), (x*16+12, y*16+55, 16, 16), 2)
    lightGrey = game.draw.rect(win, (192, 192, 192), (x*16+13, y*16+56, 14, 14), 0)

'''Initializes the board array with empty values'''
def initBoard(matrix, w, h):
    for i in range(h):
        matrix.append([" "] * w)

'''Adds the bombs to random place in the board array'''
def addBombs(matrix, bombs, w, h):
    for i in range(bombs):
        y = randint(0, h)-1
        x = randint(0, w)-1
        while matrix[y][x] == "b":
            y = randint(0, h)-1
            x = randint(0, w)-1
        matrix[y][x] = "b"

'''Gets and draws the number in the position of the click'''
def checkNumber(win, matrix, x, y, w, h, plates):
    if matrix[y][x] == " " or matrix[y][x] == "b" or matrix[y][x] == "0" and matrix[x][y] != "f":
        matrix[y][x] = checkAround(matrix, y, x, w, h)

        if matrix[y][x] == "0":
            revealAdjacentTiles(win, matrix, y, x, w, h, plates)

        if matrix[y][x] == "exp":
            return False
        else:
            return True

    return True

'''Below this line it is very non optimized and bad written code'''

'''Checks if the button is on top of screen'''
def topCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j-1] == " ":
        checkNumber(win, matrix, j-1, i, w, h, plates)

    if matrix[i][j+1] == " ":
        checkNumber(win, matrix, j+1, i, w, h, plates)

    if matrix[i+1][j] == " ":
        checkNumber(win, matrix, j, i+1, w, h, plates)

'''Checks if button is on bottom of the screen'''
def bottomCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j-1] == " ":
        checkNumber(win, matrix, j-1, i, w, h, plates)

    if matrix[i][j+1] == " ":
        checkNumber(win, matrix, j+1, i, w, h, plates)

    if matrix[i-1][j] == " ":
        checkNumber(win, matrix, j, i-1, w, h, plates)

'''Checks all around the button'''
def fullCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j-1] == " ":
        checkNumber(win, matrix, j-1, i, w, h, plates)

    if matrix[i][j+1] == " ":
        checkNumber(win, matrix, j+1, i, w, h, plates)

    if matrix[i+1][j] == " ":
        checkNumber(win, matrix, j, i+1, w, h, plates)

    if matrix[i-1][j] == " ":
        checkNumber(win, matrix, j, i-1, w, h, plates)

'''Checks if the button is on the top left corner'''
def topLeftCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j+1] == " ":
        checkNumber(win, matrix, j+1, i, w, h, plates)

    if matrix[i+1][j] == " ":
        checkNumber(win, matrix, j, i+1, w, h, plates)

'''Checks if the button is on the top right corner'''
def topRightCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j-1] == " ":
        checkNumber(win, matrix, j-1, i, w, h, plates)

    if matrix[i+1][j] == " ":
        checkNumber(win, matrix, j, i+1, w, h, plates)

'''Checks if the button is on the bottom left corner'''
def bottomLeftCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j+1] == " ":
        checkNumber(win, matrix, j+1, i, w, h, plates)

    if matrix[i-1][j] == " ":
        checkNumber(win, matrix, j, i-1, w, h, plates)

'''Checks if the button is on the bottom right corner'''
def bottomRightCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j-1] == " ":
        checkNumber(win, matrix, j-1, i, w, h, plates)

    if matrix[i-1][j] == " ":
        checkNumber(win, matrix, j, i-1, w, h, plates)

'''Checks if the button is on the left'''
def leftCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j+1] == " ":
        checkNumber(win, matrix, j+1, i, w, h, plates)

    if matrix[i+1][j] == " ":
        checkNumber(win, matrix, j, i+1, w, h, plates)

    if matrix[i-1][j] == " ":
        checkNumber(win, matrix, j, i-1, w, h, plates)

'''Checks if the button is on the right'''
def rightCheck(win, matrix, j, i, plates, w, h):
    if matrix[i][j-1] == " ":
        checkNumber(win, matrix, j-1, i, w, h, plates)

    if matrix[i+1][j] == " ":
        checkNumber(win, matrix, j, i+1, w, h, plates)

    if matrix[i-1][j] == " ":
        checkNumber(win, matrix, j, i-1, w, h, plates)

'''Before this line it is very non-optimized and bad written code'''

'''Checks around the clicked position for bombs (Gets values for Check())'''
def checkAround(matrix, i, j, w, h):
    bombsFound = 0
    w = w-1
    h = h-1

    #If its a bomb, explode
    if matrix[i][j] == "b":
        return "exp"

    #Checks the position of the clicked button
    if j > 0 and j < w:
        if i == 0:
            bombsFound += Check(matrix, i, j, 0, 2, -1, 2) #Top check
        elif i == h:
            bombsFound += Check(matrix, i, j, -1, 1, -1, 2) #Bottom Check
        else:
            bombsFound += Check(matrix, i, j, -1, 2, -1, 2) #Full Check
    else:
        if i == 0:
            if j == 0:
                bombsFound += Check(matrix, i, j, 0, 2, 0, 2) #Top Left Check
            else:
                bombsFound += Check(matrix, i, j, 0, 2, -1, 1) #Top Right Check
        elif i == h:
            if j == 0:
                bombsFound += Check(matrix, i, j, -1, 1, 0, 2) #Bottom Left Check
            else:
                bombsFound += Check(matrix, i, j, -1, 1, -1, 1) #Bottom Right Check
        else:
            if j == 0:
                bombsFound += Check(matrix, i, j, -1, 2, 0, 2) #Left Check
            else:
                bombsFound += Check(matrix, i, j, -1, 2, -1, 1) #Right Check

    return str(bombsFound)

'''Complement of checkAround (Actually checks around)'''
def Check(matrix, i, j, s1, e1, s2, e2):
    val = 0
    for line in range(s1, e1):
        for row in range(s2, e2):
            if matrix[int(i+line)][int(j+row)] == "b" or matrix[int(i+line)][int(j+row)] == "fb":
                val += 1
    return val

main()
