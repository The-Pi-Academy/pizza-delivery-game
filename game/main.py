"""
Pizza Quest: Medieval Delivery
================================
Controls:
  A / D       - Move left / right
  SPACE       - Jump (double jump supported) / Jetpack thrust (when equipped)
  LEFT SHIFT  - Dash
  1           - Equip Sword
  2           - Equip Bow
  ENTER       - Swing sword / Shoot arrow
  E           - Pick up Jetpack / Drop Jetpack
  R           - Restart (when dead) / Next level (when victorious)
  ESC         - Quit
"""

import sys
import pygame

from constants       import SCREEN_W, SCREEN_H, FPS, LEVEL_W, GAS_CAN_FUEL, JETPACK_FUEL_MAX
from player          import Player
from level           import LEVELS
from jetpack         import JetpackItem
from drawing         import (
    draw_background, draw_hud, draw_overlay,
)
from menu            import run_menu
from save            import load_best_times, save_best_times

# Pit-fall world threshold: player.y must exceed this to take pit damage
_PIT_THRESHOLD = 840   # 200 px below ground level (640)


def new_game(level_index: int = 0):
    tilemap, enemies, delivery, jetpack_items, gas_cans = LEVELS[level_index].build()
    player        = Player(120, 594)   # ground y=640, player h=46 → spawn y=594
    arrows        = []
    camera_x      = 0.0
    camera_y      = 0.0
    start_ticks   = pygame.time.get_ticks()
    return tilemap, enemies, player, arrows, delivery, camera_x, camera_y, jetpack_items, gas_cans, start_ticks


def main():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pizza Quest: Medieval Delivery")
    clock = pygame.time.Clock()

    font_big = pygame.font.Font(None, 80)
    font_md  = pygame.font.Font(None, 52)
    font_sm  = pygame.font.Font(None, 24)

    level_index = run_menu(screen, clock, len(LEVELS))
    best_times  = load_best_times(len(LEVELS))
    tilemap, enemies, player, arrows, delivery, camera_x, camera_y, jetpack_items, gas_cans, start_ticks = new_game(level_index)
    level_time  = None   # set on victory
    game_state  = "playing"

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
                        tilemap, enemies, player, arrows, delivery, camera_x, camera_y, jetpack_items, gas_cans, start_ticks = new_game(level_index)
                        level_time = None
                        game_state = "playing"
                    elif game_state == "victory":
                        if level_index >= len(LEVELS) - 1:
                            level_index = run_menu(screen, clock, len(LEVELS))
                        else:
                            level_index += 1
                        tilemap, enemies, player, arrows, delivery, camera_x, camera_y, jetpack_items, gas_cans, start_ticks = new_game(level_index)
                        level_time = None
                        game_state = "playing"
                # Jetpack pickup / drop (E key)
                if game_state == "playing" and event.key == pygame.K_e:
                    if player.has_jetpack:
                        # Drop: spawn item at player's feet
                        player.has_jetpack = False
                        player.jetpack_fuel = 0
                        dropped = JetpackItem(player.x, player.y + player.h - JetpackItem.H)
                        jetpack_items.append(dropped)
                    else:
                        # Try to pick up a nearby jetpack
                        pickup_range = player.rect.inflate(32, 32)
                        for jp in jetpack_items:
                            if jp.active and pickup_range.colliderect(jp.rect):
                                jp.active = False
                                player.has_jetpack = True
                                player.jetpack_fuel = JETPACK_FUEL_MAX
                                break
            if game_state == "playing":
                player.process_event(event, arrows)

        # ---- Render paused / end-screen state without updating -------------
        if game_state != "playing":
            draw_background(screen, camera_x)
            tilemap.draw(screen, camera_x, camera_y)
            delivery.draw(screen, camera_x, camera_y)
            for jp in jetpack_items:
                jp.draw(screen, camera_x, camera_y)
            for gc in gas_cans:
                gc.draw(screen, camera_x, camera_y)
            for e in enemies:
                e.draw(screen, camera_x, camera_y)
            for a in arrows:
                a.draw(screen, camera_x, camera_y)
            player.draw(screen, camera_x, camera_y)
            draw_hud(screen, player, font_sm, timer_seconds=level_time or 0.0)
            draw_overlay(screen, font_big, font_md, font_sm, game_state, level_index, len(LEVELS),
                         level_time=level_time, best_time=best_times[level_index])
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

        # Gas can auto-collect
        pickup_r = player.rect.inflate(8, 8)
        for gc in gas_cans[:]:
            if gc.active and pickup_r.colliderect(gc.rect):
                gc.active = False
                gas_cans.remove(gc)
                if player.has_jetpack:
                    player.jetpack_fuel = min(JETPACK_FUEL_MAX, player.jetpack_fuel + GAS_CAN_FUEL)

        # Camera smooth-follow (player at roughly 1/3 from left)
        target_cam_x = player.x - SCREEN_W // 3
        target_cam_x = max(0, min(target_cam_x, LEVEL_W - SCREEN_W))
        camera_x += (target_cam_x - camera_x) * 0.12

        # Vertical camera — only scroll up (cam_y <= 0), keep ground in view otherwise
        target_cam_y = player.y - SCREEN_H // 2
        target_cam_y = min(target_cam_y, 0)   # never scroll below world y=0
        camera_y += (target_cam_y - camera_y) * 0.12

        # Pit fall — deal damage and respawn slightly back
        if player.y > _PIT_THRESHOLD:
            player.take_damage(Player.PIT_DAMAGE)
            player.x  = max(50, player.x - 150)
            player.y  = 594
            player.vy = 0
            if player.hp <= 0:
                game_state = "dead"

        # Delivery check
        if not delivery.delivered and player.rect.colliderect(delivery.door_rect):
            delivery.delivered = True
            game_state  = "victory"
            level_time  = (pygame.time.get_ticks() - start_ticks) / 1000.0
            if best_times[level_index] is None or level_time < best_times[level_index]:
                best_times[level_index] = level_time
                save_best_times(best_times)

        # ---- Draw ----------------------------------------------------------
        draw_background(screen, camera_x)
        tilemap.draw(screen, camera_x, camera_y)
        delivery.draw(screen, camera_x, camera_y)
        for jp in jetpack_items:
            jp.draw(screen, camera_x, camera_y)
        for gc in gas_cans:
            gc.draw(screen, camera_x, camera_y)
        for e in enemies:
            e.draw(screen, camera_x, camera_y)
        for a in arrows:
            a.draw(screen, camera_x, camera_y)
        player.draw(screen, camera_x, camera_y)
        running_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
        draw_hud(screen, player, font_sm, timer_seconds=running_time)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
