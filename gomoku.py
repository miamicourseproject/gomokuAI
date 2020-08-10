from math import pi
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Board(object):
    def __init__(self, status, ROW, COL, aiplayer):
        self.turnA = True
        self.status = status
        self.ROW = ROW
        self.COL = COL
        self.aiplayer = aiplayer

    def listen(self):  # listen to the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if self.turnA:
                self.status = self.aiplayer.miniMax(self.status)
                self.turnA = not self.turnA
            else:
                if pygame.mouse.get_pressed()[0]:
                    col1 = (pygame.mouse.get_pos()[0] - x_margin) // size
                    row1 = (pygame.mouse.get_pos()[1] - y_margin) // size
                    # check and update the status
                    if self.status[col1][row1] == 1 or self.status[col1][row1] == -1:
                        # notice that this character is chosen
                        print("dont choose again!")
                        break
                    else:
                        self.status[col1][row1] = -1
                        self.turnA = not self.turnA

    def draw(self, surface):
        global size, x_margin, y_margin
        # tim cach sua lai cai nay
        size = 40
        x_margin = 10
        y_margin = 10
        y = y_margin
        for i in range(self.ROW + 1):
            pygame.draw.line(surface, (255, 255, 255), (x_margin, y), (x_margin + self.ROW * size, y))
            y = y + size
        x = x_margin
        for j in range(self.COL + 1):
            pygame.draw.line(surface, (255, 255, 255), (x, y_margin), (x, y_margin + self.COL * size))
            x = x + size
        #  draw characters in the square
        font = pygame.font.SysFont('arial', 40)
        for k in range(self.ROW):
            for l in range(self.COL):
                if self.status[k][l] == 1:
                    text = font.render('x', True, (255, 0, 0))
                elif self.status[k][l] == -1:
                    text = font.render('o', True, (255, 0, 0))
                else:
                    text = font.render('o', True, (0, 0, 0))
                surface.blit(text, (k * 40 + 20, l * 40))

    def check_in_bound(self, x, y):
        return 0 <= x < self.COL and 0 <= y < self.ROW

    def check_win(self):
        # direction
        dir = [[1, 0], [1, 1], [0, 1], [-1, 1]]
        # (col, row)

        for row in range(self.ROW):
            for col in range(self.COL):
                if self.status[col][row] != 0:
                    # all direction
                    for direction in range(4):
                        # begin
                        row1 = row + dir[direction][1]
                        col1 = col + dir[direction][0]
                        times = 1

                        # count number of consecutive x/o
                        while self.check_in_bound(col1, row1) and self.status[col1][row1] == self.status[col][row]:
                            times += 1
                            row1 = row1 + dir[direction][1]
                            col1 = col1 + dir[direction][0]

                        # check win
                        if times == 5:
                            if self.status[col][row] == 1:
                                print("A wins")
                            else:
                                print("B wins")
                            return True
        return False


class AIPlayer(object):
    def __init__(self, depth):
        self.depth = depth
    def miniMax(self, status, alpha, beta, maximizingPlayer):
        if self.depth == 0:
            return self.evaluation()
        if maximizingPlayer:
            maxEval = -math.inf
            childMax = None
            #save child in a instance variable or..
            for child in self.childSet(self.status, True):
                eval = self.miniMax(child, self.depth-1, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    childMax = child
                alpha = max(alpha,eval)
                if beta <= alpha:
                    break
            return childMax
        else:
            minEval = math.inf
            for child in self.childSet(self.status, False):
                eval = self.miniMax(child, self.depth-1, alpha, beta, True)
                minEval = min(minEval,eval)
                beta = min(beta,eval)
                if beta <= alpha:
                    break
            return minEval

        return status

    def evaluation(self):
        pass

    def childSet(self, status, turn):
        listChild = []
        for k in range(15):
            for l in range (15):
                if status[k][l] != 0:
                    break
                else:
                    if turn:
                        status[k][l] = -1
                    else:
                        status[k][l] = 1
                    listChild.append(status)
                status[k][l] = 0

        return listChild


def startBoard():
    ai = AIPlayer(2)
    global iniStatus, key
    iniStatus = [[0 for x in range(COL)] for y in range(ROW)]
    key = Board(iniStatus, ROW, COL, ai)


def redraw(surface):
    surface.fill((0, 0, 0))
    key.draw(surface)
    pygame.display.update()


def start_game():
    startBoard()


def main():
    # prepare
    global width, height, score, ROW, COL
    ROW = 15
    COL = 15
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

    while flag:
        key.listen()
        redraw(frame)
        if key.check_win():
            pygame.time.delay(500)
            start_game()


main()
