import pygame
from constants import SCREEN_W, SCREEN_H, FPS, WHITE, BLACK


class Button:
    def __init__(self, cx, cy, w, h, label, font):
        self.rect  = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
        self.label = label
        self.font  = font

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        bg_col  = (60, 60, 60) if hovered else (30, 30, 30)
        pygame.draw.rect(surface, bg_col,  self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE,   self.rect, 2, border_radius=6)
        text = self.font.render(self.label, True, WHITE)
        surface.blit(text, (
            self.rect.centerx - text.get_width()  // 2,
            self.rect.centery - text.get_height() // 2,
        ))

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def run_menu(screen, clock, level_count: int) -> int:
    """Block until the player selects a level. Returns the chosen level index (0-based)."""
    font_title  = pygame.font.Font(None, 96)
    font_sub    = pygame.font.Font(None, 38)
    font_button = pygame.font.Font(None, 52)

    cx      = SCREEN_W // 2
    btn_w   = 200
    btn_h   = 60
    spacing = 80
    start_y = SCREEN_H // 2

    buttons = [
        Button(cx, start_y + i * spacing, btn_w, btn_h,
               f"Level {i + 1}", font_button)
        for i in range(level_count)
    ]

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            for i, btn in enumerate(buttons):
                if btn.is_clicked(event):
                    return i

        screen.fill(BLACK)

        title = font_title.render("Pizza Quest", True, WHITE)
        screen.blit(title, (cx - title.get_width() // 2, 160))

        sub = font_sub.render("Choose a level", True, (180, 180, 180))
        screen.blit(sub, (cx - sub.get_width() // 2, start_y - 50))

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
