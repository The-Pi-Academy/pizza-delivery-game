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
        screen_x     = int(self.x - cam_x)
        screen_y     = int(self.y - cam_y)
        current_time = pygame.time.get_ticks()

        # Foundation
        pygame.draw.rect(surface, DK_STONE, (screen_x - 5, screen_y + 88, 90, 8))

        # Main tower body
        pygame.draw.rect(surface, STONE, (screen_x, screen_y + 20, 80, 70))
        for row in range(8):
            brick_row_y  = screen_y + 22 + row * 9
            brick_offset = 12 if row % 2 else 0
            for col in range(4):
                pygame.draw.rect(surface, DK_STONE, (screen_x + col * 20 + brick_offset, brick_row_y, 18, 8), 1)

        # Battlement top
        pygame.draw.rect(surface, DK_STONE, (screen_x, screen_y + 6, 80, 16))
        for i in range(5):
            pygame.draw.rect(surface, DK_STONE, (screen_x + i * 16, screen_y - 6, 11, 14))

        # Door arch
        pygame.draw.rect(surface,   DK_BROWN,      (screen_x + 20, screen_y + 55, 28, 35))
        pygame.draw.ellipse(surface, DK_BROWN,      (screen_x + 19, screen_y + 44, 30, 20))
        pygame.draw.rect(surface,   (40, 30, 15),   (screen_x + 23, screen_y + 57,  7, 33))
        pygame.draw.rect(surface,   (40, 30, 15),   (screen_x + 33, screen_y + 57,  7, 33))

        # Windows
        pygame.draw.rect(surface, LT_BLUE, (screen_x + 8,  screen_y + 30, 14, 16))
        pygame.draw.rect(surface, LT_BLUE, (screen_x + 58, screen_y + 30, 14, 16))
        pygame.draw.line(surface, DK_STONE, (screen_x + 15, screen_y + 30), (screen_x + 15, screen_y + 46), 1)
        pygame.draw.line(surface, DK_STONE, (screen_x + 65, screen_y + 30), (screen_x + 65, screen_y + 46), 1)

        # Flag pole + animated flag
        pygame.draw.rect(surface, DK_STONE, (screen_x + 37, screen_y - 30, 3, 30))
        flag_wave = int(math.sin(current_time * 0.004) * 3)
        pygame.draw.polygon(surface, RED, [
            (screen_x + 40, screen_y - 28),
            (screen_x + 55, screen_y - 23 + flag_wave),
            (screen_x + 40, screen_y - 18),
        ])

        # Side towers
        for side_tower_x in [screen_x - 18, screen_x + 65]:
            pygame.draw.rect(surface, STONE,    (side_tower_x, screen_y + 30, 22, 60))
            pygame.draw.rect(surface, DK_STONE, (side_tower_x, screen_y + 18, 22, 14))
            for i in range(3):
                pygame.draw.rect(surface, DK_STONE, (side_tower_x + i * 8, screen_y + 10, 6, 10))

        # Delivery indicator (bouncing arrow + label)
        if not self.delivered:
            bounce        = int(math.sin(current_time * 0.005) * 6)
            small_font    = pygame.font.Font(None, 22)
            indicator_label = small_font.render("DELIVER HERE!", True, YELLOW)
            surface.blit(indicator_label, (screen_x + 40 - indicator_label.get_width() // 2, screen_y - 55 + bounce))
            pygame.draw.polygon(surface, YELLOW, [
                (screen_x + 40, screen_y - 35 + bounce),
                (screen_x + 34, screen_y - 44 + bounce),
                (screen_x + 46, screen_y - 44 + bounce),
            ])
