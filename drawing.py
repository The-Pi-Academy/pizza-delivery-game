import pygame
from constants import (
    SCREEN_W, SCREEN_H, DASH_COOLDOWN,
    WEAPON_SWORD, WEAPON_BOW,
    WHITE, RED, GREEN, YELLOW, ORANGE,
    BROWN, GRAY, DK_GRAY, LT_GRAY, PURPLE, LT_PURPLE,
    DARK_RED, DK_ORANGE,
    SKY, STONE, DK_STONE, LT_BLUE,
)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------
def draw_centered(surface, text, font, colour, cx, cy):
    surf = font.render(text, True, colour)
    surface.blit(surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2))


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
def _draw_cloud(surface, cx, cy):
    for dx, dy, rw, rh in [
        ( 0, 8, 60, 28),
        (18, 0, 50, 32),
        (40, 6, 50, 26),
    ]:
        pygame.draw.ellipse(surface, WHITE, (cx + dx, cy + dy, rw, rh))


def draw_background(surface, cam_x):
    surface.fill(SKY)

    # Clouds (scroll at 0.15× camera speed)
    for base in [80, 280, 520, 760, 1000, 1240, 1480, 1720, 1960]:
        cx = int((base * 1.8 - cam_x * 0.15) % (SCREEN_W + 200)) - 100
        cy = 40 + (base % 3) * 22
        _draw_cloud(surface, cx, cy)

    # Far background buildings (scroll at 0.2×)
    far_bldg = [
        (0,   310, 85, 310), (90,  280, 65, 340), (165, 260, 105, 360),
        (280, 295, 85, 325), (375, 270, 75, 350), (460, 290,  95, 330),
        (565, 250, 115, 370), (690, 275, 85, 345), (785, 300,  75, 320),
        (870, 265, 100, 355), (980, 285, 80, 335),
    ]
    for bx, by, bw, bh in far_bldg:
        sx  = int((bx - cam_x * 0.20) % (SCREEN_W + 250)) - 120
        col = (125, 118, 108)
        pygame.draw.rect(surface, col, (sx, by, bw, bh))
        pygame.draw.polygon(surface, (105, 98, 88), [
            (sx,          by),
            (sx + bw // 2, by - 28),
            (sx + bw,     by),
        ])
        for wy in range(by + 18, by + bh - 18, 38):
            for wx in range(sx + 8, sx + bw - 8, 20):
                pygame.draw.rect(surface, LT_BLUE, (wx, wy, 10, 12))

    # Mid background buildings (scroll at 0.45×)
    mid_bldg = [
        (0,   360, 105, 260), (115, 340, 85,  280), (210, 325, 125, 295),
        (345, 350, 95,  270), (450, 320, 115, 300), (575, 345, 105, 275),
        (690, 320, 120, 300), (820, 355, 95,  265),
    ]
    for bx, by, bw, bh in mid_bldg:
        sx = int((bx - cam_x * 0.45) % (SCREEN_W + 250)) - 120
        pygame.draw.rect(surface, STONE,    (sx, by,      bw, bh))
        pygame.draw.rect(surface, DK_STONE, (sx, by,      bw, 14))
        for i in range(bw // 13):
            pygame.draw.rect(surface, DK_STONE, (sx + i * 13, by - 8, 9, 10))
        for wy in range(by + 18, by + bh - 14, 32):
            for wx in range(sx + 7, sx + bw - 7, 16):
                pygame.draw.rect(surface, (90, 110, 145), (wx, wy, 9, 11))


# ---------------------------------------------------------------------------
# Platform
# ---------------------------------------------------------------------------
def draw_platform(surface, plat, cam_x):
    px = plat.x - cam_x
    if px + plat.width < -10 or px > SCREEN_W + 10:
        return
    sx, sy, pw, ph = int(px), int(plat.y), plat.width, plat.height
    pygame.draw.rect(surface, STONE, (sx, sy, pw, ph))
    brick_h = 12
    for row in range(ph // brick_h + 1):
        offset = 22 if row % 2 else 0
        ry     = sy + row * brick_h
        col_x  = sx - (offset % 28)
        while col_x < sx + pw:
            pygame.draw.rect(surface, DK_STONE, (max(col_x, sx), ry, 26, brick_h - 1), 1)
            col_x += 28
    pygame.draw.rect(surface, (182, 178, 168), (sx, sy, pw, 3))


# ---------------------------------------------------------------------------
# HUD
# ---------------------------------------------------------------------------
def draw_hud(surface, player, font_sm):
    # Health bar
    bar_x, bar_y, bar_w, bar_h = 18, 18, 210, 22
    pygame.draw.rect(surface, DARK_RED, (bar_x, bar_y, bar_w, bar_h))
    ratio = max(0, player.hp / player.max_hp)
    hp_col = GREEN if ratio > 0.55 else (YELLOW if ratio > 0.27 else RED)
    pygame.draw.rect(surface, hp_col, (bar_x, bar_y, int(bar_w * ratio), bar_h))
    pygame.draw.rect(surface, WHITE,  (bar_x, bar_y, bar_w, bar_h), 2)
    surface.blit(font_sm.render(f"HP  {player.hp} / {player.max_hp}", True, WHITE),
                 (bar_x + 6, bar_y + 3))

    # Weapon label + attack-ready dot
    if player.weapon == WEAPON_SWORD:
        w_txt, w_col = "SWORD", GRAY
        ready = player.sword_cooldown <= 0
    elif player.weapon == WEAPON_BOW:
        w_txt, w_col = f"BOW    {player.arrows} arrows", BROWN
        ready = player.arrow_cooldown <= 0
    else:
        w_txt, w_col = "unarmed   press 1 or 2", LT_GRAY
        ready = True
    wsurf = font_sm.render(w_txt, True, w_col)
    surface.blit(wsurf, (bar_x, bar_y + 28))
    pygame.draw.circle(surface, GREEN if ready else RED,
                       (bar_x + wsurf.get_width() + 14, bar_y + 37), 5)

    # Dash cooldown bar
    d_x, d_y, d_w, d_h = 18, bar_y + 52, 120, 12
    cd_ratio = 1.0 - min(1.0, player.dash_cooldown / DASH_COOLDOWN)
    pygame.draw.rect(surface, DK_GRAY, (d_x, d_y, d_w, d_h))
    pygame.draw.rect(surface, LT_PURPLE if cd_ratio < 1.0 else PURPLE,
                     (d_x, d_y, int(d_w * cd_ratio), d_h))
    pygame.draw.rect(surface, WHITE, (d_x, d_y, d_w, d_h), 1)
    surface.blit(font_sm.render("DASH", True, WHITE), (d_x + d_w + 6, d_y - 1))

    # Double-jump charge pips
    for i in range(2):
        col = YELLOW if i < (2 - player.jump_count) else DK_GRAY
        pygame.draw.rect(surface, col,   (d_x + i * 20, d_y + 18, 14, 14))
        pygame.draw.rect(surface, WHITE, (d_x + i * 20, d_y + 18, 14, 14), 1)
    surface.blit(font_sm.render("JUMPS", True, WHITE), (d_x + 44, d_y + 18))

    # Controls reminder (bottom-left)
    for i, ln in enumerate([
        "WASD: Move    SPACE: Jump (×2)    SHIFT: Dash",
        "1: Sword   2: Bow   ENTER: Attack/Shoot",
    ]):
        surface.blit(font_sm.render(ln, True, (190, 190, 190)),
                     (16, SCREEN_H - 46 + i * 22))


# ---------------------------------------------------------------------------
# Game-state overlays
# ---------------------------------------------------------------------------
def draw_overlay(surface, font_big, font_md, font_sm, state):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 145))
    surface.blit(overlay, (0, 0))
    cx = SCREEN_W // 2
    if state == "dead":
        draw_centered(surface, "PIZZA DROPPED!",         font_big, RED,    cx, 240)
        draw_centered(surface, "The pizza is ruined\u2026", font_md,  ORANGE, cx, 330)
        draw_centered(surface, "Press  R  to try again", font_sm,  WHITE,  cx, 400)
    elif state == "victory":
        draw_centered(surface, "PIZZA DELIVERED!",              font_big, YELLOW, cx, 240)
        draw_centered(surface, "The kingdom feasts tonight!",   font_md,  ORANGE, cx, 330)
        draw_centered(surface, "Press  R  to deliver again",    font_sm,  WHITE,  cx, 400)
