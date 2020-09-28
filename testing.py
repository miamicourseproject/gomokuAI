from math import pi
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#hello world
#namhoanghieuphan
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
                self.aiplayer.miniMax(self.status, self.aiplayer.depth, -math.inf, math.inf, True)
                self.status[self.aiplayer.next_move[0]][self.aiplayer.next_move[1]] = 1
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


class ultility:
    @staticmethod
    def check_in_bound(col1, row1, COL, ROW):
        return 0 <= col1 < COL and 0 <= row1 < ROW

    @staticmethod
    def counting(status, pattern):
        # direction
        dir = [[1, 0], [1, 1], [0, 1], [-1, 1]]
        # (col, row)

        # prepare column, row, length, count
        COL = 3
        ROW = 3
        length = len(pattern)
        count = 0

        for row in range(ROW):
            for col in range(COL):
                # all 4 direction
                for direction in range(4):
                    # begin
                    row1 = row
                    col1 = col
                    # check if fit the pattern
                    index = 0
                    while index < length and ultility.check_in_bound(col1, row1, COL, ROW) \
                            and status[col1][row1] == pattern[index]:
                        row1 = row1 + dir[direction][1]
                        col1 = col1 + dir[direction][0]
                        index += 1
                    if index == length:
                        count += 1

        return count

    @staticmethod
    def check_win(status):
        pattern1 = (1, 1, 1, 1, 1)
        pattern2 = (-1, -1, -1, -1, -1)
        return ultility.counting(status, pattern1) > 0 or ultility.counting(status, pattern2) > 0


class AIPlayer(object):
    def __init__(self, depth):
        self.depth = depth
        self.next_move = [-1, -1]

    def miniMax(self, status, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or ultility.check_win(status):
            return self.evaluation(status)
        if maximizingPlayer:
            maxEval = -math.inf
            childMax = [-1, -1]
            for k in range(3):
                for l in range(3):
                    if self.validMove(status, k, l):
                        status[k][l] = 1
                        eval = self.miniMax(status, depth - 1, alpha, beta, False)
                        if eval > maxEval:
                            maxEval = eval
                            childMax = [k, l]
                        alpha = max(alpha, eval)
                        status[k][l] = 0
                        if beta <= alpha:
                            break
            self.next_move = childMax
            return maxEval
        else:
            minEval = math.inf
            childMin = [-1, -1]
            for k in range(3):
                for l in range(3):
                    if self.validMove(status, k, l):
                        status[k][l] = -1
                        eval = self.miniMax(status, depth - 1, alpha, beta, True)
                        if eval < minEval:
                            minEval = eval
                            childMin = [k, l]
                        beta = min(alpha, eval)
                        status[k][l] = 0
                        if beta <= alpha:
                            break
            self.next_move = childMin
            return minEval

    def evaluation(self, status):
        x = -1
        y = -x
        pattern_dict = {}
        while (x < 2):
            #open3
            pattern_dict[(0, x, x, x, 0)] = 100000*x
            #capped3
            pattern_dict[(y, x, x, x, y)] = 10000 * x
            #consecutive5
            pattern_dict[(x, x, x, x, x)] = 10000000 * x
            #gapped4_right
            pattern_dict[(x, x, x, 0, x)] = 100050 * x
            # gapped4_left
            pattern_dict[(x, 0, x, x, x)] = 100050 * x
            # gapped2_2
            pattern_dict[(x, x, 0, x, x)] = 100050 * x
            # open4
            pattern_dict[(0, x, x, x, x, 0)] = 1000000 * x
            # capped4
            pattern_dict[(y, x, x, x, x, y)] = 100050 * x

            x += 2
        value = 0
        for pattern in pattern_dict:
            value += ultility.counting(status, pattern) * pattern_dict[pattern]
        return value


    def validMove(self, status, k, l):
        return status[k][l] == 0


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
    ROW = 3
    COL = 3
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
        if ultility.check_win(key.status):
            pygame.time.delay(500)
            start_game()


main()