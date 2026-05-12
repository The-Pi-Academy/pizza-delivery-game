import math
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, DASH_COOLDOWN, JETPACK_FUEL_MAX,
    WEAPON_SWORD, WEAPON_BOW,
    WHITE, RED, GREEN, YELLOW, ORANGE,
    BROWN, GRAY, DK_GRAY, LT_GRAY, PURPLE, LT_PURPLE,
    DARK_RED, DK_ORANGE,
    SKY, STONE, DK_STONE, LT_BLUE,
)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------
def draw_centered(surface, text, font, colour, center_x, center_y):
    surf = font.render(text, True, colour)
    surface.blit(surf, (center_x - surf.get_width() // 2, center_y - surf.get_height() // 2))


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
def _draw_cloud(surface, center_x, center_y):
    for dx, dy, rw, rh in [
        ( 0, 8, 60, 28),
        (18, 0, 50, 32),
        (40, 6, 50, 26),
    ]:
        pygame.draw.ellipse(surface, WHITE, (center_x + dx, center_y + dy, rw, rh))


def draw_background(surface, cam_x):
    surface.fill(SKY)

    # Clouds (scroll at 0.15× camera speed)
    for base in [80, 280, 520, 760, 1000, 1240, 1480, 1720, 1960]:
        cloud_x = int((base * 1.8 - cam_x * 0.15) % (SCREEN_WIDTH + 200)) - 100
        cloud_y = 40 + (base % 3) * 22
        _draw_cloud(surface, cloud_x, cloud_y)

    # Far background buildings (scroll at 0.2×)
    far_buildings = [
        (0,   310, 85, 310), (90,  280, 65, 340), (165, 260, 105, 360),
        (280, 295, 85, 325), (375, 270, 75, 350), (460, 290,  95, 330),
        (565, 250, 115, 370), (690, 275, 85, 345), (785, 300,  75, 320),
        (870, 265, 100, 355), (980, 285, 80, 335),
    ]
    for building_x, building_y, building_width, building_height in far_buildings:
        screen_x       = int((building_x - cam_x * 0.20) % (SCREEN_WIDTH + 250)) - 120
        building_color = (125, 118, 108)
        pygame.draw.rect(surface, building_color, (screen_x, building_y, building_width, building_height))
        pygame.draw.polygon(surface, (105, 98, 88), [
            (screen_x,                          building_y),
            (screen_x + building_width // 2,    building_y - 28),
            (screen_x + building_width,          building_y),
        ])
        for window_y in range(building_y + 18, building_y + building_height - 18, 38):
            for window_x in range(screen_x + 8, screen_x + building_width - 8, 20):
                pygame.draw.rect(surface, LT_BLUE, (window_x, window_y, 10, 12))

    # Mid background buildings (scroll at 0.45×)
    mid_buildings = [
        (0,   360, 105, 260), (115, 340, 85,  280), (210, 325, 125, 295),
        (345, 350, 95,  270), (450, 320, 115, 300), (575, 345, 105, 275),
        (690, 320, 120, 300), (820, 355, 95,  265),
    ]
    for building_x, building_y, building_width, building_height in mid_buildings:
        screen_x = int((building_x - cam_x * 0.45) % (SCREEN_WIDTH + 250)) - 120
        pygame.draw.rect(surface, STONE,    (screen_x, building_y,      building_width, building_height))
        pygame.draw.rect(surface, DK_STONE, (screen_x, building_y,      building_width, 14))
        for i in range(building_width // 13):
            pygame.draw.rect(surface, DK_STONE, (screen_x + i * 13, building_y - 8, 9, 10))
        for window_y in range(building_y + 18, building_y + building_height - 14, 32):
            for window_x in range(screen_x + 7, screen_x + building_width - 7, 16):
                pygame.draw.rect(surface, (90, 110, 145), (window_x, window_y, 9, 11))


# ---------------------------------------------------------------------------
# Platform
# ---------------------------------------------------------------------------
def draw_platform(surface, plat, cam_x, cam_y=0):
    screen_x = plat.x - cam_x
    screen_y = plat.y - cam_y
    if screen_x + plat.width < -10 or screen_x > SCREEN_WIDTH + 10:
        return
    if screen_y + plat.height < -10 or screen_y > SCREEN_HEIGHT + 10:
        return
    screen_x, screen_y    = int(screen_x), int(screen_y)
    platform_width  = plat.width
    platform_height = plat.height
    pygame.draw.rect(surface, STONE, (screen_x, screen_y, platform_width, platform_height))
    brick_height = 12
    for row in range(platform_height // brick_height + 1):
        brick_offset = 22 if row % 2 else 0
        brick_row_y  = screen_y + row * brick_height
        brick_col_x  = screen_x - (brick_offset % 28)
        while brick_col_x < screen_x + platform_width:
            pygame.draw.rect(surface, DK_STONE, (max(brick_col_x, screen_x), brick_row_y, 26, brick_height - 1), 1)
            brick_col_x += 28
    pygame.draw.rect(surface, (182, 178, 168), (screen_x, screen_y, platform_width, 3))


# ---------------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------------
def draw_hud(surface, player, small_font, timer_seconds=0.0):
    # Health bar
    health_bar_x      = 18
    health_bar_y      = 18
    health_bar_width  = 210
    health_bar_height = 22
    pygame.draw.rect(surface, DARK_RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    health_ratio    = max(0, player.hp / player.max_hp)
    health_bar_color = GREEN if health_ratio > 0.55 else (YELLOW if health_ratio > 0.27 else RED)
    pygame.draw.rect(surface, health_bar_color, (health_bar_x, health_bar_y, int(health_bar_width * health_ratio), health_bar_height))
    pygame.draw.rect(surface, WHITE,  (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
    surface.blit(small_font.render(f"HP  {player.hp} / {player.max_hp}", True, WHITE),
                 (health_bar_x + 6, health_bar_y + 3))

    # Weapon label + attack-ready dot
    if player.weapon == WEAPON_SWORD:
        weapon_text, weapon_color = "SWORD", GRAY
        ready = player.sword.cooldown <= 0
    elif player.weapon == WEAPON_BOW:
        weapon_text, weapon_color = f"BOW    {player.arrows} arrows", BROWN
        ready = player.bow.cooldown <= 0
    else:
        weapon_text, weapon_color = "unarmed   press 1 or 2", LT_GRAY
        ready = True
    weapon_label_surface = small_font.render(weapon_text, True, weapon_color)
    surface.blit(weapon_label_surface, (health_bar_x, health_bar_y + 28))
    pygame.draw.circle(surface, GREEN if ready else RED,
                       (health_bar_x + weapon_label_surface.get_width() + 14, health_bar_y + 37), 5)

    # Dash cooldown bar
    dash_bar_x      = 18
    dash_bar_y      = health_bar_y + 52
    dash_bar_width  = 120
    dash_bar_height = 12
    dash_cooldown_ratio = 1.0 - min(1.0, player.dash_cooldown / DASH_COOLDOWN)
    pygame.draw.rect(surface, DK_GRAY, (dash_bar_x, dash_bar_y, dash_bar_width, dash_bar_height))
    pygame.draw.rect(surface, LT_PURPLE if dash_cooldown_ratio < 1.0 else PURPLE,
                     (dash_bar_x, dash_bar_y, int(dash_bar_width * dash_cooldown_ratio), dash_bar_height))
    pygame.draw.rect(surface, WHITE, (dash_bar_x, dash_bar_y, dash_bar_width, dash_bar_height), 1)
    surface.blit(small_font.render("DASH", True, WHITE), (dash_bar_x + dash_bar_width + 6, dash_bar_y - 1))

    # Jetpack fuel bar (only when equipped)
    if player.has_jetpack:
        fuel_bar_x      = 18
        fuel_bar_y      = dash_bar_y + 38
        fuel_bar_width  = 150
        fuel_bar_height = 12
        fuel_ratio = max(0.0, player.jetpack_fuel / JETPACK_FUEL_MAX)
        pygame.draw.rect(surface, DK_GRAY, (fuel_bar_x, fuel_bar_y, fuel_bar_width, fuel_bar_height))
        fuel_color = ORANGE if fuel_ratio > 0.25 else RED
        pygame.draw.rect(surface, fuel_color, (fuel_bar_x, fuel_bar_y, int(fuel_bar_width * fuel_ratio), fuel_bar_height))
        pygame.draw.rect(surface, WHITE, (fuel_bar_x, fuel_bar_y, fuel_bar_width, fuel_bar_height), 1)
        surface.blit(small_font.render("FUEL  E:drop", True, WHITE), (fuel_bar_x + fuel_bar_width + 6, fuel_bar_y - 1))

    # Timer (top-right)
    from save import format_time
    timer_label_surface = small_font.render(format_time(timer_seconds), True, WHITE)
    surface.blit(timer_label_surface, (SCREEN_WIDTH - timer_label_surface.get_width() - 18, 18))

    # Controls reminder (bottom-left)
    for line_index, hint_line in enumerate([
        "WASD: Move    SPACE: Jump / Jetpack    SHIFT: Dash",
        "1: Sword   2: Bow   ENTER: Attack/Shoot   E: Jetpack",
    ]):
        surface.blit(small_font.render(hint_line, True, (190, 190, 190)),
                     (16, SCREEN_HEIGHT - 46 + line_index * 22))


# ---------------------------------------------------------------------------
# Developer grid overlay
# ---------------------------------------------------------------------------
_dev_font: pygame.font.Font | None = None


def draw_grid_overlay(surface: pygame.Surface, cam_x: float, cam_y: float) -> None:
    from grid import TILE_SIZE

    global _dev_font
    if _dev_font is None:
        _dev_font = pygame.font.Font(None, 16)

    first_col = math.floor(cam_x / TILE_SIZE)
    last_col  = math.floor((cam_x + SCREEN_WIDTH) / TILE_SIZE) + 1
    first_row = math.floor(cam_y / TILE_SIZE)
    last_row  = math.floor((cam_y + SCREEN_HEIGHT) / TILE_SIZE) + 1

    grid_line_color = (180, 180, 0)
    for col in range(first_col, last_col + 1):
        screen_x = int(col * TILE_SIZE - cam_x)
        pygame.draw.line(surface, grid_line_color, (screen_x, 0), (screen_x, SCREEN_HEIGHT))
    for row in range(first_row, last_row + 1):
        screen_y = int(row * TILE_SIZE - cam_y)
        pygame.draw.line(surface, grid_line_color, (0, screen_y), (SCREEN_WIDTH, screen_y))

    for col in range(first_col, last_col):
        for row in range(first_row, last_row):
            screen_x    = int(col * TILE_SIZE - cam_x) + 3
            screen_y    = int(row * TILE_SIZE - cam_y) + 3
            coord_label = _dev_font.render(f"{col},{row}", True, (255, 255, 100), (0, 0, 0))
            surface.blit(coord_label, (screen_x, screen_y))


# ---------------------------------------------------------------------------
# Game-state overlays
# ---------------------------------------------------------------------------
def draw_overlay(surface, large_font, medium_font, small_font, state, level_index=0, level_count=1,
                 level_time=None, best_time=None):
    from save import format_time
    dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dim_overlay.fill((0, 0, 0, 145))
    surface.blit(dim_overlay, (0, 0))
    center_x      = SCREEN_WIDTH // 2
    is_last_level = (level_index >= level_count - 1)
    if state == "dead":
        draw_centered(surface, "PIZZA DROPPED!",            large_font,  RED,    center_x, 240)
        draw_centered(surface, "The pizza is ruined\u2026", medium_font, ORANGE, center_x, 330)
        draw_centered(surface, "Press  R  to try again",    small_font,  WHITE,  center_x, 400)
    elif state == "victory":
        draw_centered(surface, "PIZZA DELIVERED!",              large_font,  YELLOW, center_x, 220)
        draw_centered(surface, "The kingdom feasts tonight!",   medium_font, ORANGE, center_x, 305)
        if level_time is not None:
            is_new_best    = best_time is None or level_time <= best_time
            time_text_color = YELLOW if is_new_best else WHITE
            time_label     = f"Time:  {format_time(level_time)}"
            if is_new_best:
                time_label += "   NEW BEST!"
            draw_centered(surface, time_label, medium_font, time_text_color, center_x, 365)
            if best_time is not None and not is_new_best:
                draw_centered(surface, f"Best:  {format_time(best_time)}", small_font, GRAY, center_x, 405)
        next_prompt_y = 430 if level_time is not None and best_time is not None and level_time > best_time else 410
        if is_last_level:
            draw_centered(surface, "Press  R  to play again from level 1", small_font, WHITE, center_x, next_prompt_y)
        else:
            next_level_number = level_index + 2
            draw_centered(surface, f"Press  R  for level  {next_level_number}", small_font, WHITE, center_x, next_prompt_y)
