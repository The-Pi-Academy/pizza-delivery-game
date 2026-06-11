import math
import pygame
from constants import SKIN, GRAY, DK_GRAY, ORANGE, RED, WHITE
from pizza_slice import PizzaSlice


class PizzaCannon:
    SLICE_COOLDOWN = 22
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

    def release_shot(self, pizza_slices_list, x, y, w, h, facing_right):
        charge_ratio  = self.charge / self.CHARGE_MAX
        speed         = 5 + charge_ratio * 11  # 5 at min charge, 16 at full charge
        direction     = 1 if facing_right else -1
        angle_radians = math.radians(self.angle)
        speed_x       = speed * math.cos(angle_radians) * direction
        speed_y       = -speed * math.sin(angle_radians)  # negative = upward in pygame
        offset_x      = w if facing_right else -4
        offset_y      = h // 2 - 3
        pizza_slices_list.append(PizzaSlice(x + offset_x, y + offset_y, direction, speed_x=speed_x, speed_y=speed_y))
        self.cooldown = self.SLICE_COOLDOWN
        self.charging = False
        self.charge   = 0
        self.angle    = 0

    def update(self, keys):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.charging:
            if keys[pygame.K_w]:
                self.angle = min(45,  self.angle + 2)
            if keys[pygame.K_s]:
                self.angle = max(-45, self.angle - 2)
            self.charge = min(self.charge + 1, self.CHARGE_MAX)

    def draw(self, surface, screen_x, screen_y, facing_right):
        if facing_right:
            # Arm holding grip
            pygame.draw.rect(surface, SKIN,   (screen_x + 22, screen_y + 18, 8, 6))
            # Cannon chamber
            pygame.draw.rect(surface, DK_GRAY, (screen_x + 26, screen_y + 14, 14, 14))
            # Barrel
            pygame.draw.rect(surface, GRAY,   (screen_x + 40, screen_y + 18, 14, 6))
            # Muzzle ring
            pygame.draw.circle(surface, DK_GRAY, (screen_x + 54, screen_y + 21), 4, 2)
            # Pizza logo dot on chamber
            pygame.draw.circle(surface, ORANGE, (screen_x + 33, screen_y + 21), 3)
        else:
            # Arm holding grip
            pygame.draw.rect(surface, SKIN,   (screen_x,      screen_y + 18, 8, 6))
            # Cannon chamber
            pygame.draw.rect(surface, DK_GRAY, (screen_x - 10, screen_y + 14, 14, 14))
            # Barrel
            pygame.draw.rect(surface, GRAY,   (screen_x - 24, screen_y + 18, 14, 6))
            # Muzzle ring
            pygame.draw.circle(surface, DK_GRAY, (screen_x - 24, screen_y + 21), 4, 2)
            # Pizza logo dot on chamber
            pygame.draw.circle(surface, ORANGE, (screen_x - 3, screen_y + 21), 3)

    def draw_crosshair(self, surface, screen_x, screen_y, player_width, player_height, facing_right):
        angle_radians = math.radians(self.angle)
        direction     = 1 if facing_right else -1
        crosshair_x   = screen_x + player_width  // 2 + int(75 * math.cos(angle_radians) * direction)
        crosshair_y   = screen_y + player_height // 2 - int(75 * math.sin(angle_radians))
        arm_length    = 5
        pygame.draw.line(surface, RED, (crosshair_x - arm_length, crosshair_y), (crosshair_x + arm_length, crosshair_y), 1)
        pygame.draw.line(surface, RED, (crosshair_x, crosshair_y - arm_length), (crosshair_x, crosshair_y + arm_length), 1)
        pygame.draw.circle(surface, RED, (crosshair_x, crosshair_y), 3, 1)

    def draw_power_bar(self, surface, screen_x, screen_y, player_width):
        bar_width    = 50
        bar_height   = 8
        bar_left     = screen_x + player_width // 2 - bar_width // 2
        bar_top      = screen_y - 20
        charge_ratio = self.charge / self.CHARGE_MAX
        fill_width   = int(bar_width * charge_ratio)
        red_amount   = int(min(255, charge_ratio * 2 * 255))
        green_amount = int(min(255, (1 - charge_ratio) * 2 * 255))
        pygame.draw.rect(surface, DK_GRAY,                       (bar_left, bar_top, bar_width,  bar_height))
        pygame.draw.rect(surface, (red_amount, green_amount, 0), (bar_left, bar_top, fill_width, bar_height))
        pygame.draw.rect(surface, WHITE,                         (bar_left, bar_top, bar_width,  bar_height), 1)
