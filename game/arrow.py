import pygame
from constants import (
    LEVEL_WIDTH, SCREEN_HEIGHT,
    DK_BROWN, GRAY, RED,
)


class Arrow:
    def __init__(self, x, y, direction, speed=14, speed_x=None, speed_y=0.0):
        self.x         = float(x)
        self.y         = float(y)
        self.direction = direction   # +1 right, -1 left
        self.speed_x   = speed_x if speed_x is not None else speed * direction
        self.speed_y   = speed_y
        self.w         = 22
        self.h         = 6
        self.active    = True
        self.damage    = 28

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, platforms):
        self.x       += self.speed_x
        self.speed_y += 0.18   # slight arc
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
        # Shaft
        pygame.draw.line(surface, DK_BROWN, (screen_x, screen_y + 3), (screen_x + self.w - 6, screen_y + 3), 2)
        # Head and feather vary by direction
        tip_x     = screen_x + self.w if self.direction > 0 else screen_x
        feather_x = screen_x          if self.direction > 0 else screen_x + self.w
        if self.direction > 0:
            pygame.draw.polygon(surface, GRAY, [
                (tip_x,     screen_y + 3),
                (tip_x - 7, screen_y),
                (tip_x - 7, screen_y + 6),
            ])
            pygame.draw.polygon(surface, RED, [
                (feather_x,     screen_y + 3),
                (feather_x + 5, screen_y),
                (feather_x + 5, screen_y + 6),
            ])
        else:
            pygame.draw.polygon(surface, GRAY, [
                (tip_x,     screen_y + 3),
                (tip_x + 7, screen_y),
                (tip_x + 7, screen_y + 6),
            ])
            pygame.draw.polygon(surface, RED, [
                (feather_x,     screen_y + 3),
                (feather_x - 5, screen_y),
                (feather_x - 5, screen_y + 6),
            ])
