import pygame
from constants import SKIN


class Sword:
    DURATION = 18
    COOLDOWN = 28
    DAMAGE   = 38

    _img: pygame.Surface | None = None  # loaded once, shared across instances

    @classmethod
    def _load(cls):
        if cls._img is None:
            cls._img = pygame.image.load("sword.png").convert_alpha()

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

    def hitbox(self, x, y, w, facing_right):
        """Returns the sword's hit rect, or None when not active."""
        if not self.active:
            return None
        if facing_right:
            return pygame.Rect(int(x + w), int(y + 8), 42, 28)
        else:
            return pygame.Rect(int(x - 42), int(y + 8), 42, 28)

    def draw(self, surface, sx, sy, facing_right):
        img      = self._img
        _iw, ih  = img.get_size()
        progress = (1.0 - self.timer / self.DURATION) if self.active else 0.0

        if facing_right:
            angle    = -progress * 180.0
            draw_img = img
            hand     = pygame.math.Vector2(sx + 28, sy + 20)
            pygame.draw.rect(surface, SKIN, (sx + 22, sy + 18, 8, 6))
        else:
            angle    = progress * 180.0
            draw_img = pygame.transform.flip(img, True, False)
            hand     = pygame.math.Vector2(sx + 2, sy + 20)
            pygame.draw.rect(surface, SKIN, (sx, sy + 18, 8, 6))

        hilt_to_centre = pygame.math.Vector2(0, -ih / 2)
        rotated        = pygame.transform.rotate(draw_img, angle)
        rot_centre     = hand + hilt_to_centre.rotate(-angle)
        blit_pos       = rot_centre - pygame.math.Vector2(rotated.get_size()) / 2
        surface.blit(rotated, (int(blit_pos.x), int(blit_pos.y)))
