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
        if (value > 900000):
            return True
        elif (value < -900000):
            return True
        else: return False

    @staticmethod
    def checkTie(board):
        return board.empty_cell == 0