import math
import pygame
from constants import ORANGE, YELLOW, GRAY, DK_GRAY, SCREEN_WIDTH, SCREEN_HEIGHT


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
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        if screen_x + self.W < -10 or screen_x > SCREEN_WIDTH + 10 or screen_y + self.H < -10 or screen_y > SCREEN_HEIGHT + 10:
            return
        # Can body
        pygame.draw.rect(surface, (140, 55, 15), (screen_x + 2, screen_y + 6, 16, 22))
        pygame.draw.rect(surface, (190, 85, 35), (screen_x + 4, screen_y + 8, 12, 18))
        # Cap / spout
        pygame.draw.rect(surface, GRAY,    (screen_x + 6, screen_y + 2, 8, 6))
        pygame.draw.rect(surface, DK_GRAY, (screen_x + 8, screen_y,     4, 4))
        # Handle bar
        pygame.draw.rect(surface, (100, 45, 10), (screen_x, screen_y + 4, 20, 4))
        # Fuel symbol (orange circle)
        pygame.draw.circle(surface, ORANGE, (screen_x + 10, screen_y + 17), 4)
        pygame.draw.circle(surface, YELLOW, (screen_x + 10, screen_y + 17), 2)
        # Bouncing label
        current_time = pygame.time.get_ticks()
        bounce       = int(math.sin(current_time * 0.006) * 3)
        small_font   = pygame.font.Font(None, 18)
        gas_label    = small_font.render("GAS", True, ORANGE)
        surface.blit(gas_label, (screen_x + 2, screen_y - 14 + bounce))
