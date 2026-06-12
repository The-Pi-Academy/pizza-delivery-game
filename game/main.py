"""
Pizza Quest: Medieval Delivery
================================
Controls:
  A / D       - Move left / right
  SPACE       - Jump (double jump supported) / Jetpack thrust (when equipped)
  LEFT SHIFT  - Dash
  1           - Equip Sword
  2           - Equip Pizza Cannon
  ENTER       - Swing breadstick / Launch pizza slice
  E           - Pick up Jetpack / Drop Jetpack
  R           - Restart current level / Next level (when victorious)
  M           - Toggle developer mode (grid overlay)
  ESC         - Quit
"""

import sys
from dataclasses import dataclass, field

import pygame

from constants       import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LEVEL_WIDTH, GAS_CAN_FUEL, JETPACK_FUEL_MAX
from player          import Player
from levels          import LEVELS
from jetpack         import JetpackItem
from drawing         import (
    draw_background, draw_hud, draw_overlay, draw_grid_overlay,
)
from menu            import run_menu
from save            import load_best_times, save_best_times

# Game states
PLAYING = "playing"
DEAD    = "dead"
VICTORY = "victory"

# Player spawn (ground y=640, player h=46 → spawn y=594)
_SPAWN_X, _SPAWN_Y = 120, 594

# Pit-fall world threshold: player.y must exceed this to take pit damage
_PIT_THRESHOLD = 840   # 200 px below ground level (640)


@dataclass
class Fonts:
    """The three font sizes used across the HUD and overlays."""
    big: pygame.font.Font
    md:  pygame.font.Font
    sm:  pygame.font.Font


@dataclass
class World:
    """All mutable state for one level run, bundled so it can be reset in one line."""
    level_index:   int
    tilemap:       object
    enemies:       list
    player:        Player
    deliveries:    list
    jetpack_items: list
    gas_cans:      list
    pizza_slices:  list           = field(default_factory=list)
    camera_x:      float          = 0.0
    camera_y:      float          = 0.0
    start_ticks:   int            = 0
    level_time:    float | None   = None   # set on victory
    state:         str            = PLAYING

    @classmethod
    def load(cls, level_index: int) -> "World":
        tilemap, enemies, deliveries, jetpack_items, gas_cans = LEVELS[level_index].build()
        return cls(
            level_index=level_index,
            tilemap=tilemap,
            enemies=enemies,
            player=Player(_SPAWN_X, _SPAWN_Y),
            deliveries=deliveries,
            jetpack_items=jetpack_items,
            gas_cans=gas_cans,
            start_ticks=pygame.time.get_ticks(),
        )

    def elapsed(self) -> float:
        """Seconds since this level run began."""
        return (pygame.time.get_ticks() - self.start_ticks) / 1000.0


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
def handle_events(world, screen, clock, dev_mode):
    """Drain the event queue. Returns (running, world, dev_mode) — world/dev_mode
    may be replaced when the player restarts or advances a level."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, world, dev_mode
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, world, dev_mode
            if event.key == pygame.K_r:
                world, dev_mode = _restart(world, screen, clock, dev_mode)
                continue
            if event.key == pygame.K_m:
                dev_mode = not dev_mode
            if world.state == PLAYING and event.key == pygame.K_e:
                _toggle_jetpack(world)
        if world.state == PLAYING:
            world.player.process_event(event, world.pizza_slices)
    return True, world, dev_mode


def _restart(world, screen, clock, dev_mode):
    """Handle the R key: retry the current level, or advance after a victory."""
    if world.state in (DEAD, PLAYING):
        return World.load(world.level_index), dev_mode

    # Victory: advance to the next level, or return to the menu after the last one.
    level_index = world.level_index
    if level_index >= len(LEVELS) - 1:
        level_index, dev_mode = run_menu(screen, clock, len(LEVELS), dev_mode)
    else:
        level_index += 1
    return World.load(level_index), dev_mode


def _toggle_jetpack(world):
    """E key: drop an equipped jetpack at the player's feet, or pick up a nearby one."""
    player = world.player
    if player.has_jetpack:
        player.has_jetpack  = False
        player.jetpack_fuel = 0
        world.jetpack_items.append(
            JetpackItem.from_pixels(player.x, player.y + player.h - JetpackItem.H))
    else:
        pickup_range = player.rect.inflate(32, 32)
        for jetpack in world.jetpack_items:
            if jetpack.active and pickup_range.colliderect(jetpack.rect):
                jetpack.active      = False
                player.has_jetpack  = True
                player.jetpack_fuel = JETPACK_FUEL_MAX
                break


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update(world, best_times):
    """Advance the simulation by one frame."""
    keys      = pygame.key.get_pressed()
    platforms = world.tilemap.platforms

    world.player.update(platforms, keys)
    _update_pizza_slices(world, platforms)
    _resolve_combat(world, platforms)
    _resolve_slice_delivery(world)
    for jetpack in world.jetpack_items:
        jetpack.update(platforms)
    _collect_gas_cans(world)
    _update_camera(world)
    _apply_pit_fall(world)
    _check_victory(world, best_times)


