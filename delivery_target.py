import math
import pygame
from constants import (
    STONE, DK_STONE, DK_BROWN, LT_BLUE, RED, YELLOW,
)


class DeliveryTarget:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.delivered = False

    @property
    def door_rect(self):
        return pygame.Rect(self.x + 20, self.y + 55, 28, 35)

    def draw(self, surface, cam_x, cam_y=0):
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        t  = pygame.time.get_ticks()

        # Foundation
        pygame.draw.rect(surface, DK_STONE, (sx - 5, sy + 88, 90, 8))

        # Main tower body
        pygame.draw.rect(surface, STONE, (sx, sy + 20, 80, 70))
        for row in range(8):
            ry     = sy + 22 + row * 9
            offset = 12 if row % 2 else 0
            for col in range(4):
                pygame.draw.rect(surface, DK_STONE, (sx + col * 20 + offset, ry, 18, 8), 1)

        # Battlement top
        pygame.draw.rect(surface, DK_STONE, (sx, sy + 6, 80, 16))
        for i in range(5):
            pygame.draw.rect(surface, DK_STONE, (sx + i * 16, sy - 6, 11, 14))

        # Door arch
        pygame.draw.rect(surface,   DK_BROWN,      (sx + 20, sy + 55, 28, 35))
        pygame.draw.ellipse(surface, DK_BROWN,      (sx + 19, sy + 44, 30, 20))
        pygame.draw.rect(surface,   (40, 30, 15),   (sx + 23, sy + 57,  7, 33))
        pygame.draw.rect(surface,   (40, 30, 15),   (sx + 33, sy + 57,  7, 33))

        # Windows
        pygame.draw.rect(surface, LT_BLUE, (sx + 8,  sy + 30, 14, 16))
        pygame.draw.rect(surface, LT_BLUE, (sx + 58, sy + 30, 14, 16))
        pygame.draw.line(surface, DK_STONE, (sx + 15, sy + 30), (sx + 15, sy + 46), 1)
        pygame.draw.line(surface, DK_STONE, (sx + 65, sy + 30), (sx + 65, sy + 46), 1)

        # Flag pole + animated flag
        pygame.draw.rect(surface, DK_STONE, (sx + 37, sy - 30, 3, 30))
        flag_wave = int(math.sin(t * 0.004) * 3)
        pygame.draw.polygon(surface, RED, [
            (sx + 40, sy - 28),
            (sx + 55, sy - 23 + flag_wave),
            (sx + 40, sy - 18),
        ])

        # Side towers
        for tx in [sx - 18, sx + 65]:
            pygame.draw.rect(surface, STONE,    (tx, sy + 30, 22, 60))
            pygame.draw.rect(surface, DK_STONE, (tx, sy + 18, 22, 14))
            for i in range(3):
                pygame.draw.rect(surface, DK_STONE, (tx + i * 8, sy + 10, 6, 10))

        # Delivery indicator (bouncing arrow + label)
        if not self.delivered:
            bounce  = int(math.sin(t * 0.005) * 6)
            font_sm = pygame.font.Font(None, 22)
            lbl     = font_sm.render("DELIVER HERE!", True, YELLOW)
            surface.blit(lbl, (sx + 40 - lbl.get_width() // 2, sy - 55 + bounce))
            pygame.draw.polygon(surface, YELLOW, [
                (sx + 40, sy - 35 + bounce),
                (sx + 34, sy - 44 + bounce),
                (sx + 46, sy - 44 + bounce),
            ])
