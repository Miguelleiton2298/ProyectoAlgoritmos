import sys
import pygame
import random
from PIL import Image, ImageSequence

from Constantes import *
from Listas import *

#convierte una imagen tipo PIL a surface de pygame
def pil2surface(pil_img):
    mode, size, data = pil_img.mode, pil_img.size, pil_img.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

#carga una gif animado como una lista de imagenes pygame
def load_gif(filename):
    pil_img = Image.open(filename)
    sprites = []
    if pil_img.format == 'GIF' and pil_img.is_animated:
        for sp in ImageSequence.Iterator(pil_img):
            py_img = pil2surface(sp.convert('RGBA'))
            sprites.append(py_img)
    else:
         sprites.append(pil2surface(pil_img))
    return  sprites

class Snake:
    def __init__(self):
        self.length = PilaLIFO()
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (20, 20, 0)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]
    def turn(self, point):
        if self.length.getLargo() > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % WIDTH), (cur[1] + (y * GRIDSIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length.getLargo():
                self.positions.pop()
    def reset(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (100, 100, 0), r, 1)
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food:
    def __init__(self):
        self.position = (0, 0)
        #random color
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.text = random.choice([" ( ", " ) ", " [ ", " ] ", " { ", " } "])
        self.randomize_position()

    def randomize_position(self):

        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)
        # Cambiar el color de la comida
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Cambiar el texto de la comida
        self.text = random.choice([" ( ", " ) ", " [ ", " ] ", " { ", " } "])


    # agregar mas de una comida al tablero en distintas ibicaciones
    def draw_more1(self, surface):
        for i in range(2):
            r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (100, 100, 0), r, 1)
            # Agregar texto a la comida
            font = pygame.font.SysFont('Arial', 25)
            text = font.render(self.text, True, (0, 0, 0))
            surface.blit(text, (self.position[0], self.position[1]))
            self.randomize_position()


    def draw(self, surface):


        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (100, 100, 0), r, 1)
        # Agregar texto a la comida
        font = pygame.font.SysFont('Arial', 25)
        text = font.render(self.text, True, (0, 0, 0))
        surface.blit(text, (self.position[0], self.position[1]))


def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
         for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (150, 180, 50), r)
            else:
                rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (150, 190, 0), rr)
def main():
    pygame.init()
    # Titulo
    pygame.display.set_caption("SNAKE GAME")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()
    snake.length.Push(1)

    myfont = pygame.font.SysFont("monospace", 30, bold=True, italic=True)

    while (True):
        clock.tick(6)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()

        if snake.get_head_position() == food.position:
            # Agregar mas de una comida
            snake.length.Push(1)
            print(snake.length.getLargo())
            snake.score += 1
            food.draw_more1(surface)

            # Aqui van las condicionales respecto de la comida que coma
            #if comida == 1:

        snake.draw(surface)
        food.draw(surface)


        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (255, 255, 200))
        screen.blit(text, (5, 10))
        pygame.display.update()

if __name__ == '__main__':
    #Main
    main()

    