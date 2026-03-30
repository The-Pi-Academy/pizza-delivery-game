import pygame
import random


class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'colour', 'life', 'max_life', 'size')

    def __init__(self, x, y, colour, vx, vy, life, size=4):
        self.x, self.y   = float(x), float(y)
        self.vx, self.vy = vx, vy
        self.colour      = colour
        self.life        = life
        self.max_life    = life
        self.size        = size

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.25
        self.life -= 1

    def draw(self, surface, cam_x):
        ratio = self.life / self.max_life
        r, g, b = self.colour
        col = (int(r * ratio), int(g * ratio), int(b * ratio))
        sz  = max(1, int(self.size * ratio))
        pygame.draw.circle(surface, col, (int(self.x - cam_x), int(self.y)), sz)


def spawn_hit_particles(particles, x, y, colour, count=8):
    for _ in range(count):
        particles.append(Particle(
            x, y, colour,
            random.uniform(-3.5, 3.5),
            random.uniform(-5.0, -0.5),
            random.randint(20, 35),
            random.randint(3, 6),
        ))
