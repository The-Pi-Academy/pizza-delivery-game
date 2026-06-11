import pygame
from constants import (
    LEVEL_WIDTH, SCREEN_HEIGHT,
    YELLOW, DK_ORANGE, RED,
)


class PizzaSlice:
    def __init__(self, x, y, direction, speed=14, speed_x=None, speed_y=0.0):
        self.x         = float(x)
        self.y         = float(y)
        self.direction = direction   # +1 right, -1 left
        self.speed_x   = speed_x if speed_x is not None else speed * direction
        self.speed_y   = speed_y
        self.w         = 20
        self.h         = 14
        self.active    = True
        self.damage    = 30

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, platforms):
        self.x       += self.speed_x
        self.speed_y += 0.18
        self.y       += self.speed_y
        if self.x < -50 or self.x > LEVEL_WIDTH + 50 or self.y > SCREEN_HEIGHT + 50 or self.y < -3000:
            self.active = False
            return
        for p in platforms:
            if self.rect.colliderect(p):
                self.active = False
                return

    def draw(self, surface, cam_x, cam_y=0):
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        hh = self.h // 2

        if self.direction > 0:
            tip  = (screen_x + self.w, screen_y + hh)
            top  = (screen_x, screen_y)
            bot  = (screen_x, screen_y + self.h)
            pep1 = (screen_x + 8,  screen_y + hh - 2)
            pep2 = (screen_x + 13, screen_y + hh + 2)
        else:
            tip  = (screen_x, screen_y + hh)
            top  = (screen_x + self.w, screen_y)
            bot  = (screen_x + self.w, screen_y + self.h)
            pep1 = (screen_x + self.w - 8,  screen_y + hh - 2)
            pep2 = (screen_x + self.w - 13, screen_y + hh + 2)

        pygame.draw.polygon(surface, YELLOW, [top, bot, tip])
        pygame.draw.line(surface, DK_ORANGE, top, bot, 4)
        pygame.draw.circle(surface, RED, pep1, 2)
        pygame.draw.circle(surface, RED, pep2, 2)
