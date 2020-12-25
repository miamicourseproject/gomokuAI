import numpy as np
import ctypes
# this class includes help methods that can be used globally
class ultility:
    @staticmethod
    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    @staticmethod
    def checkInBound(col1, row1, COL, ROW):
        return 0 <= col1 < COL and 0 <= row1 < ROW

    # this counting method takes in x,y position and counts number of possible patterns (horizontally, vertically
    # and diagonally) containing that position
    # the flag parameter indicates whether to add or remove the score to or from the bound
    @staticmethod
    def counting(x_position, y_position, pattern, COL, ROW, status, score, bound, flag):
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
            i = 0
            while i < (numberOfGoBack+1):
                # get a new starting point
                row1 = y_starting + i*dir[direction][1]
                col1 = x_starting + i*dir[direction][0]
                index = 0
                # create a list storing empty positions that are fitted in a pattern
                remember = []
                # see if every square in a checked row/col/diag has the same status to a pattern
                while index < length and ultility.checkInBound(col1, row1, COL, ROW) \
                        and status[col1][row1] == pattern[index]:
                    # first check if it's the empty position to store
                    # score is also a flag indicating whether modifying the bound
                    if status[col1][row1] == 0:
                        remember.append(ultility.getNumber(col1, row1, COL))
                    # go through every square
                    row1 = row1 + dir[direction][1]
                    col1 = col1 + dir[direction][0]
                    index += 1
                # if we found one pattern
                if index == length:
                    count += 1
                    for pos in remember:
                        if not(pos in bound):
                            bound[pos] = 0
                        bound[pos] += flag*score  # update better percentage later
                    i += index
                else:
                    i += 1
        return count

    @staticmethod
    def checkWin(value):
        return value > 900000 or value < -900000  #test???

    # Return the ordinal number given the position
    @staticmethod
    def getNumber(col, row, COL):
        return COL * row + col

    # Return position[col, row] given the ordinal number
    @staticmethod
    def getPosition(number, COL):
        return [number % COL, number // COL]

    # Return the decimal form of the given quintery number
    # In this form, {-1: 0, 0: 1, 1: 2}
    @staticmethod
    def quinary2dec(list):
        lowest = 0
        hash = 0
        for num in list:
            hash += (num+1) * (4 ** lowest)
            lowest += 1
        return hash

    # Update the pattern_dict
    # The value of the dict is as follow [point, len, ...(position of blank space)]
    @staticmethod
    def format(dict):
        dict2 = {}
        for key in dict.keys():
            list = [dict[key], len(key)]
            for pos in range(len(key)):
                if key[pos] == 0:
                    list.append(pos)
            list = np.array(list)
            dict2[ultility.quinary2dec(key)] = list

    @staticmethod
    def checkTie(board):
        return board.empty_cell == 0