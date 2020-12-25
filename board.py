import pygame
import math
from ultility import ultility
import ctypes

xMargin = None
yMargin = None
size = None

class Board(object):
    def __init__(self, turnA, status, value, ROW, COL, aiplayer, patternDict):
        # turnA means AI's turn while !turnA is human's turn
        self.turnA = turnA
        self.initTurn = turnA
        self.status = status
        # initialize the boundary cases
        self.bound = {ultility.getNumber(COL//2, ROW//2, COL): 1}
        self.value = value
        self.ROW = ROW
        self.COL = COL
        self.aiplayer = aiplayer
        self.patternDict = patternDict
        self.empty_cell = ROW * COL

    def listen(self, pos):  # listen to the user
        if self.turnA:
            # call miniMax function so that AI can make its next move
            self.aiplayer.miniMax(self.status, self.bound, self.value, self.aiplayer.depth, -math.inf, math.inf, self.initTurn)
            ai_nextMove_x = self.aiplayer.nextMove[0]
            ai_nextMove_y = self.aiplayer.nextMove[1]
            # update board's total value
            self.value = self.aiplayer.next_value
            # make AI's decided next move and change turnA to False
            self.status[ai_nextMove_x][ai_nextMove_y] = 1 if self.initTurn else -1
            # update the new boundary for possible moves in the current status
            self.bound = self.aiplayer.next_bound
            # update empty cell
            self.empty_cell = self.empty_cell - 1
            self.turnA = not self.turnA

        # human's turn
        else:
            # get position of clicked mouse and convert it to according row and column
            col1 = (pos[0] - xMargin) // size
            row1 = (pos[1] - yMargin) // size
            if ultility.checkInBound(col1, row1, self.COL, self.ROW):
                # check if that position is already marked
                if self.status[col1][row1] == 1 or self.status[col1][row1] == -1:
                    ultility.Mbox('Error', "Invalid Move", 1)
                else:
                    # update board's value, make the move and change turnA to True
                    initTurnVal = -1 if self.initTurn else 1
                    self.value = self.aiplayer.evaluation(col1, row1, self.value, self.status, initTurnVal, self.bound)
                    self.status[col1][row1] = initTurnVal
                    # update the new boundary for possible moves in the current status
                    self.aiplayer.updateBound(self.bound, self.status, col1, row1)
                    # empty cell update
                    self.empty_cell = self.empty_cell - 1
                    self.turnA = not self.turnA

    def draw(self, surface):
        global size, xMargin, yMargin
        # set size of each square and board's margin
        size = 40
        xMargin = (800 - size*self.ROW)//2
        yMargin = (700 - size*self.ROW)//2
        # draw the board
        y = yMargin
        for i in range(self.ROW + 1):
            pygame.draw.line(surface, (255, 255, 255), (xMargin, y), (xMargin + self.ROW * size, y))
            y = y + size
        x = xMargin
        for j in range(self.COL + 1):
            pygame.draw.line(surface, (255, 255, 255), (x, yMargin), (x, yMargin + self.COL * size))
            x = x + size
        #  draw characters in the square
        font = pygame.font.SysFont('arial', 40)
        for k in range(self.ROW):
            for l in range(self.COL):
                if self.status[k][l] == 1:
                    text = font.render('x', True, (255, 255, 255))
                elif self.status[k][l] == -1:
                    text = font.render('o', True, (255, 255, 255))
                # draw nothing if square is empty
                else:
                    text = font.render('', True, (0, 0, 0))
                surface.blit(text, (k * size + xMargin + 10, l * size + yMargin - 10))
