from math import pi
import math
import random
import pygame
import sys
from pygame.locals import *
from button import button
from board import Board
from ultility import ultility
from AIPlayer import AIPlayer

# Define variables at global scope first before using them
x_margin = None
y_margin = None
size = None
iniStatus = None
key = None
width = None 
height = None
score = None
ROW = None
COL = None

# Color code
white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)
lessGray = (192,192,192)

# initialize board
def startBoard():
    ai = AIPlayer(2, COL, ROW, createPatternDict())
    global iniStatus, key
    iniStatus = [[0 for x in range(COL)] for y in range(ROW)]
    key = Board(iniStatus, 0, COL, ROW, ai, createPatternDict())

def reDraw(surface):
    surface.fill((0, 0, 0))
    key.draw(surface)
    pygame.display.update()

# this method contains different patterns with their values
# These adapt from https://linyanghe.github.io/projects/resources/Gomuku.pdf
def createPatternDict():
    x = -1
    patternDict = {}
    while (x < 2):
        y = -x
        # long_5
        patternDict[(x, x, x, x, x)] = 1000000 * x
        # live_4
        patternDict[(0, x, x, x, x, 0)] = 1000 * x
        # go_4
        patternDict[(0, x, x, x, x, y)] = 500 * x
        patternDict[(y, x, x, x, x, 0)] = 500 * x
        patternDict[(0, x, x, x, 0, x, 0)] = 500 * x
        patternDict[(0, x, 0, x, x, x, 0)] = 500 * x
        patternDict[(0, x, x, 0, x, x, 0)] = 500 * x
        # dead_4
        patternDict[(y, x, x, x, x, y)] = -5 * x
        # live_3
        patternDict[(0, x, x, x, 0)] = 200 * x
        patternDict[(0, x, 0, x, x, 0)] = 200 * x
        patternDict[(0, x, x, 0, x, 0)] = 200 * x
        # sleep_3
        patternDict[(0, 0, x, x, x, y)] = 50 * x
        patternDict[(y, x, x, x, 0, 0)] = 50 * x
        patternDict[(0, x, 0, x, x, y)] = 50 * x
        patternDict[(y, x, x, 0, x, 0)] = 50 * x
        patternDict[(0, x, x, 0, x, y)] = 50 * x
        patternDict[(y, x, 0, x, x, 0)] = 50 * x
        patternDict[(x, 0, 0, x, x)] = 50 * x
        patternDict[(x, x, 0, 0, x)] = 50 * x
        patternDict[(x, 0, x, 0, x)] = 50 * x
        patternDict[(y, 0, x, x, x, 0, y)] = 50 * x
        # dead_3
        patternDict[(y, x, x, x, y)] = -5 * x
        # live_2
        patternDict[(0, 0, x, x, 0)] = 5 * x
        patternDict[(0, x, x, 0, 0)] = 5 * x
        patternDict[(0, x, 0, x, 0)] = 5 * x
        patternDict[(0, x, 0, 0, x, 0)] = 5 * x
        # sleep_2
        patternDict[(0, 0, 0, x, x, y)] = 3 * x
        patternDict[(y, x, x, 0, 0, 0)] = 3 * x
        patternDict[(0, 0, x, 0, x, y)] = 3 * x
        patternDict[(y, x, 0, x, 0, 0)] = 3 * x
        patternDict[(0, x, 0, 0, x, y)] = 3 * x
        patternDict[(y, x, 0, 0, x, 0)] = 3 * x
        patternDict[(x, 0, 0, 0, x)] = 3 * x
        patternDict[(y, 0, x, 0, x, 0, y)] = 3 * x
        patternDict[(y, 0, x, x, 0, 0, y)] = 3 * x
        patternDict[(y, 0, 0, x, x, 0, y)] = 3 * x
        # dead_2
        patternDict[(y, x, x, y)] = -5 * x
        x += 2
    return patternDict

#Main Screen
def main():
    # prepare
    global width, height, score, ROW, COL
    ROW = 8
    COL = 8
    score = 0
    pygame.init()
    height, width = 650, 650
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Game')
    screen.fill((0, 0, 0))
    # instantiate the game
    startBoard()
    # main loop
    flag = True
    while flag:
        button = pygame.Rect(50, 100, 100, 50)
        pygame.draw.rect(screen, (255, 0, 0), button)
        key.listen()
        reDraw(screen)
        if ultility.checkWin(key.value):
            pygame.time.delay(50)
            startBoard()
 
#Credits Screen
def credit():
    pygame.init()
    pygame.display.set_caption('credit')
    screen = pygame.display.set_mode((700, 700),0,32)
    screen.fill(black)
    cre = "This is the project of Thomas"
    while True:
        pygame.display.update()
        font = pygame.font.SysFont('comicsans', 20)
        text = font.render(cre, 1, (255,255,255))
        screen.blit(text, (20, 20))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

# Main Menu
def main_menu():
    pygame.init()
    pygame.display.set_caption('Start')
    screen = pygame.display.set_mode((700, 700),0,32)
    screen.fill(black)
    wide, high= pygame.display.get_surface().get_size()
    # Initate Buttons
    startButton = button(gray, wide / 4 , high / 4, wide / 2, high / 8, "Start")
    startButton.draw(screen, white)
    creditButton = button(gray, wide / 4 , high / 2.5, wide / 2, high / 8, "Credit")
    creditButton.draw(screen, white)
    while True:
        # Get position of the mouse
        pos = pygame.mouse.get_pos()
        # Update the screen
        pygame.display.update()
        # Draw Buttons
        startButton.draw(screen)
        creditButton.draw(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (startButton.isOver(pos)):
                    main()
                    
                if (creditButton.isOver(pos)):
                    credit()
                    
            if event.type == pygame.MOUSEMOTION:
                if (startButton.isOver(pos)):
                    startButton.color = lessGray
                else:
                    startButton.color = gray

                if (creditButton.isOver(pos)):
                    creditButton.color = lessGray
                else:
                    creditButton.color = gray
    


credit()