def _update_pizza_slices(world, platforms):
    for slice_ in world.pizza_slices[:]:
        slice_.update(platforms)
        if not slice_.active:
            world.pizza_slices.remove(slice_)


def _resolve_combat(world, platforms):
    player       = world.player
    breadstick_r = player.breadstick_rect()
    for enemy in world.enemies:
        enemy.update(platforms)
        if not enemy.active:
            continue

        # Breadstick hit (tracked per swing to avoid multi-hit)
        if breadstick_r and enemy.rect.colliderect(breadstick_r):
            if id(enemy) not in player.breadstick.hit_set:
                player.breadstick.hit_set.add(id(enemy))
                enemy.take_damage(player.breadstick.DAMAGE)

        # Pizza slice hit
        for slice_ in world.pizza_slices[:]:
            if slice_.active and slice_.rect.colliderect(enemy.rect):
                enemy.take_damage(slice_.damage)
                slice_.active = False
                world.pizza_slices.remove(slice_)

        # Enemy melee attack on player
        if enemy.rect.colliderect(player.rect) and enemy.can_attack():
            if player.take_damage(enemy.DAMAGE):
                enemy.do_attack()
                if player.hp <= 0:
                    world.state = DEAD


def _resolve_slice_delivery(world):
    """Pizza slices that strike an unfinished delivery target count toward its order."""
    for slice_ in world.pizza_slices[:]:
        if not slice_.active:
            continue
        for delivery in world.deliveries:
            if not delivery.delivered and slice_.rect.colliderect(delivery.hit_rect):
                delivery.receive_slice()
                slice_.active = False
                world.pizza_slices.remove(slice_)
                break


def _collect_gas_cans(world):
    player   = world.player
    pickup_r = player.rect.inflate(8, 8)
    for gas_can in world.gas_cans[:]:
        if gas_can.active and pickup_r.colliderect(gas_can.rect):
            gas_can.active = False
            world.gas_cans.remove(gas_can)
            if player.has_jetpack:
                player.jetpack_fuel = min(JETPACK_FUEL_MAX, player.jetpack_fuel + GAS_CAN_FUEL)


def _update_camera(world):
    """Smooth-follow the player: ~1/3 from the left, never scrolling below world y=0."""
    target_cam_x = world.player.x - SCREEN_WIDTH // 3
    target_cam_x = max(0, min(target_cam_x, LEVEL_WIDTH - SCREEN_WIDTH))
    world.camera_x += (target_cam_x - world.camera_x) * 0.12

    target_cam_y = min(world.player.y - SCREEN_HEIGHT // 2, 0)
    world.camera_y += (target_cam_y - world.camera_y) * 0.12


def _apply_pit_fall(world):
    """Falling into a pit deals damage and respawns the player slightly back."""
    player = world.player
    if player.y > _PIT_THRESHOLD:
        player.take_damage(Player.PIT_DAMAGE)
        player.x       = max(50, player.x - 150)
        player.y       = _SPAWN_Y
        player.speed_y = 0
        if player.hp <= 0:
            world.state = DEAD


def _check_victory(world, best_times):
    """All orders complete when every delivery target is satisfied."""
    if world.state != PLAYING:
        return
    if world.deliveries and all(d.delivered for d in world.deliveries):
        world.state      = VICTORY
        world.level_time = world.elapsed()
        best = best_times[world.level_index]
        if best is None or world.level_time < best:
            best_times[world.level_index] = world.level_time
            save_best_times(best_times)


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def render(screen, world, fonts, dev_mode, best_times):
    timer = world.elapsed() if world.state == PLAYING else (world.level_time or 0.0)
    _draw_world(screen, world, fonts, dev_mode, timer)
    if world.state != PLAYING:
        draw_overlay(screen, fonts.big, fonts.md, fonts.sm, world.state,
                     world.level_index, len(LEVELS),
                     level_time=world.level_time, best_time=best_times[world.level_index])
    pygame.display.flip()


def _draw_world(screen, world, fonts, dev_mode, timer_seconds):
    cam_x, cam_y = world.camera_x, world.camera_y
    draw_background(screen, cam_x, cam_y)
    world.tilemap.draw(screen, cam_x, cam_y)
    for group in (world.deliveries, world.jetpack_items, world.gas_cans,
                  world.enemies, world.pizza_slices):
        for obj in group:
            obj.draw(screen, cam_x, cam_y)
    world.player.draw(screen, cam_x, cam_y)
    if dev_mode:
        draw_grid_overlay(screen, cam_x, cam_y)
    draw_hud(screen, world.player, fonts.sm, deliveries=world.deliveries,
             timer_seconds=timer_seconds)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Pizza Quest: Medieval Delivery")
    clock = pygame.time.Clock()

    fonts = Fonts(pygame.font.Font(None, 80),
                  pygame.font.Font(None, 52),
                  pygame.font.Font(None, 24))

    level_index, dev_mode = run_menu(screen, clock, len(LEVELS))
    best_times = load_best_times(len(LEVELS))
    world = World.load(level_index)

    running = True
    while running:
        clock.tick(FPS)
        running, world, dev_mode = handle_events(world, screen, clock, dev_mode)
        if world.state == PLAYING:
            update(world, best_times)
        render(screen, world, fonts, dev_mode, best_times)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
