import math
import pygame
from constants import (
    GRAVITY, JUMP_FORCE, MOVE_SPEED,
    DASH_SPEED, DASH_FRAMES, DASH_COOLDOWN,
    WEAPON_NONE, WEAPON_SWORD, WEAPON_BOW,
    WHITE, RED, DARK_RED, ORANGE, DK_ORANGE, YELLOW, CREAM,
    DK_BROWN, DK_GRAY, BROWN, GRAY, LT_GRAY, SKIN,
)
from arrow import Arrow


class Player:
    SWORD_DURATION    = 18
    SWORD_COOLDOWN    = 28
    ARROW_COOLDOWN    = 22
    INVINCIBLE_FRAMES = 55

    _sword_img: pygame.Surface | None = None   # loaded once, shared across instances

    @classmethod
    def _load_sword(cls):
        if cls._sword_img is None:
            cls._sword_img = pygame.image.load("sword.png").convert_alpha()

    def __init__(self, x, y):
        self._load_sword()
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

        # Sword
        self.sword_active   = False
        self.sword_timer    = 0
        self.sword_cooldown = 0
        self.sword_hit_set: set = set()

        # Dash
        self.dashing       = False
        self.dash_timer    = 0
        self.dash_dir      = 1
        self.dash_cooldown = 0

        # Bow
        self.arrow_cooldown  = 0
        self.bow_charging    = False
        self.bow_charge      = 0
        self.bow_charge_max  = 60   # frames to reach full power (~1 second)
        self.bow_angle       = 0    # degrees; 0=horizontal, +90=straight up, -45=down

        # Invincibility frames
        self.invincible = 0

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
                self.bow_charging = False
                self.bow_charge   = 0
                self.bow_angle    = 0
                self.weapon = WEAPON_SWORD
            elif k == pygame.K_2:
                self.weapon = WEAPON_BOW
            elif k == pygame.K_RETURN:
                if self.weapon == WEAPON_SWORD:
                    self._try_swing()
                elif self.weapon == WEAPON_BOW and not self.bow_charging:
                    if self.arrow_cooldown <= 0 and self.arrows > 0:
                        self.bow_charging = True
                        self.bow_charge   = 0
                        self.bow_angle    = 0
                        self.vx           = 0.0

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN and self.bow_charging:
                self._release_shot(arrows_list)

    def _try_jump(self):
        if self.jump_count < 2:
            self.vy = JUMP_FORCE * (0.85 if self.jump_count == 1 else 1.0)
            self.jump_count += 1
            self.on_ground = False

    def _try_dash(self):
        if self.dash_cooldown <= 0 and not self.dashing:
            self.dashing       = True
            self.dash_timer    = DASH_FRAMES
            self.dash_dir      = 1 if self.facing_right else -1
            self.dash_cooldown = DASH_COOLDOWN

    def _try_swing(self):
        if not self.sword_active and self.sword_cooldown <= 0:
            self.sword_active   = True
            self.sword_timer    = self.SWORD_DURATION
            self.sword_cooldown = self.SWORD_COOLDOWN
            self.sword_hit_set.clear()

    def _release_shot(self, arrows_list):
        power     = self.bow_charge / self.bow_charge_max
        speed     = 5 + power * 11   # 5 at min charge, 16 at full charge
        direction = 1 if self.facing_right else -1
        rad       = math.radians(self.bow_angle)
        arrow_vx  = speed * math.cos(rad) * direction
        arrow_vy  = -speed * math.sin(rad)   # negative = upward in pygame
        ox        = self.w if self.facing_right else -4
        oy        = self.h // 2 - 3
        arrows_list.append(Arrow(
            self.x + ox, self.y + oy,
            direction,
            vx=arrow_vx,
            vy=arrow_vy,
        ))
        self.arrows        -= 1
        self.arrow_cooldown = self.ARROW_COOLDOWN
        self.bow_charging   = False
        self.bow_charge     = 0
        self.bow_angle      = 0

    # -------------------------------------------------------------------------
    # Per-frame update
    # -------------------------------------------------------------------------
    def update(self, platforms, keys):
        # Horizontal input
        if self.bow_charging:
            self.vx = 0.0
            if keys[pygame.K_w]:
                self.bow_angle = min(90,  self.bow_angle + 2)
            if keys[pygame.K_s]:
                self.bow_angle = max(-45, self.bow_angle - 2)
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
        if self.dash_cooldown  > 0: self.dash_cooldown  -= 1
        if self.sword_cooldown > 0: self.sword_cooldown -= 1
        if self.arrow_cooldown > 0: self.arrow_cooldown -= 1
        if self.invincible     > 0: self.invincible     -= 1

        # Bow charge
        if self.bow_charging:
            self.bow_charge = min(self.bow_charge + 1, self.bow_charge_max)

        if self.sword_active:
            self.sword_timer -= 1
            if self.sword_timer <= 0:
                self.sword_active = False
                self.sword_hit_set.clear()

        # Walk animation
        self.anim_timer += 1
        if self.on_ground and abs(self.vx) > 0.5:
            if self.anim_timer % 7 == 0:
                self.walk_frame = (self.walk_frame + 1) % 4
        else:
            self.walk_frame = 0

    def sword_rect(self):
        if not self.sword_active:
            return None
        if self.facing_right:
            return pygame.Rect(int(self.x + self.w), int(self.y + 8), 42, 28)
        else:
            return pygame.Rect(int(self.x - 42),     int(self.y + 8), 42, 28)

    def take_damage(self, dmg):
        if self.invincible > 0:
            return False
        self.hp = max(0, self.hp - dmg)
        self.invincible = self.INVINCIBLE_FRAMES
        return True

    # -------------------------------------------------------------------------
    # Draw
    # -------------------------------------------------------------------------
    def draw(self, surface, cam_x):
        # Flicker during invincibility
        if self.invincible > 0 and (self.invincible // 4) % 2 == 0:
            return

        sx      = int(self.x - cam_x)
        sy      = int(self.y)
        leg_bob = [0, 4, 0, -4][self.walk_frame] if self.on_ground else 0
        fr      = self.facing_right

        # Power indicator (bow charging)
        if self.bow_charging:
            bar_w, bar_h = 50, 8
            bar_x = sx + self.w // 2 - bar_w // 2
            bar_y = sy - 20
            power = self.bow_charge / self.bow_charge_max
            fill  = int(bar_w * power)
            # Colour shifts green → yellow → red as power increases
            r = int(min(255, power * 2 * 255))
            g = int(min(255, (1 - power) * 2 * 255))
            pygame.draw.rect(surface, DK_GRAY, (bar_x,          bar_y, bar_w, bar_h))
            pygame.draw.rect(surface, (r, g, 0), (bar_x,        bar_y, fill,  bar_h))
            pygame.draw.rect(surface, WHITE,     (bar_x,        bar_y, bar_w, bar_h), 1)

        # Pizza delivery bag (opposite side to facing direction)
        bag_x = sx - 10 if fr else sx + self.w + 2
        pygame.draw.rect(surface, DK_ORANGE, (bag_x,     sy + 14, 12, 20))
        pygame.draw.rect(surface, ORANGE,    (bag_x + 2, sy + 16,  8, 16))
        pygame.draw.circle(surface, YELLOW,  (bag_x + 6, sy + 20),  4)

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
            # Rotation: 0° idle, sweeps 180° clockwise over the attack duration
            progress = (1.0 - self.sword_timer / self.SWORD_DURATION) if self.sword_active else 0.0
            img = self._sword_img
            iw, ih = img.get_size()

            if fr:
                angle    = -progress * 180.0                         # clockwise
                draw_img = img
                hand     = pygame.math.Vector2(sx + 28, sy + 20)
                pygame.draw.rect(surface, SKIN, (sx + 22, sy + 18, 8, 6))  # arm
            else:
                angle    = progress * 180.0                          # mirrored sweep
                draw_img = pygame.transform.flip(img, True, False)
                hand     = pygame.math.Vector2(sx + 2,  sy + 20)
                pygame.draw.rect(surface, SKIN, (sx, sy + 18, 8, 6))       # arm

            # Rotate the sprite around its hilt (assumed at bottom-centre of image)
            hilt_to_centre = pygame.math.Vector2(0, -ih / 2)
            rotated        = pygame.transform.rotate(draw_img, angle)
            rot_centre     = hand + hilt_to_centre.rotate(-angle)
            blit_pos       = rot_centre - pygame.math.Vector2(rotated.get_size()) / 2
            surface.blit(rotated, (int(blit_pos.x), int(blit_pos.y)))
        elif self.weapon == WEAPON_BOW:
            if fr:
                pygame.draw.rect(surface, SKIN,  (sx + 22, sy + 18, 8, 6))
                pygame.draw.arc(surface,  BROWN, (sx + 28, sy + 10, 10, 22), 0.2, math.pi - 0.2, 3)
                pygame.draw.line(surface, CREAM, (sx + 29, sy + 12), (sx + 29, sy + 30), 1)
            else:
                pygame.draw.rect(surface, SKIN,  (sx,      sy + 18, 8, 6))
                pygame.draw.arc(surface,  BROWN, (sx - 10, sy + 10, 10, 22), 0.2, math.pi - 0.2, 3)
                pygame.draw.line(surface, CREAM, (sx - 2,  sy + 12), (sx - 2,  sy + 30), 1)
        else:
            pygame.draw.rect(surface, SKIN, (sx + 22, sy + 18, 8, 8))
            pygame.draw.rect(surface, SKIN, (sx,      sy + 18, 8, 8))

        # Bow crosshair
        if self.weapon == WEAPON_BOW:
            rad  = math.radians(self.bow_angle)
            dirn = 1 if fr else -1
            ch_x = sx + self.w // 2 + int(75 * math.cos(rad) * dirn)
            ch_y = sy + self.h // 2 - int(75 * math.sin(rad))
            arm  = 5
            pygame.draw.line(surface, RED, (ch_x - arm, ch_y),       (ch_x + arm, ch_y),       1)
            pygame.draw.line(surface, RED, (ch_x,       ch_y - arm), (ch_x,       ch_y + arm), 1)
            pygame.draw.circle(surface, RED, (ch_x, ch_y), 3, 1)

        # Dash ghost trail
        if self.dashing:
            ghost = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            ghost.fill((180, 100, 255, 60))
            surface.blit(ghost, (sx - int(self.dash_dir * 20), sy))
