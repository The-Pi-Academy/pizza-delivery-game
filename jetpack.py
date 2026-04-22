import pygame
from constants import DK_GRAY, GRAY, ORANGE, YELLOW, SCREEN_W, SCREEN_H


class JetpackItem:
    """World-space jetpack pickup — press E to equip, E again to drop."""
    W, H = 24, 32

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.active = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def draw(self, surface: pygame.Surface, cam_x: float, cam_y: float = 0) -> None:
        if not self.active:
            return
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        if sx + self.W < -10 or sx > SCREEN_W + 10 or sy + self.H < -10 or sy > SCREEN_H + 10:
            return
        # Tank body
        pygame.draw.rect(surface, DK_GRAY, (sx + 4, sy + 2, 16, 26))
        pygame.draw.rect(surface, GRAY,    (sx + 6, sy + 4, 12, 22))
        # Nozzles
        pygame.draw.rect(surface, (50, 50, 50), (sx + 5,  sy + 26, 5, 6))
        pygame.draw.rect(surface, (50, 50, 50), (sx + 14, sy + 26, 5, 6))
        # Shoulder strap
        pygame.draw.rect(surface, (100, 70, 40), (sx + 8, sy, 8, 4))
        # Flame hint at nozzles
        pygame.draw.circle(surface, ORANGE, (sx + 7,  sy + 32), 3)
        pygame.draw.circle(surface, ORANGE, (sx + 17, sy + 32), 3)
        # [E] prompt above
        font = pygame.font.Font(None, 20)
        surf = font.render("[E]", True, YELLOW)
        surface.blit(surf, (sx + 4, sy - 16))
