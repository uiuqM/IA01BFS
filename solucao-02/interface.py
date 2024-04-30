import pygame
from tkinter import *
from tkinter import messagebox
from pygame import Vector2
import random

image_path = "knight.png"

start_position = (random.randint(0, 7), random.randint(0, 7))

window_size = 800
cell_size = int(window_size / 8)
draw_path = True

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
BROWN = (102, 51, 0)
CREAM = (255, 204, 153)
LIGHT_GREEN = (60, 179, 113)
DARK_GREN = (46, 99, 71)
BLUE = (106, 90, 205)

background_color = CREAM
cell_color = BROWN
line_color = CREAM

simulation_ticks = 3  # 0 Remover atraso


class Rider(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int):
        super().__init__()

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

        self.rect = self.image.get_rect()
        self.set_position(x, y)

    def set_position(self, x: int, y: int):

        pos = get_position(x, y)

        self.rect.x = pos.x
        self.rect.y = pos.y

        if not cell_is_check(x, y):
            check_cells.append((x, y))
        else:
            error_cells.append((x, y))

    def get_position(self) -> Vector2:
        return get_cell_position(int(self.rect.x), int(self.rect.y))

    def move_to_position(self, x: int, y: int):
        pos = self.get_position()

        if int(abs(pos.x - x) + abs(pos.y - y)) != 3:
            error("Erro: número incorreto de casas cobertas")
            return

        movements.append([(int(pos.x), int(pos.y)), (x, y)])
        self.set_position(x, y)

    def move_position(self, x: int, y: int):
        pos = self.get_position()

        if int(abs(pos.x - x) + abs(pos.y - y)) != 3:
            error("Erro: número incorreto de casas cobertas")
            return

        movements.append([(pos.x, pos.y), (pos.x + x, pos.y + y)])
        self.set_position(int(pos.x + x), int(pos.y + y))


def get_cell_position(x: int, y: int) -> Vector2:
    return Vector2(x / cell_size, (-y + (window_size - cell_size)) / cell_size)


def get_position(x: int, y: int) -> Vector2:
    return Vector2(x * cell_size, -y * cell_size + (window_size - cell_size))


def cell_is_check(x: int, y: int) -> bool:
    return (x, y) in check_cells


def draw_grid():
    screen.fill(background_color)

    for x in range(0, window_size, cell_size):
        for y in range(0, window_size, cell_size):

            pos = get_cell_position(x, y)

            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, line_color, rect, 1)

            color = None

            if (pos.x, pos.y) in error_cells:
                color = RED
            elif (pos.x, pos.y) == start_position:
                color = BLUE
            elif cell_is_check(int(pos.x), int(pos.y)):
                if (x / cell_size) % 2 == (y / cell_size) % 2:
                    color = DARK_GREN
                else:
                    color = LIGHT_GREEN

            elif (x / cell_size) % 2 == (y / cell_size) % 2:
                color = cell_color

            if color is not None:
                pygame.draw.rect(screen, color, [x, y, cell_size, cell_size])


def update():
    # RESOLUTION
    path_method()

    # INPUTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # GRAPHIQUE
    draw_grid()

    if draw_path:
        for c in movements:
            pos = get_position(c[0][0], c[0][1])
            new_pos = get_position(c[1][0], c[1][1])

            x = (pos.x + cell_size/2, pos.y + cell_size/2)
            y = (new_pos.x + cell_size/2, new_pos.y + cell_size/2)

            pygame.draw.line(screen, BLACK, x, y, 2)

    screen.blit(rider.image, rider.rect)

    pygame.display.flip()
    clock.tick(simulation_ticks)

    if len(check_cells) == 64 or len(error_cells) >= 1:
        return False
    else:
        return True


def path_method():

    path = [[2, 51, 6, 15, 64, 25, 28, 23],
            [7, 14, 1, 50, 5, 22, 43, 26],
            [52, 3, 8, 63, 16, 27, 24, 29],
            [9, 62, 13, 4, 49, 42, 21, 44],
            [12, 53, 10, 17, 36, 45, 30, 41],
            [61, 56, 59, 48, 31, 40, 35, 20],
            [58, 11, 54, 37, 18, 33, 46, 39],
            [55, 60, 57, 32, 47, 38, 19, 34]]

    pos = rider.get_position()
    index = path[7 - int(pos.y)][int(pos.x)]

    for x in range(len(path[0])):
        for y in range(len(path)):
            if path[7 - y][x] == (index % 64) + 1:
                rider.move_to_position(x, y)
                break


def error(log):
    pygame.display.set_caption(log)

    Tk().wm_withdraw()
    messagebox.showinfo("Erro /!\\", log)

    pygame.quit()


def display_result():
    pygame.display.set_caption("Cavalos -> Número de casas válidas : " + str(len(check_cells)))

    Tk().wm_withdraw()
    messagebox.showinfo("Resultados", "Número de casas válidas: " + str(len(check_cells)))


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption("Cavalos")
    screen = pygame.display.set_mode((window_size, window_size))
    clock = pygame.time.Clock()

    # Affichage du damier + gestion des cellules
    check_cells = []
    error_cells = []

    movements = []

    draw_grid()

    # Mise en place du cavalier
    rider = Rider(start_position[0], start_position[1])

    # Boucle update
    running = True
    while running:
        running = update()

    # Fin du programme (+ affichage des stats)
    display_result()
    pygame.quit()