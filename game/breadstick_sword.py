import pygame
from constants import SKIN


class BreadstickSword:
    DURATION = 18
    COOLDOWN = 28
    DAMAGE   = 38

    _img: pygame.Surface | None = None  # loaded once, shared across instances

    @classmethod
    def _load(cls):
        if cls._img is None:
            cls._img = pygame.image.load("breadstick.png").convert_alpha()

    def __init__(self):
        self._load()
        self.active   = False
        self.timer    = 0
        self.cooldown = 0
        self.hit_set: set = set()

    def try_swing(self):
        if not self.active and self.cooldown <= 0:
            self.active   = True
            self.timer    = self.DURATION
            self.cooldown = self.COOLDOWN
            self.hit_set.clear()

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
                self.hit_set.clear()

    def hitbox(self, x, y, width, facing_right):
        """Returns the breadstick's hit rect, or None when not active."""
        if not self.active:
            return None
        if facing_right:
            return pygame.Rect(int(x + width), int(y + 8), 42, 28)
        else:
            return pygame.Rect(int(x - 42), int(y + 8), 42, 28)

    def draw(self, surface, screen_x, screen_y, facing_right):
        breadstick_image    = self._img
        _, image_height     = breadstick_image.get_size()
        progress            = (1.0 - self.timer / self.DURATION) if self.active else 0.0

        if facing_right:
            angle               = -progress * 180.0
            breadstick_surface  = breadstick_image
            hand_position       = pygame.math.Vector2(screen_x + 28, screen_y + 20)
            pygame.draw.rect(surface, SKIN, (screen_x + 22, screen_y + 18, 8, 6))
        else:
            angle               = progress * 180.0
            breadstick_surface  = pygame.transform.flip(breadstick_image, True, False)
            hand_position       = pygame.math.Vector2(screen_x + 2, screen_y + 20)
            pygame.draw.rect(surface, SKIN, (screen_x, screen_y + 18, 8, 6))

        hilt_to_center      = pygame.math.Vector2(0, -image_height / 2)
        rotated_breadstick  = pygame.transform.rotate(breadstick_surface, angle)
        rotation_center     = hand_position + hilt_to_center.rotate(-angle)
        draw_position       = rotation_center - pygame.math.Vector2(rotated_breadstick.get_size()) / 2
        surface.blit(rotated_breadstick, (int(draw_position.x), int(draw_position.y)))
