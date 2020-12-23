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
from Dropdown import DropDown
from pathlib import Path
from InputBox import InputBox

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
black = (30,30,30)
gray = (128,128,128)
lessGray = (192,192,192)
COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

# initialize board
def startBoard():
    ai = AIPlayer(2, COL, ROW, createPatternDict())
    global iniStatus, key
    iniStatus = [[0 for x in range(COL)] for y in range(ROW)]
    key = Board(iniStatus, 0, COL, ROW, ai, createPatternDict())

def reDraw(surface):
    surface.fill(black)
    key.draw(surface)
    pygame.display.update()

# this method contains different patterns with their values
# These adapt from this report. Link: https://linyanghe.github.io/projects/resources/Gomuku.pdf
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
def main(size = 5):
    # prepare
    global width, height, score, ROW, COL
    ROW, COL = size, size
    score = 0
    pygame.init()
    screen = pygame.display.set_mode((700, 700),0,32)
    pygame.display.set_caption('Game')
    screen.fill(black)
    wide, high = pygame.display.get_surface().get_size()

    # instantiate the game
    startBoard()
    
    # main loop
    while True:
        pos = pygame.mouse.get_pos()
        button1 = pygame.Rect(50, 100, 100, 50)
        pygame.draw.rect(screen, (255, 0, 0), button1)
        key.listen()
        reDraw(screen)
        if ultility.checkWin(key.value) or ultility.checkTie(key):
            pygame.time.delay(50)
            startBoard()
 
#Credits Screen
def credit():
    pygame.init()
    pygame.display.set_caption('credit')
    screen = pygame.display.set_mode((700, 700),0,32)
    screen.fill(black)
    wide, high = pygame.display.get_surface().get_size()

    creditForTeam = "This Project is made by Duc Nam, Hieu Phan and Thomas Nguyen"
    creditForBackEnd = "Algorithms + Game Logic: Duc Nam and Hieu Phan"
    creditForFrontEnd = "UI/ Design: Thomas Nguyen"

    backButton = button(gray, wide / 4 , 7 * high / 8 - 20, wide / 2, high / 8, "Back to Main Menu")
    backButton.draw(screen, white)
    pygame.display.update()

    font = pygame.font.SysFont('Times New Roman', 20)
    cre1 = font.render(creditForTeam, False, white)
    cre2 = font.render(creditForBackEnd, False, white)
    cre3 = font.render(creditForFrontEnd, False, white)
        
    screen.blit(cre1, (wide / 12, high / 20))
    screen.blit(cre2, (wide / 12, high / 20 + 30))
    screen.blit(cre3, (wide / 12, high / 20 + 60))


    while True:
        pos = pygame.mouse.get_pos()
        backButton.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (backButton.isOver(pos)):
                    mainMenu()
                    
            if event.type == pygame.MOUSEMOTION:
                if (backButton.isOver(pos)):
                    backButton.color = lessGray
                else:
                    backButton.color = gray

# Substart Menu
def subStart():
    pygame.init()
    pygame.display.set_caption('credit')
    screen = pygame.display.set_mode((700, 700),0,32)
    screen.fill(black)
    wide, high = pygame.display.get_surface().get_size()

    # List of size
    sizeList = [5,6,7,8,9,10]
    size = 5 # default value

    # create buttons
    titleText= "Choose the size of your board"
    startButton =  button(gray, wide / 4 , high / 7, wide / 2, high / 8, "Start Game")
    startButton.draw(screen, white)
    backButton = button(gray, wide / 4 , 7 * high / 8 - 20, wide / 2, high / 8, "Back to Main Menu")
    backButton.draw(screen, white)  

    # create title
    font = pygame.font.SysFont('Times New Roman', 40)
    title = font.render(titleText, False, white)
    screen.blit(title, (wide / 6, high / 20))
    
    # create dropdown
    sizeDropDown = DropDown([gray, lessGray], [gray, lessGray], wide / 4 , high / 3 + 20, wide / 2, high / 15, 
    pygame.font.SysFont("Times New Roman", 30), "Select Mode", ["5x5", "6x6", "7x7", "8x8", "9x9", "10x10"])

    # create input field
    nameInput = InputBox(wide / 4, 15 * high / 56 + 20, wide / 2, high / 20, "Fill in your name")

    while True:
        pos = pygame.mouse.get_pos()
        backButton.draw(screen)
        startButton.draw(screen)
        nameInput.draw(screen)
        pygame.display.update()
        event_list = pygame.event.get()

        for event in event_list:
            nameInput.handle_event(event)
            nameInput.update()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (backButton.isOver(pos)):
                    mainMenu()
                if (startButton.isOver(pos)):
                    main(size)

            if event.type == pygame.MOUSEMOTION:
                if (backButton.isOver(pos)):
                    backButton.color = lessGray
                else:
                    backButton.color = gray

                if (startButton.isOver(pos)):
                    startButton.color = lessGray
                else:
                    startButton.color = gray

        selectedOption = sizeDropDown.update(event_list,pos)

        if selectedOption >= 0:
            sizeDropDown.main = sizeDropDown.options[selectedOption]
            size = sizeList[selectedOption]

        screen.fill(black)
        nameInput.draw(screen)
        sizeDropDown.draw(screen)
        screen.blit(title, (wide / 6, high / 20))

    pygame.display.update()

