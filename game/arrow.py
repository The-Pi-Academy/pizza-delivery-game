import pygame
from constants import (
    LEVEL_W, SCREEN_H,
    DK_BROWN, GRAY, RED,
)


class Arrow:
    def __init__(self, x, y, direction, speed=14, vx=None, vy=0.0):
        self.x   = float(x)
        self.y   = float(y)
        self.dir = direction   # +1 right, -1 left
        self.vx  = vx if vx is not None else speed * direction
        self.vy  = vy
        self.w   = 22
        self.h   = 6
        self.active = True
        self.damage = 28

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, platforms):
        self.x += self.vx
        self.vy += 0.18   # slight arc
        self.y  += self.vy
        if self.x < -50 or self.x > LEVEL_W + 50 or self.y > SCREEN_H + 50 or self.y < -3000:
            self.active = False
            return
        for p in platforms:
            if self.rect.colliderect(p):
                self.active = False
                return

    def draw(self, surface, cam_x, cam_y=0):
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        # Shaft
        pygame.draw.line(surface, DK_BROWN, (sx, sy + 3), (sx + self.w - 6, sy + 3), 2)
        # Head and feather vary by direction
        tip_x     = sx + self.w if self.dir > 0 else sx
        feather_x = sx          if self.dir > 0 else sx + self.w
        if self.dir > 0:
            pygame.draw.polygon(surface, GRAY, [
                (tip_x,     sy + 3),
                (tip_x - 7, sy),
                (tip_x - 7, sy + 6),
            ])
            pygame.draw.polygon(surface, RED, [
                (feather_x,     sy + 3),
                (feather_x + 5, sy),
                (feather_x + 5, sy + 6),
            ])
        else:
            pygame.draw.polygon(surface, GRAY, [
                (tip_x,     sy + 3),
                (tip_x + 7, sy),
                (tip_x + 7, sy + 6),
            ])
            pygame.draw.polygon(surface, RED, [
                (feather_x,     sy + 3),
                (feather_x - 5, sy),
                (feather_x - 5, sy + 6),
            ])
