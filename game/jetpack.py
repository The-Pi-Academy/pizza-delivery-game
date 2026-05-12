import pygame
from constants import DK_GRAY, GRAY, ORANGE, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT


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
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        if screen_x + self.W < -10 or screen_x > SCREEN_WIDTH + 10 or screen_y + self.H < -10 or screen_y > SCREEN_HEIGHT + 10:
            return
        # Tank body
        pygame.draw.rect(surface, DK_GRAY, (screen_x + 4, screen_y + 2, 16, 26))
        pygame.draw.rect(surface, GRAY,    (screen_x + 6, screen_y + 4, 12, 22))
        # Nozzles
        pygame.draw.rect(surface, (50, 50, 50), (screen_x + 5,  screen_y + 26, 5, 6))
        pygame.draw.rect(surface, (50, 50, 50), (screen_x + 14, screen_y + 26, 5, 6))
        # Shoulder strap
        pygame.draw.rect(surface, (100, 70, 40), (screen_x + 8, screen_y, 8, 4))
        # Flame hint at nozzles
        pygame.draw.circle(surface, ORANGE, (screen_x + 7,  screen_y + 32), 3)
        pygame.draw.circle(surface, ORANGE, (screen_x + 17, screen_y + 32), 3)
        # [E] prompt above
        prompt_font   = pygame.font.Font(None, 20)
        pickup_prompt = prompt_font.render("[E]", True, YELLOW)
        surface.blit(pickup_prompt, (screen_x + 4, screen_y - 16))
