import pygame
from constants import ORANGE, YELLOW, GRAY, DK_GRAY, SCREEN_W, SCREEN_H


class GasCan:
    """World-space gas can — auto-collected on contact, refuels the jetpack."""
    W, H = 20, 28

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
        # Can body
        pygame.draw.rect(surface, (140, 55, 15), (sx + 2, sy + 6, 16, 22))
        pygame.draw.rect(surface, (190, 85, 35), (sx + 4, sy + 8, 12, 18))
        # Cap / spout
        pygame.draw.rect(surface, GRAY,    (sx + 6, sy + 2, 8, 6))
        pygame.draw.rect(surface, DK_GRAY, (sx + 8, sy,     4, 4))
        # Handle bar
        pygame.draw.rect(surface, (100, 45, 10), (sx, sy + 4, 20, 4))
        # Fuel symbol (orange circle)
        pygame.draw.circle(surface, ORANGE, (sx + 10, sy + 17), 4)
        pygame.draw.circle(surface, YELLOW, (sx + 10, sy + 17), 2)
        # Bouncing label
        t = pygame.time.get_ticks()
        import math
        bounce = int(math.sin(t * 0.006) * 3)
        font = pygame.font.Font(None, 18)
        surf = font.render("GAS", True, ORANGE)
        surface.blit(surf, (sx + 2, sy - 14 + bounce))
