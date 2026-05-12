import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK
from save import load_best_times, format_time


class Button:
    def __init__(self, center_x, center_y, button_width, button_height, label, font):
        self.rect  = pygame.Rect(center_x - button_width // 2, center_y - button_height // 2, button_width, button_height)
        self.label = label
        self.font  = font

    def draw(self, surface):
        hovered  = self.rect.collidepoint(pygame.mouse.get_pos())
        bg_col   = (60, 60, 60) if hovered else (30, 30, 30)
        pygame.draw.rect(surface, bg_col, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE,  self.rect, 2, border_radius=6)
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


def run_menu(screen, clock, level_count: int, dev_mode: bool = False) -> tuple[int, bool]:
    """Block until the player selects a level. Returns (level_index, dev_mode)."""
    font_title  = pygame.font.Font(None, 96)
    font_sub    = pygame.font.Font(None, 38)
    font_button = pygame.font.Font(None, 52)
    font_dev    = pygame.font.Font(None, 30)

    center_x       = SCREEN_WIDTH // 2
    button_width   = 280
    button_height  = 60
    spacing        = 80
    buttons_start_y = SCREEN_HEIGHT // 2
    best_times     = load_best_times(level_count)

    def make_label(i):
        best_time = best_times[i]
        if best_time is not None:
            return f"Level {i + 1}   {format_time(best_time)}"
        return f"Level {i + 1}"

    buttons = [
        Button(center_x, buttons_start_y + i * spacing, button_width, button_height,
               make_label(i), font_button)
        for i in range(level_count)
    ]

    dev_btn_y = buttons_start_y + level_count * spacing + 20
    dev_btn   = Button(center_x, dev_btn_y, 220, 40, "", font_dev)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if dev_btn.is_clicked(event):
                dev_mode = not dev_mode
            for i, btn in enumerate(buttons):
                if btn.is_clicked(event):
                    return i, dev_mode

        screen.fill(BLACK)

        title = font_title.render("Pizza Quest", True, WHITE)
        screen.blit(title, (center_x - title.get_width() // 2, 160))

        sub = font_sub.render("Choose a level", True, (180, 180, 180))
        screen.blit(sub, (center_x - sub.get_width() // 2, buttons_start_y - 50))

        for btn in buttons:
            btn.draw(screen)

        dev_btn.label       = f"DEV MODE: {'ON' if dev_mode else 'OFF'}"
        dev_mode_border_color = (255, 220, 50) if dev_mode else (140, 140, 140)
        pygame.draw.rect(screen, (25, 25, 25),         dev_btn.rect, border_radius=6)
        pygame.draw.rect(screen, dev_mode_border_color, dev_btn.rect, 2, border_radius=6)
        dev_mode_label = font_dev.render(dev_btn.label, True, dev_mode_border_color)
        screen.blit(dev_mode_label, (dev_btn.rect.centerx - dev_mode_label.get_width() // 2,
                                     dev_btn.rect.centery - dev_mode_label.get_height() // 2))

        pygame.display.flip()
