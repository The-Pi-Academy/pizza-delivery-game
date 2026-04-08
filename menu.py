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


def run_menu(screen, clock):
    """Block until the player clicks a level button. Returns the chosen level number."""
    font_title  = pygame.font.Font(None, 96)
    font_button = pygame.font.Font(None, 52)

    play_btn = Button(SCREEN_W // 2, SCREEN_H // 2, 220, 60, "Play", font_button)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.key == pygame.K_ESCAPE if event.type == pygame.KEYDOWN else False:
                pygame.quit()
                raise SystemExit
            if play_btn.is_clicked(event):
                return 1

        screen.fill(BLACK)

        title = font_title.render("Pi Camp Pizza Delivery", True, WHITE)
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 80))

        play_btn.draw(screen)

        pygame.display.flip()
