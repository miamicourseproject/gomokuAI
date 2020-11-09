from math import pi
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Board(object):
    def __init__(self, status, value, ROW, COL, aiplayer, pattern_dict):
        self.turnA = True
        self.status = status
        self.value = value
        self.ROW = ROW
        self.COL = COL
        self.aiplayer = aiplayer
        self.pattern_dict = pattern_dict

    def listen(self):  # listen to the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if self.turnA:
                self.aiplayer.miniMax(self.status, self.value, self.aiplayer.depth, -math.inf, math.inf, True)
                ai_next_move_x = self.aiplayer.next_move[0]
                ai_next_move_y = self.aiplayer.next_move[1]
                self.value = self.aiplayer.evaluation(ai_next_move_x,ai_next_move_y,self.value,self.status,1)
                print(self.value)
                self.status[ai_next_move_x][ai_next_move_y] = 1
                for pattern in self.pattern_dict:
                    if ultility.counting(ai_next_move_x, ai_next_move_y, pattern, self.COL, self.ROW, self.status) > 0:
                        print(pattern)
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
                        self.value = self.aiplayer.evaluation(col1,row1,self.value,self.status,-1)
                        print(self.value)
                        self.status[col1][row1] = -1
                        for pattern in self.pattern_dict:
                            if ultility.counting(col1, row1, pattern, self.COL, self.ROW,
                                                 self.status) > 0:
                                print(pattern)
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
    def counting(x_position, y_position, pattern, COL, ROW, status):
        # direction
        dir = [[1, 0], [1, 1], [0, 1], [-1, 1]]
        # (col, row)

        # prepare column, row, length, count
        length = len(pattern)
        count = 0

        # all 4 direction
        for direction in range(4):
            # find starting point
            if dir[direction][0]*dir[direction][1] == 0:
                numberOfGoBack = dir[direction][0] * min(5, x_position) + dir[direction][1] * min(5, y_position)
            else:
                numberOfGoBack = min(5, (x_position * dir[direction][0]) % COL, y_position)
            # very first starting point
            x_starting = x_position - numberOfGoBack * dir[direction][0]
            y_starting = y_position - numberOfGoBack * dir[direction][1]
            # loop through different possible patterns in a row/col/diag
            for i in range(numberOfGoBack+1):
                # get a new starting point
                row1 = y_starting + i*dir[direction][1]
                col1 = x_starting + i*dir[direction][0]
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
    def check_win(value):
        return value % 10 != 0

class AIPlayer(object):
    def __init__(self, depth, COL, ROW, pattern_dict):
        self.depth = depth
        self.ROW = ROW
        self.COL = COL
        self.pattern_dict = pattern_dict
        # self declared
        self.next_move = [-1, -1]
        self.next_value = 0
    def miniMax(self, status, value, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or ultility.check_win(value):
            return value
        if maximizingPlayer:
            maxEval = -math.inf
            childMax = [-1, -1]
            for k in range(self.COL):
                for l in range(self.ROW):
                    if self.validMove(status, k, l):
                        new_val = self.evaluation(k, l, value, status, 1)
                        status[k][l] = 1
                        eval = self.miniMax(status, new_val, depth - 1, alpha, beta, False)
                        if eval > maxEval:
                            maxEval = eval
                            childMax = [k, l]
                            self.next_value = new_val
                        alpha = max(alpha, eval)
                        status[k][l] = 0
                        if beta <= alpha:
                            break
            self.next_move = childMax
            return maxEval
        else:
            minEval = math.inf
            childMin = [-1, -1]
            for k in range(self.COL):
                for l in range(self.ROW):
                    if self.validMove(status, k, l):
                        new_val = self.evaluation(k, l, value, status, -1)
                        status[k][l] = -1
                        eval = self.miniMax(status, new_val, depth - 1, alpha, beta, True)
                        if eval < minEval:
                            minEval = eval
                            childMin = [k, l]
                            self.next_value = new_val
                        beta = min(beta, eval)
                        status[k][l] = 0
                        if beta <= alpha:
                            break
            self.next_move = childMin
            return minEval

    def evaluation(self, new_x, new_y, currentBoardEval, status, turn):
        value_before = 0
        value_after = 0
        for pattern in self.pattern_dict:
            value_before += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status) * self.pattern_dict[pattern]
            status[new_x][new_y] = turn
            value_after += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status) * self.pattern_dict[
                pattern]
            status[new_x][new_y] = 0
        return currentBoardEval + value_after - value_before


    def validMove(self, status, k, l):
        return status[k][l] == 0

def startBoard():
    ai = AIPlayer(2, COL, ROW, create_pattern_dict())
    global iniStatus, key
    iniStatus = [[0 for x in range(COL)] for y in range(ROW)]
    key = Board(iniStatus, 0, COL, ROW, ai, create_pattern_dict())


def redraw(surface):
    surface.fill((0, 0, 0))
    key.draw(surface)
    pygame.display.update()


def start_game():
    startBoard()

def create_pattern_dict():
    x = -1
    pattern_dict = {}
    while (x < 2):
        y = -x
        # open3
        pattern_dict[(0, x, x, x, 0)] = 1100 * x
        # capped3_left
        pattern_dict[(0, x, x, x, y)] = 1010 * x
        # capped3_right
        pattern_dict[(y, x, x, x, 0)] = 1010 * x
        # consecutive5
        pattern_dict[(x, x, x, x, x)] = 100000000000 * x + 1
        # gapped4_right
        pattern_dict[(x, x, x, 0, x)] = 100000 * x
        # gapped4_left
        pattern_dict[(x, 0, x, x, x)] = 100000 * x
        # gapped4_mid
        pattern_dict[(x, x, 0, x, x)] = 1000000 * x
        # open4
        pattern_dict[(0, x, x, x, x, 0)] = 100000000 * x
        # capped4_left
        pattern_dict[(0, x, x, x, x, y)] = 10000000 * x
        # capped4_right
        pattern_dict[(y, x, x, x, x, 0)] = 10000000 * x

        x += 2
    return pattern_dict

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
        if ultility.check_win(key.value):
            pygame.time.delay(50)
            start_game()



main()
# 0
# 0
# 0
# 0
# 0
# -1010
# (1, -1, -1, -1, 0)
# 0
# 0
# 0
# -1100
# (0, -1, -1, -1, 0)
# -1100
# -10000090
# (1, -1, -1, -1, -1, 0)
# -90