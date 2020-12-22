import pygame
import math

xMargin = None
yMargin = None
size = None

class Board(object):
    def __init__(self, status, value, ROW, COL, aiplayer, patternDict):
        # turnA means AI's turn while !turnA is human's turn
        self.turnA = True # always let AI go first
        self.status = status
        self.value = value
        self.ROW = ROW
        self.COL = COL
        self.aiplayer = aiplayer
        self.patternDict = patternDict

    def listen(self):  # listen to the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # AI's turn
            if self.turnA:
                # call miniMax function so that AI can make its next move
                self.aiplayer.miniMax(self.status, self.value, self.aiplayer.depth, -math.inf, math.inf, True)
                ai_nextMove_x = self.aiplayer.nextMove[0]
                ai_nextMove_y = self.aiplayer.nextMove[1]
                # update board's total value
                self.value = self.aiplayer.next_value
                # make AI's decided next move and change turnA to False
                self.status[ai_nextMove_x][ai_nextMove_y] = 1
                self.turnA = not self.turnA

            # human's turn
            else:
                if pygame.mouse.get_pressed()[0]:
                    # get position of clicked mouse and convert it to according row and column
                    col1 = (pygame.mouse.get_pos()[0] - xMargin) // size
                    row1 = (pygame.mouse.get_pos()[1] - yMargin) // size
                    # check if that position is already marked
                    if self.status[col1][row1] == 1 or self.status[col1][row1] == -1:
                        print("dont choose again!")
                        break
                    else:
                        # update board's value, make the move and change turnA to True
                        self.value = self.aiplayer.evaluation(col1,row1,self.value,self.status,-1)
                        self.status[col1][row1] = -1
                        self.turnA = not self.turnA

    def draw(self, surface):
        global size, xMargin, yMargin
        # set size of each square and board's margin
        size = 40
        xMargin = 10
        yMargin = 10
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
                    text = font.render('x', True, (255, 0, 0))
                elif self.status[k][l] == -1:
                    text = font.render('o', True, (255, 0, 0))
                # draw nothing if square is empty
                else:
                    text = font.render('', True, (0, 0, 0))
                surface.blit(text, (k * 40 + 20, l * 40))
