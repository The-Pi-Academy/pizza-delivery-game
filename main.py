"""
Pizza Quest: Medieval Delivery
================================
Controls:
  A / D       - Move left / right
  SPACE       - Jump (double jump supported)
  LEFT SHIFT  - Dash
  1           - Equip Sword
  2           - Equip Bow
  ENTER       - Swing sword / Shoot arrow
  R           - Restart (when dead) / Next level (when victorious)
  ESC         - Quit
"""

import sys
import pygame

from constants       import SCREEN_W, SCREEN_H, FPS, LEVEL_W
from player          import Player
from delivery_target import DeliveryTarget
from level           import LEVELS
from drawing         import (
    draw_background, draw_hud, draw_overlay,
)
from menu            import run_menu


def new_game(level_index: int = 0):
    tilemap, enemies = LEVELS[level_index].build()
    player   = Player(120, 594)          # ground y=640, player h=46 → spawn y=594
    arrows   = []
    delivery = DeliveryTarget(2620, 550) # door bottom aligns with ground y=640
    camera_x = 0.0
    return tilemap, enemies, player, arrows, delivery, camera_x


def main():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pizza Quest: Medieval Delivery")
    clock = pygame.time.Clock()

    font_big = pygame.font.Font(None, 80)
    font_md  = pygame.font.Font(None, 52)
    font_sm  = pygame.font.Font(None, 24)

    run_menu(screen, clock)

    level_index = 0
    tilemap, enemies, player, arrows, delivery, camera_x = new_game(level_index)
    game_state = "playing"

    running = True
    while running:
        clock.tick(FPS)

        # ---- Events --------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    if game_state == "dead":
                        tilemap, enemies, player, arrows, delivery, camera_x = new_game(level_index)
                        game_state = "playing"
                    elif game_state == "victory":
                        level_index = (level_index + 1) % len(LEVELS)
                        tilemap, enemies, player, arrows, delivery, camera_x = new_game(level_index)
                        game_state = "playing"
            if game_state == "playing":
                player.process_event(event, arrows)

        # ---- Render paused / end-screen state without updating -------------
        if game_state != "playing":
            draw_background(screen, camera_x)
            tilemap.draw(screen, camera_x)
            delivery.draw(screen, camera_x)
            for e in enemies:
                e.draw(screen, camera_x)
            for a in arrows:
                a.draw(screen, camera_x)
            player.draw(screen, camera_x)
            draw_hud(screen, player, font_sm)
            draw_overlay(screen, font_big, font_md, font_sm, game_state, level_index, len(LEVELS))
            pygame.display.flip()
            continue

        # ---- Update --------------------------------------------------------
        keys = pygame.key.get_pressed()
        platforms = tilemap.platforms
        player.update(platforms, keys)

        # Arrows
        for a in arrows[:]:
            a.update(platforms)
            if not a.active:
                arrows.remove(a)

        # Enemies + combat resolution
        sword_r = player.sword_rect()
        for e in enemies:
            e.update(platforms)
            if not e.active:
                continue

            # Sword hit (tracked per swing to avoid multi-hit)
            if sword_r and e.rect.colliderect(sword_r):
                if id(e) not in player.sword.hit_set:
                    player.sword.hit_set.add(id(e))
                    e.take_damage(player.sword.DAMAGE)

            # Arrow hit
            for a in arrows[:]:
                if a.active and a.rect.colliderect(e.rect):
                    e.take_damage(a.damage)
                    a.active = False
                    arrows.remove(a)

            # Enemy melee attack on player
            if e.rect.colliderect(player.rect) and e.can_attack():
                if player.take_damage(e.DAMAGE):
                    e.do_attack()
                    if player.hp <= 0:
                        game_state = "dead"

        # Camera smooth-follow (player at roughly 1/3 from left)
        target_cam = player.x - SCREEN_W // 3
        target_cam = max(0, min(target_cam, LEVEL_W - SCREEN_W))
        camera_x  += (target_cam - camera_x) * 0.12

        # Pit fall — deal damage and respawn slightly back
        if player.y > SCREEN_H + 60:
            player.take_damage(Player.PIT_DAMAGE)
            player.x  = max(50, player.x - 150)
            player.y  = 594
            player.vy = 0
            if player.hp <= 0:
                game_state = "dead"

        # Delivery check
        if not delivery.delivered and player.rect.colliderect(delivery.door_rect):
            delivery.delivered = True
            game_state = "victory"

        # ---- Draw ----------------------------------------------------------
        draw_background(screen, camera_x)
        tilemap.draw(screen, camera_x)
        delivery.draw(screen, camera_x)
        for e in enemies:
            e.draw(screen, camera_x)
        for a in arrows:
            a.draw(screen, camera_x)
        player.draw(screen, camera_x)
        draw_hud(screen, player, font_sm)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
