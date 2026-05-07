import pygame
from constants import (
    GRAVITY, JUMP_FORCE, MOVE_SPEED,
    DASH_SPEED, DASH_FRAMES, DASH_COOLDOWN,
    WEAPON_NONE, WEAPON_SWORD, WEAPON_BOW,
    JETPACK_THRUST, JETPACK_FUEL_MAX,
    WHITE, RED, DARK_RED, ORANGE, DK_ORANGE, YELLOW, CREAM,
    DK_BROWN, DK_GRAY, BROWN, GRAY, LT_GRAY, SKIN,
)
from sword import Sword
from bow import Bow


class Player:
    INVINCIBLE_FRAMES = 55
    PIT_DAMAGE        = 25

    def __init__(self, x, y):
        self.x  = float(x)
        self.y  = float(y)
        self.w  = 30
        self.h  = 46
        self.vx = 0.0
        self.vy = 0.0

        self.on_ground    = False
        self.facing_right = True
        self.jump_count   = 0

        self.hp     = 100
        self.max_hp = 100

        self.weapon = WEAPON_SWORD
        self.arrows = 25

        self.sword = Sword()
        self.bow   = Bow()

        # Dash
        self.dashing       = False
        self.dash_timer    = 0
        self.dash_dir      = 1
        self.dash_cooldown = 0

        # Invincibility frames
        self.invincible = 0

        # Jetpack
        self.has_jetpack       = False
        self.jetpack_fuel      = 0
        self.jetpack_thrusting = False

        # Animation
        self.anim_timer = 0
        self.walk_frame = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    @property
    def centre(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    # -------------------------------------------------------------------------
    # Input
    # -------------------------------------------------------------------------
    def process_event(self, event, arrows_list):
        """Call once per pygame event."""
        if event.type == pygame.KEYDOWN:
            k = event.key
            if k == pygame.K_SPACE:
                self._try_jump()
            elif k in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                self._try_dash()
            elif k == pygame.K_1:
                self.bow.cancel()
                self.weapon = WEAPON_SWORD
            elif k == pygame.K_2:
                self.weapon = WEAPON_BOW
            elif k == pygame.K_RETURN:
                if self.weapon == WEAPON_SWORD:
                    self.sword.try_swing()
                elif self.weapon == WEAPON_BOW and not self.bow.charging:
                    if self.bow.cooldown <= 0 and self.arrows > 0:
                        self.bow.start_charge()
                        self.vx = 0.0

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN and self.bow.charging:
                self.bow.release_shot(
                    arrows_list, self.x, self.y, self.w, self.h, self.facing_right
                )
                self.arrows -= 1

    def _try_jump(self):
        if self.jump_count < 1:
            self.vy = JUMP_FORCE
            self.jump_count += 1
            self.on_ground = False

    def _try_dash(self):
        if self.dash_cooldown <= 0 and not self.dashing:
            self.dashing       = True
            self.dash_timer    = DASH_FRAMES
            self.dash_dir      = 1 if self.facing_right else -1
            self.dash_cooldown = DASH_COOLDOWN

    # -------------------------------------------------------------------------
    # Per-frame update
    # -------------------------------------------------------------------------
    def update(self, platforms, keys):
        # Horizontal input
        if self.bow.charging:
            self.vx = 0.0
        elif not self.dashing:
            if keys[pygame.K_a]:
                self.vx = -MOVE_SPEED
                self.facing_right = False
            elif keys[pygame.K_d]:
                self.vx = MOVE_SPEED
                self.facing_right = True
            else:
                self.vx *= 0.75
                if abs(self.vx) < 0.4:
                    self.vx = 0.0

        # Dash movement
        if self.dashing:
            self.vx          = DASH_SPEED * self.dash_dir
            self.vy          = max(self.vy, 0)
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False

        # Gravity
        if not self.dashing:
            self.vy = min(self.vy + GRAVITY, 22)

        # Jetpack thrust (SPACE held, overrides gravity effect)
        self.jetpack_thrusting = False
        if self.has_jetpack and self.jetpack_fuel > 0 and keys[pygame.K_SPACE]:
            self.vy = max(self.vy - JETPACK_THRUST, -16.0)
            self.jetpack_fuel -= 1
            self.jetpack_thrusting = True

        # Move X + clamp to level left edge
        self.x += self.vx
        if self.x < 0:
            self.x, self.vx = 0.0, 0.0

        # Platform collision X
        for p in platforms:
            r = self.rect
            if r.colliderect(p):
                if self.vx > 0:
                    self.x  = p.left - self.w
                    self.vx = 0.0
                elif self.vx < 0:
                    self.x  = p.right
                    self.vx = 0.0

        # Move Y
        self.y += self.vy

        # Platform collision Y
        self.on_ground = False
        for p in platforms:
            r = self.rect
            if r.colliderect(p):
                if self.vy >= 0 and r.bottom - self.vy <= p.top + 10:
                    self.y         = p.top - self.h
                    self.vy        = 0.0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.vy < 0:
                    self.y  = p.bottom
                    self.vy = 0.0

        # Cooldowns
        if self.dash_cooldown > 0: self.dash_cooldown -= 1
        if self.invincible     > 0: self.invincible     -= 1

        self.sword.update()
        self.bow.update(keys)

        # Walk animation
        self.anim_timer += 1
        if self.on_ground and abs(self.vx) > 0.5:
            if self.anim_timer % 7 == 0:
                self.walk_frame = (self.walk_frame + 1) % 4
        else:
            self.walk_frame = 0

    def sword_rect(self):
        return self.sword.hitbox(self.x, self.y, self.w, self.facing_right)

    def take_damage(self, dmg):
        if self.invincible > 0:
            return False
        self.hp = max(0, self.hp - dmg)
        self.invincible = self.INVINCIBLE_FRAMES
        return True

    # -------------------------------------------------------------------------
    # Draw
    # -------------------------------------------------------------------------
    def draw(self, surface, cam_x, cam_y=0):
        # Flicker during invincibility
        if self.invincible > 0 and (self.invincible // 4) % 2 == 0:
            return

        sx      = int(self.x - cam_x)
        sy      = int(self.y - cam_y)
        leg_bob = [0, 4, 0, -4][self.walk_frame] if self.on_ground else 0
        fr      = self.facing_right

        # Power indicator (bow charging)
        if self.bow.charging:
            self.bow.draw_power_bar(surface, sx, sy, self.w)

        # Pizza delivery bag (opposite side to facing direction)
        bag_x = sx - 10 if fr else sx + self.w + 2
        pygame.draw.rect(surface, DK_ORANGE, (bag_x,     sy + 14, 12, 20))
        pygame.draw.rect(surface, ORANGE,    (bag_x + 2, sy + 16,  8, 16))
        pygame.draw.circle(surface, YELLOW,  (bag_x + 6, sy + 20),  4)

        # Jetpack tanks on back (drawn before body so body overlaps straps)
        if self.has_jetpack:
            jp_x = sx - 6 if fr else sx + self.w - 2
            pygame.draw.rect(surface, DK_GRAY, (jp_x, sy + 14, 8, 22))
            pygame.draw.rect(surface, GRAY,    (jp_x + 1, sy + 15, 6, 20))
            pygame.draw.rect(surface, (50, 50, 50), (jp_x + 1, sy + 33, 6, 4))
            if self.jetpack_thrusting:
                pygame.draw.ellipse(surface, ORANGE, (jp_x,     sy + 36, 8, 10))
                pygame.draw.ellipse(surface, YELLOW, (jp_x + 2, sy + 38, 4,  6))

        # Legs + boots
        pygame.draw.rect(surface, DK_BROWN,     (sx + 5,  sy + 34,  9, 12 + leg_bob))
        pygame.draw.rect(surface, DK_BROWN,     (sx + 16, sy + 34,  9, 12 - leg_bob))
        pygame.draw.rect(surface, (50, 35, 15), (sx + 4,  sy + 44 + leg_bob, 11, 5))
        pygame.draw.rect(surface, (50, 35, 15), (sx + 15, sy + 44 - leg_bob, 11, 5))

        # Body
        pygame.draw.rect(surface, RED,      (sx + 4,  sy + 16, 22, 20))
        pygame.draw.rect(surface, DARK_RED, (sx + 4,  sy + 16,  3, 20))
        pygame.draw.rect(surface, DARK_RED, (sx + 23, sy + 16,  3, 20))

        # Head
        pygame.draw.ellipse(surface, SKIN, (sx + 7, sy + 3, 16, 14))

        # Delivery cap
        pygame.draw.rect(surface,   DARK_RED, (sx + 5,  sy + 3, 20, 6))
        pygame.draw.rect(surface,   DARK_RED, (sx + 3,  sy + 5, 24, 4))
        pygame.draw.circle(surface, CREAM,    (sx + 22, sy + 3),  3)

        # Arms + weapon
        if self.weapon == WEAPON_SWORD:
            self.sword.draw(surface, sx, sy, fr)
        elif self.weapon == WEAPON_BOW:
            self.bow.draw(surface, sx, sy, fr)
            self.bow.draw_crosshair(surface, sx, sy, self.w, self.h, fr)
        else:
            pygame.draw.rect(surface, SKIN, (sx + 22, sy + 18, 8, 8))
            pygame.draw.rect(surface, SKIN, (sx,      sy + 18, 8, 8))

        # Dash ghost trail
        if self.dashing:
            ghost = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            ghost.fill((180, 100, 255, 60))
            surface.blit(ghost, (sx - int(self.dash_dir * 20), sy))
