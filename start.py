__author__ = 'NoNotCar'
import pygame, sys, math
from random import randint

pygame.init()
import UniJoy

ssize = (600, 600)
screen = pygame.display.set_mode(ssize)
clock = pygame.time.Clock()
shipmass = 1000
colconv = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255))


class Ship(object):
    def __init__(self, n, ships):
        self.x, self.y = 0, 0
        done = False
        while not done:
            self.x, self.y = randint(100, 500), randint(100, 500)
            done=True
            for ship in ships:
                if self.get_dist(ship.x,ship.y)<300:
                    done=False
        self.xs = 0
        self.ys = 0
        self.j = UniJoy.Unijoy(n)
        self.num = n

    def get_dist(self, x, y):
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        return (dx ** 2 + dy ** 2) ** 0.5

    def update(self):
        jpos = self.j.getstick(1)
        self.xs += jpos[0] / 10
        self.ys += jpos[1] / 10
        self.x += self.xs
        self.y += self.ys


ships = []
for n in range(pygame.joystick.get_count()):
    ships.append(Ship(n,ships))
while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
    for ship in ships[:]:
        pygame.draw.circle(screen, colconv[ship.num], (int(ship.x), int(ship.y)), 3)
        if not (0 <= ship.x <= 600 and 0 <= ship.y <= 600):
            ships.remove(ship)
            pygame.draw.circle(screen, (255, 225, 0), (int(ship.x), int(ship.y)), 30)
        for oship in ships[:]:
            if oship is not ship:
                try:
                    dist = ship.get_dist(oship.x, oship.y)
                    gforce = shipmass / dist ** 2
                    scale = gforce / dist
                    ship.xs += (oship.x - ship.x) * scale
                    ship.ys += (oship.y - ship.y) * scale
                except ZeroDivisionError:
                    ships.remove(ship)
                    ships.remove(oship)
                    pygame.draw.circle(screen, (255, 225, 0), (int(ship.x), int(ship.y)), 30)
    for ship in ships:
        ship.update()
    pygame.display.flip()
    clock.tick(60)
    if len(ships) == 0:
        sys.exit("YOU ALL FAILED")
    elif len(ships) == 1:
        sys.exit("PLAYER %s WINS!" % int(ships[0].num + 1))
