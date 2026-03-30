import pygame
from enemy import Enemy

GROUND_Y = 620   # top of ground surface


def create_level():
    """Return (platforms, enemies) for level 1."""
    platforms = []
    enemies   = []

    # ---- Flat ground — continuous except for the gap near the end -----------
    platforms.append(pygame.Rect(0,    GROUND_Y, 2350, 80))   # long flat section
    platforms.append(pygame.Rect(2500, GROUND_Y, 1000, 80))   # landing strip (gap is 150 px wide)

    # ---- A handful of patrolling guards spread across the flat section ------
    # (x, spawn_y, patrol_left, patrol_right, hp)
    ground_enemies = [
        ( 600, GROUND_Y - 46,  300, 1000, 60),
        (1300, GROUND_Y - 46,  900, 1700, 60),
        (2000, GROUND_Y - 46, 1500, 2300, 60),
    ]
    for ex, ey, el, er, ehp in ground_enemies:
        enemies.append(Enemy(ex, ey, el, er, ehp))

    return platforms, enemies
