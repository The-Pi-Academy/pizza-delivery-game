import math
import pygame
from constants import SKIN, BROWN, CREAM, RED, WHITE, DK_GRAY
from arrow import Arrow


class Bow:
    ARROW_COOLDOWN = 22
    CHARGE_MAX     = 60  # frames to reach full power (~1 second)

    def __init__(self):
        self.cooldown = 0
        self.charging = False
        self.charge   = 0
        self.angle    = 0  # degrees; 0=horizontal, +90=straight up, -45=down

    def start_charge(self):
        if self.cooldown <= 0:
            self.charging = True
            self.charge   = 0
            self.angle    = 0

    def cancel(self):
        self.charging = False
        self.charge   = 0
        self.angle    = 0

    def release_shot(self, arrows_list, x, y, w, h, facing_right):
        power     = self.charge / self.CHARGE_MAX
        speed     = 5 + power * 11  # 5 at min charge, 16 at full charge
        direction = 1 if facing_right else -1
        rad       = math.radians(self.angle)
        vx        = speed * math.cos(rad) * direction
        vy        = -speed * math.sin(rad)  # negative = upward in pygame
        ox        = w if facing_right else -4
        oy        = h // 2 - 3
        arrows_list.append(Arrow(x + ox, y + oy, direction, vx=vx, vy=vy))
        self.cooldown = self.ARROW_COOLDOWN
        self.charging = False
        self.charge   = 0
        self.angle    = 0

    def update(self, keys):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.charging:
            if keys[pygame.K_w]:
                self.angle = min(90,  self.angle + 2)
            if keys[pygame.K_s]:
                self.angle = max(-45, self.angle - 2)
            self.charge = min(self.charge + 1, self.CHARGE_MAX)

    def draw(self, surface, sx, sy, facing_right):
        if facing_right:
            pygame.draw.rect(surface, SKIN,  (sx + 22, sy + 18, 8, 6))
            pygame.draw.arc(surface,  BROWN, (sx + 28, sy + 10, 10, 22), 0.2, math.pi - 0.2, 3)
            pygame.draw.line(surface, CREAM, (sx + 29, sy + 12), (sx + 29, sy + 30), 1)
        else:
            pygame.draw.rect(surface, SKIN,  (sx,      sy + 18, 8, 6))
            pygame.draw.arc(surface,  BROWN, (sx - 10, sy + 10, 10, 22), 0.2, math.pi - 0.2, 3)
            pygame.draw.line(surface, CREAM, (sx - 2,  sy + 12), (sx - 2,  sy + 30), 1)

    def draw_crosshair(self, surface, sx, sy, w, h, facing_right):
        rad  = math.radians(self.angle)
        dirn = 1 if facing_right else -1
        ch_x = sx + w // 2 + int(75 * math.cos(rad) * dirn)
        ch_y = sy + h // 2 - int(75 * math.sin(rad))
        arm  = 5
        pygame.draw.line(surface, RED, (ch_x - arm, ch_y),       (ch_x + arm, ch_y),       1)
        pygame.draw.line(surface, RED, (ch_x,       ch_y - arm), (ch_x,       ch_y + arm), 1)
        pygame.draw.circle(surface, RED, (ch_x, ch_y), 3, 1)

    def draw_power_bar(self, surface, sx, sy, w):
        bar_w, bar_h = 50, 8
        bar_x = sx + w // 2 - bar_w // 2
        bar_y = sy - 20
        power = self.charge / self.CHARGE_MAX
        fill  = int(bar_w * power)
        r = int(min(255, power * 2 * 255))
        g = int(min(255, (1 - power) * 2 * 255))
        pygame.draw.rect(surface, DK_GRAY,  (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (r, g, 0), (bar_x, bar_y, fill,  bar_h))
        pygame.draw.rect(surface, WHITE,    (bar_x, bar_y, bar_w, bar_h), 1)
