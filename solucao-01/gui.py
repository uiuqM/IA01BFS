from time import sleep
import pygame
from pygame import *
import board
from collections import deque
import sys

WIDTH = HEIGHT = 512
DIMENSION = 8
MAX_FPS = 15
SQ_SIZE = HEIGHT/DIMENSION

knight = pygame.image.load("img/knight.png")

knight = pygame.transform.scale(knight, (60, 60))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("White"))
    st =  board.State()
    print(st.board)
    drawBoard(screen)
    drawPieces(screen, board.State().board)
    running = True
    sqSelected = ()
    playerClicks = []

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = int(location[0]//SQ_SIZE)
                row = int(location[1]//SQ_SIZE)
                if (sqSelected == (row, col)):
                    sqSelected = ()
                    playerClicks = []
                sqSelected = (row, col)
                playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    findShortestDistance(playerClicks[0], playerClicks[1], screen, st)
                    
                    move = board.Move(playerClicks[0], playerClicks[1], st.board)

                    print(playerClicks)
                    print(move.getChessNotation())

                    st.MakeMove(move)

                    sqSelected = ()
                    playerClicks = []

            drawState(screen, st, sqSelected)


        clock.tick(MAX_FPS)
        pygame.display.flip()

def highlightSquare(screen, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(pygame.Color('blue'))
        screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

def highlightMove(screen, sqSelected, level):
    if sqSelected != ():
        r, c = sqSelected
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        font = pygame.font.SysFont("monospace", 60)
        label = font.render(str(level), 1, (0, 0, 0))
        screen.blit(label, (c*SQ_SIZE, r*SQ_SIZE))
        #pygame.display.set_caption(str(level))
    """if sqSelected != ():
        r, c = sqSelected
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(150)
        s.fill(pygame.Color('red'))
        screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
"""
def showLevel(screen, level):
    phrase = "Current minimum is: "
    font = pygame.font.SysFont("monospace", 40)
    label = font.render(str(level), 1, (255, 255, 0))
    screen.blit(label, (250, 250))
    pygame.display.set_caption(phrase + str(level))

def animateMove(move, screen, board, clock):
    pass

def drawState(screen, st, sqSelected, isAlgo=False, level=None):
    drawBoard(screen)
    if (isAlgo):
        highlightMove(screen, sqSelected, level)
    highlightSquare(screen, sqSelected)
    drawPieces(screen, st.board)

def drawBoard(screen):
    colors = (pygame.Color("white"), pygame.Color("dark green"))

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j) %2)]
            pygame.draw.rect(screen, color, pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]

            if piece != "--":
                screen.blit(knight, pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Below lists detail all eight possible movements for a knight
possible_moves = {(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)}

def findShortestDistance(startSq, endSq, screen, st):
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

        move = (cur_row, cur_col)

        drawState(screen, st, move, isAlgo=True, level=level)
        sleep(0.3)

        # if the destination is reached, return level from tree
        if cur_row == endRow and cur_col == endCol:
            showLevel(screen, level)
            pygame.display.flip()
            return level
 
        for dx, dy in possible_moves:
            # skip if the location is visited before or out of range of the board
            if ( 0 <= cur_row + dx <= 8 and 0 <= cur_col + dy <= 8 and (cur_row + dx, cur_col + dy) not in visited):

                visited.add((cur_row + dx, cur_col + dy))
                q.append((cur_row + dx, cur_col + dy, level+1))
                pygame.display.flip()

    # return infinity if the path is not possible
    return sys.maxsize

if __name__ == "__main__":
    main()
