import pygame
from constants import (
    GRAVITY,
    SKIN, GRAY, DK_GRAY, DARK_RED, GREEN, WHITE, DK_BROWN,
)


class Enemy:
    DAMAGE = 20

    def __init__(self, x, y, left_bound=0, right_bound=0, hp=60, stationary=False):
        self.x = float(x)
        self.y = float(y)
        self.w = 32
        self.h = 46
        self.speed_x     = 1.4
        self.speed_y     = 0.0
        self.left_bound  = left_bound
        self.right_bound = right_bound
        self.facing_right = True
        self.stationary  = stationary
        self.hp     = hp
        self.max_hp = hp
        self.active = True
        self.on_ground    = False
        self.atk_cooldown = 0
        self.hit_flash    = 0   # frames remaining to flicker after taking damage
        self.anim_timer   = 0
        self.walk_frame   = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    @property
    def centre(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def update(self, platforms):
        if not self.active:
            return

        if not self.stationary:
            self.x += self.speed_x
            for p in platforms:
                if self.rect.colliderect(p):
                    if self.speed_x > 0:
                        self.x       = p.left - self.w
                        self.speed_x = -abs(self.speed_x)
                        self.facing_right = False
                    elif self.speed_x < 0:
                        self.x       = p.right
                        self.speed_x = abs(self.speed_x)
                        self.facing_right = True
            if self.x <= self.left_bound:
                self.x       = self.left_bound
                self.speed_x = abs(self.speed_x)
                self.facing_right = True
            elif self.x + self.w >= self.right_bound:
                self.x       = self.right_bound - self.w
                self.speed_x = -abs(self.speed_x)
                self.facing_right = False

        self.speed_y = min(self.speed_y + GRAVITY, 20)
        self.y      += self.speed_y
        self.on_ground = False
        for p in platforms:
            r = self.rect
            if r.colliderect(p):
                if self.speed_y >= 0 and r.bottom - self.speed_y <= p.top + 8:
                    self.y       = p.top - self.h
                    self.speed_y = 0
                    self.on_ground = True
                elif self.speed_y < 0:
                    self.y       = p.bottom
                    self.speed_y = 0

        if self.atk_cooldown > 0:
            self.atk_cooldown -= 1
        if self.hit_flash > 0:
            self.hit_flash -= 1

        if not self.stationary:
            self.anim_timer += 1
            if self.anim_timer % 10 == 0:
                self.walk_frame = (self.walk_frame + 1) % 4

    def take_damage(self, dmg):
        self.hp -= dmg
        self.hit_flash = 20
        if self.hp <= 0:
            self.active = False

    def can_attack(self):
        return self.atk_cooldown <= 0

    def do_attack(self):
        self.atk_cooldown = 80

    def draw(self, surface, cam_x, cam_y=0):
        if not self.active:
            return
        if self.hit_flash > 0 and (self.hit_flash // 3) % 2 == 0:
            return
        screen_x = int(self.x - cam_x)
        screen_y = int(self.y - cam_y)
        leg_bob  = [0, 3, 0, -3][self.walk_frame]

        # Legs
        pygame.draw.rect(surface, DK_GRAY, (screen_x + 6,  screen_y + 34, 8, 12 + leg_bob))
        pygame.draw.rect(surface, DK_GRAY, (screen_x + 18, screen_y + 34, 8, 12 - leg_bob))

        # Body (chainmail)
        pygame.draw.rect(surface, DK_GRAY, (screen_x + 4,  screen_y + 16, 24, 20))
        pygame.draw.rect(surface, GRAY,    (screen_x + 6,  screen_y + 18, 20, 16))
        for ring_row_y in range(screen_y + 18, screen_y + 34, 4):
            for ring_col_x in range(screen_x + 6, screen_x + 26, 6):
                pygame.draw.circle(surface, DK_GRAY, (ring_col_x, ring_row_y), 2, 1)

        # Head + helmet
        pygame.draw.ellipse(surface, SKIN,   (screen_x + 8,  screen_y + 3, 16, 14))
        pygame.draw.rect(surface,   DK_GRAY, (screen_x + 5,  screen_y + 1, 22, 10))   # helm bowl
        pygame.draw.rect(surface,   DK_GRAY, (screen_x + 9,  screen_y + 8, 14,  6))   # visor
        pygame.draw.rect(surface,   GRAY,    (screen_x + 11, screen_y + 9, 10,  4))   # visor slit

        # Spear
        spear_x = screen_x + self.w + 2 if self.facing_right else screen_x - 5
        pygame.draw.rect(surface, DK_BROWN, (spear_x, screen_y - 4, 3, 44))
        pygame.draw.polygon(surface, GRAY, [
            (spear_x,     screen_y - 4),
            (spear_x + 3, screen_y - 4),
            (spear_x + 1, screen_y - 14),
        ])

        # HP bar
        health_bar_width = 34
        pygame.draw.rect(surface, DARK_RED, (screen_x - 1, screen_y - 11, health_bar_width, 5))
        pygame.draw.rect(surface, GREEN,    (screen_x - 1, screen_y - 11, int(health_bar_width * max(0, self.hp / self.max_hp)), 5))
        pygame.draw.rect(surface, WHITE,    (screen_x - 1, screen_y - 11, health_bar_width, 5), 1)
