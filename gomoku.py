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
                # check and update the status
                if self.status[col1][row1] == 1 or self.status[col1][row1] == -1:
                    # notice that this character is chosen
                    print("dont choose again!")
                    break
                else:
                    if self.turnA:
                        self.status[col1][row1] = 1
                        self.turnA = False
                        self.turnB = True
                    else:
                        self.status[col1][row1] = -1
                        self.turnA = True
                        self.turnB = False
        return ''

    def draw(self, surface):
        global size, ROW, COL, x_margin, y_margin
        size = 40
        ROW = 15
        COL = 15
        x_margin = 10
        y_margin = 10
        y = y_margin
        for i in range(ROW + 1):
            pygame.draw.line(surface, (255, 255, 255), (x_margin, y), (x_margin + ROW * size, y))
            y = y + size
        x = x_margin
        for j in range(ROW + 1):
            pygame.draw.line(surface, (255, 255, 255), (x, y_margin), (x, y_margin + COL * size))
            x = x + size
        #  draw characters in the square
        font = pygame.font.SysFont('arial', 40)
        for k in range(ROW):
            for l in range(COL):
                if self.status[k][l] == 1:
                    text = font.render('x', True, (255, 0, 0))
                elif self.status[k][l] == -1:
                    text = font.render('o', True, (255, 0, 0))
                else:
                    text = font.render('o', True, (0, 0, 0))
                surface.blit(text, (k * 40 + 20, l * 40))

    def check_in_bound(self, x, y):
        return 0 <= x < COL and 0 <= y < ROW

    def check_win(self):
        # direction
        dir = [[1, 0], [1, 1], [0, 1], [-1, 1]]

        for row in range(ROW):
            for col in range(COL):
                if self.status[col][row] != 0:
                    pass;
                    # horizon (pos 0)

                    # vert (pos 2)

                    # diag + (pos 1)

                    # diag - (pos 3)


def startBoard():
    global iniStatus, key
    # tim cach sua lai cai nay
    w, h = 15, 15;
    iniStatus = [[0 for x in range()] for y in range(h)]
    key = Board(iniStatus)

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
    start_game()
    while flag:
        inp = key.listen()
        redraw(frame)

main()