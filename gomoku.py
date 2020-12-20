from math import pi
import math
import random
import pygame
import sys
from pygame.locals import *
from button import button

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

class Board(object):
    def __init__(self, status, value, ROW, COL, aiplayer, pattern_dict):
        # turnA means AI's turn while !turnA is human's turn
        self.turnA = True # always let AI go first
        self.status = status
        self.value = value
        self.ROW = ROW
        self.COL = COL
        self.aiplayer = aiplayer
        self.pattern_dict = pattern_dict
        self.empty_cell = ROW * COL

    def listen(self):  # listen to the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # AI's turn
            if self.turnA:
                # call miniMax function so that AI can make its next move
                self.aiplayer.miniMax(self.status, self.value, self.aiplayer.depth, -math.inf, math.inf, True)
                ai_next_move_x = self.aiplayer.next_move[0]
                ai_next_move_y = self.aiplayer.next_move[1]
                # update board's total value
                self.value = self.aiplayer.next_value
                # make AI's decided next move and change turnA to False
                self.status[ai_next_move_x][ai_next_move_y] = 1
                self.turnA = not self.turnA
                self.empty_cell = self.empty_cell - 1

            # human's turn
            else:
                if pygame.mouse.get_pressed()[0]:
                    # get position of clicked mouse and convert it to according row and column
                    col1 = (pygame.mouse.get_pos()[0] - x_margin) // size
                    row1 = (pygame.mouse.get_pos()[1] - y_margin) // size
                    # check if that position is already marked
                    if self.status[col1][row1] == 1 or self.status[col1][row1] == -1:
                        print("dont choose again!")
                        break
                    else:
                        self.empty_cell = self.empty_cell - 1
                        print(self.empty_cell)
                        # update board's value, make the move and change turnA to True
                        self.value = self.aiplayer.evaluation(col1,row1,self.value,self.status,-1)
                        self.status[col1][row1] = -1
                        self.turnA = not self.turnA

    def draw(self, surface):
        global size, x_margin, y_margin
        # tim cach sua lai cai nay
        # set size of each square and board's margin
        size = 40
        x_margin = 10
        y_margin = 10
        # draw the board
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
                # draw nothing if square is empty
                else:
                    text = font.render('', True, (0, 0, 0))
                surface.blit(text, (k * 40 + 20, l * 40))

# this class includes help methods that can be used globally
class ultility:
    @staticmethod
    def checkInBound(col1, row1, COL, ROW):
        return 0 <= col1 < COL and 0 <= row1 < ROW

    # this counting method takes in x,y position and counts number of possible patterns (horizontally, vertically
    # and diagonally) containing that position
    @staticmethod
    def counting(x_position, y_position, pattern, COL, ROW, status):
        # set unit directions
        dir = [[1, 0], [1, 1], [0, 1], [-1, 1]]
        # prepare column, row, length, count
        length = len(pattern)
        count = 0

        # loop through all 4 directions
        for direction in range(4):
            # find number of squares that we can go back to check for patterns in a particular direction
            if dir[direction][0] * dir[direction][1] == 0:
                numberOfGoBack = dir[direction][0] * min(5, x_position) + dir[direction][1] * min(5, y_position)
            elif dir[direction][0] == 1:
                numberOfGoBack = min(5, x_position, y_position)
            else:
                numberOfGoBack = min(5, COL - 1 - x_position, y_position)
            # very first starting point after finding out numberOfGoBack
            x_starting = x_position - numberOfGoBack * dir[direction][0]
            y_starting = y_position - numberOfGoBack * dir[direction][1]
            # move through all possible patterns in a row/col/diag
            for i in range(numberOfGoBack+1):
                # get a new starting point
                row1 = y_starting + i*dir[direction][1]
                col1 = x_starting + i*dir[direction][0]
                index = 0
                # see if every square in a checked row/col/diag has the same status to a pattern
                while index < length and ultility.checkInBound(col1, row1, COL, ROW) \
                        and status[col1][row1] == pattern[index]:
                    # go through every square
                    row1 = row1 + dir[direction][1]
                    col1 = col1 + dir[direction][0]
                    index += 1
                # if we found one pattern
                if index == length:
                    count += 1
        return count

    @staticmethod
    def checkWin(value):
        return value % 10 != 0 # all pattern's points are divisible by 10 except for the winning one

class AIPlayer(object):
    def __init__(self, depth, COL, ROW, pattern_dict):
        self.depth = depth
        self.ROW = ROW
        self.COL = COL
        self.pattern_dict = pattern_dict
        # initialize values
        self.next_move = [-1, -1]
        self.next_value = 0

    # this method finds the optimized values and moves for either AI or human turn, given current status and depth that
    # we want to examine. Alpha beta prunning is used to pass unnecessary status when dfs-ing through status "tree"
    def miniMax(self, status, value, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or ultility.checkWin(value):
            return value
        # assume that maximizing player is AI because its move is marked as 1
        if maximizingPlayer:
            # initialize max value
            maxEval = -math.inf
            # look for possible remaining positions
            for position in self.childOf(status):
                # get the position and calculate the value if make the move in that position
                k, l = position[0], position[1]
                new_val = self.evaluation(k, l, value, status, 1)
                status[k][l] = 1
                # going down to depth - 1, which is opponent's turn then continue dfs-ing to get the optimal value
                eval = self.miniMax(status, new_val, depth - 1, alpha, beta, False)
                if eval > maxEval:
                    # reset max value to eval and set next move and next value according to current checked position
                    maxEval = eval
                    if depth == self.depth:
                        self.next_move = [k, l]
                        self.next_value = new_val
                alpha = max(alpha, eval)
                # delete the move for checking other positions
                status[k][l] = 0
                if beta <= alpha:
                    break
            return maxEval
        # in terms of minimizing player
        else:
            minEval = math.inf
            for position in self.childOf(status):
                k, l = position[0], position[1]
                new_val = self.evaluation(k, l, value, status, -1)
                status[k][l] = -1
                eval = self.miniMax(status, new_val, depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                beta = min(beta, eval)
                status[k][l] = 0
                if beta <= alpha:
                    break
            return minEval

    # this method takes in current board's value and intended move and returns the value after that move is made
    # the idea of this method is to calculate the difference in number of patterns, thus value, around checked position,
    # then add that difference to current board's value
    def evaluation(self, new_x, new_y, currentBoardEval, status, turn):
        value_before = 0
        value_after = 0
        # check for every pattern in pattern_dict
        for pattern in self.pattern_dict:
            value_before += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status) * self.pattern_dict[pattern]
            # make the move then calculate value_after
            status[new_x][new_y] = turn
            value_after += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status) * self.pattern_dict[
                pattern]
            # delete the move
            status[new_x][new_y] = 0
        return currentBoardEval + value_after - value_before

    # this method returns all possible moves that can be made in a give board status
    def childOf(self, status):
        for k in range(self.COL):
            for l in range(self.ROW):
                if status[k][l] == 0:
                    yield [k, l]

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

# A pattern dictionary of winning moves
def createPatternDict():
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

# Create Buttons Class
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

#Main Screen
def main():
    # prepare
    global width, height, score, ROW, COL
    ROW = 6
    COL = 6
    score = 0
    pygame.init()
    width = 650
    height = width
    frame = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Game')
    frame.fill((0, 0, 0))
    # instantiate the game
    startBoard()
    # main loop
    flag = True
    while flag:
        button = pygame.Rect(50, 100, 100, 50)
        pygame.draw.rect(frame, (255, 0, 0), button)
        key.listen()
        reDraw(frame)
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

white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)
lessGray = (192,192,192)

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
    


main_menu()