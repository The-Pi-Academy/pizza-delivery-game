import math
import pygame
from grid import to_px
from constants import (
    STONE, DK_STONE, DK_BROWN, LT_BLUE, RED, YELLOW, DK_ORANGE,
)


class DeliveryTarget:
    def __init__(self, grid_x, grid_y, required_slices=1):
        # Constructor args are grid coordinates — convert to pixels here.
        self.x               = to_px(grid_x)
        self.y               = to_px(grid_y)
        self.required_slices = required_slices
        self.slices_delivered = 0

    @property
    def delivered(self):
        return self.slices_delivered >= self.required_slices

    @property
    def door_rect(self):
        return pygame.Rect(self.x + 20, self.y + 55, 28, 35)

    @property
    def hit_rect(self):
        """Full castle area that counts as a valid pizza delivery hit."""
        return pygame.Rect(self.x - 18, self.y - 6, 116, 102)

    def receive_slice(self):
        if not self.delivered:
            self.slices_delivered += 1

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

        # Order indicator: fraction + pizza slice icon
        if not self.delivered:
            bounce    = int(math.sin(current_time * 0.005) * 6)
            frac_font = pygame.font.Font(None, 36)
            frac_surf = frac_font.render(f"{self.slices_delivered}/{self.required_slices}", True, YELLOW)

            icon_w, icon_h = 10, 16
            gap     = 6
            total_w = frac_surf.get_width() + gap + icon_w
            fx      = screen_x + 40 - total_w // 2
            fy      = screen_y - 62 + bounce

            surface.blit(frac_surf, (fx, fy))

            # Mini pizza slice icon (tip pointing down, 90° CW)
            ix  = fx + frac_surf.get_width() + gap
            iy  = fy + (frac_surf.get_height() - icon_h) // 2
            ihw = icon_w // 2
            pygame.draw.polygon(surface, YELLOW, [(ix, iy), (ix + icon_w, iy), (ix + ihw, iy + icon_h)])
            pygame.draw.line(surface, DK_ORANGE, (ix, iy), (ix + icon_w, iy), 3)
            pygame.draw.circle(surface, RED, (ix + 4, iy + 5), 2)
            pygame.draw.circle(surface, RED, (ix + 6, iy + 9), 2)
