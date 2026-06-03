import pygame
import random

pygame.init()

WIDTH = 500
ROWS = 20

class Cube:
    rows = ROWS
    w = WIDTH

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny

        self.pos = (
            self.pos[0] + self.dirnx,
            self.pos[1] + self.dirny
        )

    def draw(self, surface, eyes=False):

        dis = self.w // self.rows

        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(
            surface,
            self.color,
            (i * dis + 1, j * dis + 1, dis - 2, dis - 2)
        )

        if eyes:
            centre = dis // 2
            radius = 3

            circleMiddle = (
                i * dis + centre - radius,
                j * dis + 8
            )

            circleMiddle2 = (
                i * dis + dis - radius * 2,
                j * dis + 8
            )

            pygame.draw.circle(surface, (0, 0, 0),
                               circleMiddle, radius)

            pygame.draw.circle(surface, (0, 0, 0),
                               circleMiddle2, radius)


class Snake:

    def __init__(self, color, pos):

        self.body = []
        self.turns = {}

        self.color = color

        self.head = Cube(pos)

        self.body.append(self.head)

        self.dirnx = 0
        self.dirny = 1

    def move(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos] = [self.dirnx, self.dirny]

        elif keys[pygame.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos] = [self.dirnx, self.dirny]

        elif keys[pygame.K_UP]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos] = [self.dirnx, self.dirny]

        elif keys[pygame.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):

            p = c.pos

            if p in self.turns:

                turn = self.turns[p]

                c.move(turn[0], turn[1])

                if i == len(self.body) - 1:
                    self.turns.pop(p)

            else:

                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (ROWS - 1, c.pos[1])

                elif c.dirnx == 1 and c.pos[0] >= ROWS - 1:
                    c.pos = (0, c.pos[1])

                elif c.dirny == 1 and c.pos[1] >= ROWS - 1:
                    c.pos = (c.pos[0], 0)

                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], ROWS - 1)

                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):

        self.head = Cube(pos)

        self.body = [self.head]

        self.turns = {}

        self.dirnx = 0
        self.dirny = 1

    def addCube(self):

        tail = self.body[-1]

        dx = tail.dirnx
        dy = tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(
                Cube((tail.pos[0] - 1, tail.pos[1]))
            )

        elif dx == -1 and dy == 0:
            self.body.append(
                Cube((tail.pos[0] + 1, tail.pos[1]))
            )

        elif dx == 0 and dy == 1:
            self.body.append(
                Cube((tail.pos[0], tail.pos[1] - 1))
            )

        elif dx == 0 and dy == -1:
            self.body.append(
                Cube((tail.pos[0], tail.pos[1] + 1))
            )

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):

        for i, c in enumerate(self.body):

            if i == 0:
                c.draw(surface, True)

            else:
                c.draw(surface)


def drawGrid(w, rows, surface):

    sizeBtwn = w // rows

    x = 0
    y = 0

    for _ in range(rows):

        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(
            surface,
            (255, 255, 255),
            (x, 0),
            (x, w)
        )

        pygame.draw.line(
            surface,
            (255, 255, 255),
            (0, y),
            (w, y)
        )


def randomSnack(rows, item):

    positions = [cube.pos for cube in item.body]

    while True:

        x = random.randrange(rows)
        y = random.randrange(rows)

        if (x, y) not in positions:
            return (x, y)


def redrawWindow(surface):

    global snake_obj
    global snack

    surface.fill((0, 0, 0))

    snake_obj.draw(surface)

    snack.draw(surface)

    drawGrid(WIDTH, ROWS, surface)

    pygame.display.update()


def main():

    global snake_obj
    global snack

    win = pygame.display.set_mode((WIDTH, WIDTH))

    pygame.display.set_caption("Snake")

    snake_obj = Snake((255, 0, 0), (10, 10))

    snack = Cube(
        randomSnack(ROWS, snake_obj),
        color=(0, 255, 0)
    )

    clock = pygame.time.Clock()

    while True:

        pygame.time.delay(50)

        clock.tick(10)

        snake_obj.move()

        if snake_obj.head.pos == snack.pos:

            snake_obj.addCube()

            snack = Cube(
                randomSnack(ROWS, snake_obj),
                color=(0, 255, 0)
            )

        for x in range(len(snake_obj.body)):

            if snake_obj.body[x].pos in list(
                map(lambda z: z.pos,
                    snake_obj.body[x + 1:])
            ):
                snake_obj.reset((10, 10))
                break

        redrawWindow(win)


main()