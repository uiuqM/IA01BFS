from collections import deque
import sys


class State ():
    def __init__(self):
        self.board = [
            ["--", "kn", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
        ]

        self.moveLog = []

    def MakeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        self.moveLog.append(move)



class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e":4, "f":5, "g":6, "h":7}

    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]

        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]

        self.pieceMoved = self.startRow, self.startCol

        self.pieceCaptured = board[self.endRow][self.endCol]

        self.pieceCaptured = self.endRow, self.endCol

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]


# Below lists detail all eight possible movements for a knight
possible_moves = {(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)}

def isValid(x, y, N):
    return not (x < 0 or y < 0 or x >= N or y >= N)

def highlightSquare(screen, st, move, sqSelected):

    pass


def findShortestDistance(startSq, endSq, board):
    startRow = startSq[0]
    startCol = startSq[1]

    endRow = endSq[0]
    endCol = endSq[1]

    level = 0

    # set to check if the matrix cell is visited before or not
    visited = set()
 
    # create a queue and enqueue the first node
    q = deque([(startRow, startCol, level)])
 
    # loop till queue is empty
    while q:
 
        # dequeue front node and process it
        cur_row, cur_col, level = q.popleft()

        print((cur_row, cur_col), level)
 
        # if the destination is reached, return level from tree
        if cur_row == endRow and cur_col == endCol:
            return level
 
        for dx, dy in possible_moves:
            # skip if the location is visited before or out of range of the board
            if ( 0 <= cur_row + dx <= 8 and 0 <= cur_col + dy <= 8 and (cur_row + dx, cur_col + dy) not in visited):
                visited.add((cur_row + dx, cur_col + dy))
                q.append((cur_row + dx, cur_col + dy, level+1))

    # return infinity if the path is not possible
    return sys.maxsize