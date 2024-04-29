import pygame
from pygame import *
import board

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
                    print(board.findShortestDistance(playerClicks[0], playerClicks[1], st.board))
                    
                    move = board.Move(playerClicks[0], playerClicks[1], st.board)

                    print(playerClicks)
                    print(move.getChessNotation())

                    st.MakeMove(move)

                    sqSelected = ()
                    playerClicks = []
            drawState(screen, st)


        clock.tick(MAX_FPS)
        pygame.display.flip()

def drawState(screen, st):
    drawBoard(screen)
    drawPieces(screen, st.board)

def drawBoard(screen):
    colors = (pygame.Color("white"), pygame.Color("gray"))

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


if __name__ == "__main__":
    main()
