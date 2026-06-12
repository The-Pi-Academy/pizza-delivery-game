import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK
from save import load_best_times, format_time


# Key / description pairs shown on the controls screen.
CONTROLS = [
    ("A / D",      "Move left / right"),
    ("SPACE",      "Jump (double jump) / Jetpack thrust"),
    ("LEFT SHIFT", "Dash"),
    ("1",          "Equip Sword"),
    ("2",          "Equip Pizza Cannon"),
    ("ENTER",      "Swing breadstick / Launch pizza slice"),
    ("E",          "Pick up / Drop Jetpack"),
    ("R",          "Restart level / Next level (on victory)"),
    ("M",          "Toggle developer mode (grid overlay)"),
    ("ESC",        "Quit"),
]


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


def _run_controls_screen(screen, clock):
    """Show the list of controls until the player closes it (X button or ESC)."""
    font_title = pygame.font.Font(None, 72)
    font_key   = pygame.font.Font(None, 34)
    font_desc  = pygame.font.Font(None, 30)
    font_x     = pygame.font.Font(None, 40)

    close_btn = Button(SCREEN_WIDTH - 44, 44, 48, 48, "X", font_x)

    key_x  = SCREEN_WIDTH // 2 - 300
    desc_x = SCREEN_WIDTH // 2 - 80
    list_y = 200
    row_h  = 44

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if close_btn.is_clicked(event):
                return

        screen.fill(BLACK)

        title = font_title.render("Controls", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 90))

        for row, (key, desc) in enumerate(CONTROLS):
            y = list_y + row * row_h
            screen.blit(font_key.render(key, True, (255, 220, 50)), (key_x, y))
            screen.blit(font_desc.render(desc, True, WHITE),        (desc_x, y))

        close_btn.draw(screen)

        pygame.display.flip()


def run_menu(screen, clock, level_count: int, dev_mode: bool = False) -> tuple[int, bool]:
    """Block until the player selects a level. Returns (level_index, dev_mode)."""
    font_title  = pygame.font.Font(None, 96)
    font_sub    = pygame.font.Font(None, 38)
    font_button = pygame.font.Font(None, 52)

    center_x        = SCREEN_WIDTH // 2
    button_width    = 280
    button_height   = 60
    spacing         = 80
    buttons_start_y = SCREEN_HEIGHT // 2
    best_times      = load_best_times(level_count)

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

    controls_btn_y = buttons_start_y + level_count * spacing + 20
    controls_btn   = Button(center_x, controls_btn_y, 220, 40, "Controls", font_sub)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if controls_btn.is_clicked(event):
                _run_controls_screen(screen, clock)
                break
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

        controls_btn.draw(screen)

        pygame.display.flip()
