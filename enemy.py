import pygame
from constants import (
    GRAVITY,
    SKIN, GRAY, DK_GRAY, DARK_RED, GREEN, WHITE, DK_BROWN,
)


class Enemy:
    DAMAGE = 18

    def __init__(self, x, y, left_bound, right_bound, hp=60):
        self.x = float(x)
        self.y = float(y)
        self.w = 32
        self.h = 46
        self.vx          = 1.4
        self.vy          = 0.0
        self.left_bound  = left_bound
        self.right_bound = right_bound
        self.facing_right = True
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

        self.x += self.vx
        if self.x <= self.left_bound:
            self.x = self.left_bound
            self.vx = abs(self.vx)
            self.facing_right = True
        elif self.x + self.w >= self.right_bound:
            self.x = self.right_bound - self.w
            self.vx = -abs(self.vx)
            self.facing_right = False

        self.vy = min(self.vy + GRAVITY, 20)
        self.y += self.vy
        self.on_ground = False
        for p in platforms:
            r = self.rect
            if r.colliderect(p):
                if self.vy >= 0 and r.bottom - self.vy <= p.top + 8:
                    self.y = p.top - self.h
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = p.bottom
                    self.vy = 0

        if self.atk_cooldown > 0:
            self.atk_cooldown -= 1
        if self.hit_flash > 0:
            self.hit_flash -= 1

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
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        leg_bob = [0, 3, 0, -3][self.walk_frame]

        # Legs
        pygame.draw.rect(surface, DK_GRAY, (sx + 6,  sy + 34, 8, 12 + leg_bob))
        pygame.draw.rect(surface, DK_GRAY, (sx + 18, sy + 34, 8, 12 - leg_bob))

        # Body (chainmail)
        pygame.draw.rect(surface, DK_GRAY, (sx + 4,  sy + 16, 24, 20))
        pygame.draw.rect(surface, GRAY,    (sx + 6,  sy + 18, 20, 16))
        for ry in range(sy + 18, sy + 34, 4):
            for rx in range(sx + 6, sx + 26, 6):
                pygame.draw.circle(surface, DK_GRAY, (rx, ry), 2, 1)

        # Head + helmet
        pygame.draw.ellipse(surface, SKIN,   (sx + 8,  sy + 3, 16, 14))
        pygame.draw.rect(surface,   DK_GRAY, (sx + 5,  sy + 1, 22, 10))   # helm bowl
        pygame.draw.rect(surface,   DK_GRAY, (sx + 9,  sy + 8, 14,  6))   # visor
        pygame.draw.rect(surface,   GRAY,    (sx + 11, sy + 9, 10,  4))   # visor slit

        # Spear
        spear_x = sx + self.w + 2 if self.facing_right else sx - 5
        pygame.draw.rect(surface, DK_BROWN, (spear_x, sy - 4, 3, 44))
        pygame.draw.polygon(surface, GRAY, [
            (spear_x,     sy - 4),
            (spear_x + 3, sy - 4),
            (spear_x + 1, sy - 14),
        ])

        # HP bar
        bw = 34
        pygame.draw.rect(surface, DARK_RED, (sx - 1, sy - 11, bw, 5))
        pygame.draw.rect(surface, GREEN,    (sx - 1, sy - 11, int(bw * max(0, self.hp / self.max_hp)), 5))
        pygame.draw.rect(surface, WHITE,    (sx - 1, sy - 11, bw, 5), 1)
