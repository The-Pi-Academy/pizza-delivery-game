import pygame
from constants import SCREEN_W, SCREEN_H, FPS, WHITE, BLACK
from save import load_best_times, format_time


class Button:
    def __init__(self, cx, cy, w, h, label, font):
        self.rect  = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
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

    cx         = SCREEN_W // 2
    btn_w      = 280
    btn_h      = 60
    spacing    = 80
    start_y    = SCREEN_H // 2
    best_times = load_best_times(level_count)

    def make_label(i):
        bt = best_times[i]
        if bt is not None:
            return f"Level {i + 1}   {format_time(bt)}"
        return f"Level {i + 1}"

    buttons = [
        Button(cx, start_y + i * spacing, btn_w, btn_h,
               make_label(i), font_button)
        for i in range(level_count)
    ]

    dev_btn_y  = start_y + level_count * spacing + 20
    dev_btn    = Button(cx, dev_btn_y, 220, 40, "", font_dev)

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
        screen.blit(title, (cx - title.get_width() // 2, 160))

        sub = font_sub.render("Choose a level", True, (180, 180, 180))
        screen.blit(sub, (cx - sub.get_width() // 2, start_y - 50))

        for btn in buttons:
            btn.draw(screen)

        dev_btn.label = f"DEV MODE: {'ON' if dev_mode else 'OFF'}"
        dev_on_col    = (255, 220, 50) if dev_mode else (140, 140, 140)
        pygame.draw.rect(screen, (25, 25, 25), dev_btn.rect, border_radius=6)
        pygame.draw.rect(screen, dev_on_col,   dev_btn.rect, 2, border_radius=6)
        lbl = font_dev.render(dev_btn.label, True, dev_on_col)
        screen.blit(lbl, (dev_btn.rect.centerx - lbl.get_width() // 2,
                          dev_btn.rect.centery - lbl.get_height() // 2))

        pygame.display.flip()
