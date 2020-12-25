from ultility import ultility
import math
from random import randint


class AIPlayer(object):
    def __init__(self, depth, COL, ROW, patternDict):
        self.depth = depth
        self.ROW = ROW
        self.COL = COL
        self.patternDict = patternDict
        # initialize values
        self.nextMove = [-1, -1]
        self.next_value = 0
        self.next_bound = None

    # this method finds the optimized values and moves for either AI or human turn, given current status and depth that
    # we want to examine. Alpha beta prunning is used to pass unnecessary status when dfs-ing through status "tree"
    def miniMax(self, status, bound, value, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or ultility.checkWin(value):
            return value
        # assume that maximizing player is AI because its move is marked as 1
        if maximizingPlayer:
            # initialize max value
            maxEval = -math.inf
            # look for possible remaining positions
            for position in self.childOf(bound):
                # get the position
                k, l = position[0], position[1]
                # create new boundary & update its percentage
                # and calculate the value if make the move in that position
                newBound = dict(bound)
                new_val = self.evaluation(k, l, value, status, 1, newBound)
                status[k][l] = 1
                # update the boundary based on the move just played
                self.updateBound(newBound, status, k, l)
                # going down to depth - 1, which is opponent's turn then continue dfs-ing to get the optimal value
                eval = self.miniMax(status, newBound, new_val, depth - 1, alpha, beta, False)
                if eval > maxEval:
                    # reset max value to eval and set next move and next value according to current checked position
                    maxEval = eval
                    if depth == self.depth:
                        self.nextMove = [k, l]
                        self.next_value = new_val
                        self.next_bound = newBound
                alpha = max(alpha, eval)
                # delete the move for checking other positions
                status[k][l] = 0
                # delete the new boundary
                del newBound
                if beta <= alpha:
                    break
            return maxEval
        # in terms of minimizing player
        else:
            minEval = math.inf
            for position in self.childOf(bound):
                k, l = position[0], position[1]
                newBound = dict(bound)
                new_val = self.evaluation(k, l, value, status, -1, newBound)
                status[k][l] = -1
                # update the boundary based on the move just played
                self.updateBound(newBound, status, k, l)
                eval = self.miniMax(status, newBound, new_val, depth - 1, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    if depth == self.depth:
                        self.nextMove = [k, l]
                        self.next_value = new_val
                        self.next_bound = newBound
                beta = min(beta, eval)
                status[k][l] = 0
                # delete the new boundary
                del newBound
                if beta <= alpha:
                    break
            return minEval

    # this method takes in current board's value and intended move and returns the value after that move is made
    # the idea of this method is to calculate the difference in number of patterns, thus value, around checked position,
    # then add that difference to current board's value
    def evaluation(self, new_x, new_y, currentBoardEval, status, turn, bound):
        valueBefore = 0
        valueAfter = 0
        # check for every pattern in patternDict
        for pattern in self.patternDict:
            score = self.patternDict[pattern]
            valueBefore += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status, abs(score), bound, -1)*score
            # make the move then calculate valueAfter,
            # this time, also update the boundary percentage
            status[new_x][new_y] = turn
            valueAfter += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status, abs(score), bound, 1)*score
            # delete the move
            status[new_x][new_y] = 0
        return currentBoardEval + valueAfter - valueBefore

    # Update new boundary for possible moves given the recently-played move
    def updateBound(self, newBound, status, new_x, new_y):
        # get rid of the played position
        played = ultility.getNumber(new_x, new_y, self.COL)
        if played in newBound:
            newBound.pop(played)
        # check to add new position
        directions = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]  # [col, row]
        for dir in directions:
            new_col = new_x + dir[0]
            new_row = new_y + dir[1]
            if ultility.checkInBound(new_col, new_row, self.COL, self.ROW) and status[new_col][new_row] == 0:
                num = ultility.getNumber(new_col, new_row, self.COL)
                if not (num in newBound):  # if not previously been updated in def evaluation
                    newBound[num] = 1

    # this method returns all possible moves that can be made in a given board status
    def childOf(self, bound):
        for pos in sorted(bound.items(), key=lambda ele: ele[1], reverse=True):
            yield ultility.getPosition(pos[0], self.COL)