#High Score Menu
def highScore():
    pygame.init()
    pygame.display.set_caption('High Score')
    screen = pygame.display.set_mode((700, 700))
    screen.fill(black)
    wide, high= pygame.display.get_surface().get_size()

    # Write to File
    highScorePathWrite = open('High Scores.txt', "a")
    highScorePathWrite.close()

    # Read File
    highScorePathRead = open('High Scores.txt', 'r')
    lines = highScorePathRead.readlines()
    if (len(lines) == 0):
        lines = ["No Data Yet"]
    index = 0

    #Screen Title
    font = pygame.font.SysFont('Times New Roman', 40)
    playerInfo = font.render("High Score", False, white)
    textWidth, textHeight = font.size("High Score")
    screen.blit(playerInfo, (wide / 2 - textWidth / 2, high / 20 + 20 * 2 * index))

    # Back Button
    backButton = button(gray, wide / 4 ,  7 * high / 8 - 20, wide / 2, high / 8, "Back to Main Menu")
    backButton.draw(screen, white)
    pygame.display.update()

    for line in lines:
        line = line.strip()
        font = pygame.font.SysFont('Times New Roman', 25)
        textWidth, textHeight = font.size("High Score")
        playerInfo = font.render(line, False, white)
        screen.blit(playerInfo, (wide / 2 - textWidth / 2, high / 6 + 20 * 2 * index))
        index = index + 1

    while True:
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        backButton.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (backButton.isOver(pos)):
                    mainMenu()
                    
            if event.type == pygame.MOUSEMOTION:
                if (backButton.isOver(pos)):
                    backButton.color = lessGray
                else:
                    backButton.color = gray

# Main Menu
def mainMenu():
    pygame.init()
    pygame.display.set_caption('Start')
    screen = pygame.display.set_mode((700, 700))
    screen.fill(black)
    wide, high = pygame.display.get_surface().get_size()

    # Draw the title
    title = "TIC-TAC-TOE"
    font = pygame.font.SysFont('Times New Roman', 40)
    gameTitle = font.render(title, False, white)
    screen.blit(gameTitle, (wide / 3, high / 20))

    # Initate Buttons
    startButton = button(gray, wide / 4 , high / 4, wide / 2, high / 8, "Start")
    startButton.draw(screen, white)
    creditButton = button(gray, wide / 4 , 3 * high / 8 + 20, wide / 2, high / 8, "Credit")
    creditButton.draw(screen, white)
    highScoreButton = button(gray, wide / 4 , high / 2 + 40, wide / 2, high / 8, "High Score")
    highScoreButton.draw(screen, white)

    while True:
        event_list = pygame.event.get()
        # Get position of the mouse
        pos = pygame.mouse.get_pos()

        # Draw Buttons
        startButton.draw(screen)
        creditButton.draw(screen)
        highScoreButton.draw(screen)
        
        for event in event_list:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (startButton.isOver(pos)):
                    subStart() 
                if (creditButton.isOver(pos)):
                    credit()
                if (highScoreButton.isOver(pos)):
                    highScore()
                    
            if event.type == pygame.MOUSEMOTION:
                if (startButton.isOver(pos)):
                    startButton.color = lessGray
                else:
                    startButton.color = gray
                if (creditButton.isOver(pos)):
                    creditButton.color = lessGray
                else:
                    creditButton.color = gray
                if (highScoreButton.isOver(pos)):
                    highScoreButton.color = lessGray
                else:
                    highScoreButton.color = gray
        pygame.display.update()

main()
