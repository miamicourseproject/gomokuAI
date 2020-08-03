from math import pi
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Board(object):
    def __init__(self, status):
        self.turnA = True
        self.turnB = False
        self.status = status
    def listen(self):  # listen to the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                col1 = (pygame.mouse.get_pos()[0] - x_margin) // size
                row1 = (pygame.mouse.get_pos()[1] - y_margin) // size
                # get the position of the square in the 3x9 rectangle
                pos = row1 * col + col1
                # check and update the status
                if self.status[pos] == 1 or self.status[pos] == -1:
                    # notice that this character is chosen
                    print("dont choose again")
                    break
                else:
                    if self.turnA:
                        self.status[pos] = 1
                        self.turnA = False
                        self.turnB = True
                    else:
                        self.status[pos] = -1
                        self.turnA = True
                        self.turnB = False
        return ''
    def draw(self, surface):
        global size, row, col, x_margin, y_margin
        size = 40
        row = 15
        col = 15
        x_margin = 10
        y_margin = 10
        y = y_margin
        for i in range(row + 1):
            pygame.draw.line(surface, (255, 255, 255), (x_margin, y), (x_margin + 15 * size, y))
            y = y + size
        x = x_margin
        for j in range(col + 1):
            pygame.draw.line(surface, (255, 255, 255), (x, y_margin), (x, y_margin + 15 * size))
            x = x + size
        #  draw characters in the square
        font = pygame.font.SysFont('arial', 25)
        for k in range(225):
            if self.status[k] == 1:
                text = font.render('x', True, (255, 0, 0))
            elif self.status[k] == -1:
                text = font.render('o', True, (255, 0, 0))
            else:
                text = font.render('o', True, (0, 0, 0))
            rowk = k//15 + 1
            colk = k%15
            surface.blit(text, (colk*40, rowk*40))

def startBoard():
    global key
    key = Board([0] * 225)

def redraw(surface):
    surface.fill((0, 0, 0))
    key.draw(surface)
    pygame.display.update()

def start_game():
    startBoard()

def main():
    # prepare
    global width, height,score
    score = 0
    pygame.init()
    width = 650
    height = width
    frame = pygame.display.set_mode((width, height))
    frame.fill((0, 0, 0))
    # instantiate the game
    start_game()
    # main loop
    flag = True
    flag = False
    flag = True
    while flag:
        start_game()
        inp = key.listen()
        redraw(frame)

main()