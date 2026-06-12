import pygame
from grid import to_px
from constants import DK_GRAY, GRAY, ORANGE, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY


class JetpackItem:
    """World-space jetpack pickup — press E to equip, E again to drop."""
    W, H = 24, 32

    def __init__(self, grid_x: float, grid_y: float):
        # Constructor args are grid coordinates — convert to pixels here.
        # grid_y is the row the item rests on, so offset up by its height.
        self.x       = float(to_px(grid_x))
        self.y       = float(to_px(grid_y) - self.H)
        self.speed_y = 0.0
        self.active  = True

    @classmethod
    def from_pixels(cls, x: float, y: float) -> "JetpackItem":
        """Build directly from pixel coordinates (e.g. dropping at the player's feet)."""
        item = cls(0, 0)
        item.x = float(x)
        item.y = float(y)
        return item

    def update(self, platforms) -> None:
        if not self.active:
            return
        self.speed_y = min(self.speed_y + GRAVITY, 22)
        self.y += self.speed_y
        for p in platforms:
            if self.rect.colliderect(p) and self.speed_y > 0:
                self.y       = p.top - self.H
                self.speed_y = 0.0

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
