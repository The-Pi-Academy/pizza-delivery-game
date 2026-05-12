import pygame
import random


class Particle:
    __slots__ = ('x', 'y', 'speed_x', 'speed_y', 'colour', 'life', 'max_life', 'size')

    def __init__(self, x, y, colour, speed_x, speed_y, life, size=4):
        self.x, self.y         = float(x), float(y)
        self.speed_x, self.speed_y = speed_x, speed_y
        self.colour            = colour
        self.life              = life
        self.max_life          = life
        self.size              = size

    def update(self):
        self.x       += self.speed_x
        self.y       += self.speed_y
        self.speed_y += 0.25
        self.life    -= 1

    def draw(self, surface, cam_x):
        life_ratio    = self.life / self.max_life
        red, green, blue = self.colour
        faded_color   = (int(red * life_ratio), int(green * life_ratio), int(blue * life_ratio))
        current_size  = max(1, int(self.size * life_ratio))
        pygame.draw.circle(surface, faded_color, (int(self.x - cam_x), int(self.y)), current_size)


def spawn_hit_particles(particles, x, y, colour, count=8):
    for _ in range(count):
        particles.append(Particle(
            x, y, colour,
            random.uniform(-3.5, 3.5),
            random.uniform(-5.0, -0.5),
            random.randint(20, 35),
            random.randint(3, 6),
        ))
