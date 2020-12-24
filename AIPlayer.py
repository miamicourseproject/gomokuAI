from ultility import ultility
import math


class AIPlayer(object):
    def __init__(self, depth, COL, ROW, patternDict):
        self.depth = depth
        self.ROW = ROW
        self.COL = COL
        self.patternDict = patternDict
        # initialize values
        self.nextMove = [-1, -1]
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
                    if depth == self.depth and maximizingPlayer:
                        self.nextMove = [k, l]
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
                    if depth == self.depth and not maximizingPlayer:
                        self.nextMove = [k, l]
                        self.next_value = new_val
                beta = min(beta, eval)
                status[k][l] = 0
                if beta <= alpha:
                    break
            return minEval

    # this method takes in current board's value and intended move and returns the value after that move is made
    # the idea of this method is to calculate the difference in number of patterns, thus value, around checked position,
    # then add that difference to current board's value
    def evaluation(self, new_x, new_y, currentBoardEval, status, turn):
        valueBefore = 0
        valueAfter = 0
        # check for every pattern in patternDict
        for pattern in self.patternDict:
            valueBefore += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status) * self.patternDict[pattern]
            # make the move then calculate valueAfter
            status[new_x][new_y] = turn
            valueAfter += ultility.counting(new_x, new_y, pattern, self.COL, self.ROW, status) * self.patternDict[
                pattern]
            # delete the move
            status[new_x][new_y] = 0
        return currentBoardEval + valueAfter - valueBefore

    # this method returns all possible moves that can be made in a give board status
    def childOf(self, status):
        for k in range(self.COL):
            for l in range(self.ROW):
                if status[k][l] == 0:
                    yield [k, l]