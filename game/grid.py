"""
Grid system — 64 × 64 pixel tiles.

Usage in level definitions
--------------------------
    from grid import TileMap

    tilemap = TileMap()
    tilemap.add(0, 10, 36, 2, "tiles/ground.png")   # 36 wide, 2 tall, at grid (0, 10)

Tile PNG files live in the game root (or a sub-folder).
If the file is missing the tile falls back to the brick-stone primitive renderer.
"""

import os
import pygame

TILE_SIZE: int = 64

# ---------------------------------------------------------------------------
# Image cache — loaded lazily on first draw, None means "file not found"
# ---------------------------------------------------------------------------
_image_cache: dict[str, pygame.Surface | None] = {}


def _load_tile_image(filename: str) -> pygame.Surface | None:
    if filename in _image_cache:
        return _image_cache[filename]
    if os.path.isfile(filename):
        raw = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(raw, (TILE_SIZE, TILE_SIZE))
        _image_cache[filename] = img
        return img
    _image_cache[filename] = None
    return None


# ---------------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------------
def tile_rect(gx: int, gy: int, gw: int = 1, gh: int = 1) -> pygame.Rect:
    """Convert grid coordinates to a pixel-space pygame.Rect.

    Parameters
    ----------
    gx, gy : int   Grid column / row of the top-left corner.
    gw, gh : int   Width and height in grid cells (default 1).
    """
    return pygame.Rect(gx * TILE_SIZE, gy * TILE_SIZE, gw * TILE_SIZE, gh * TILE_SIZE)


def to_px(grid_units: int) -> int:
    """Convert a distance in grid units to pixels."""
    return grid_units * TILE_SIZE


# ---------------------------------------------------------------------------
# Tile & TileMap
# ---------------------------------------------------------------------------
class Tile:
    """A rectangular block defined in grid space, optionally textured."""
    __slots__ = ("rect", "image")

    def __init__(self, rect: pygame.Rect, image: str) -> None:
        self.rect  = rect
        self.image = image  # PNG filename relative to the game root


class TileMap:
    """Collection of Tile objects that handles both collision and rendering."""

    def __init__(self) -> None:
        self._tiles: list[Tile] = []

    # ------------------------------------------------------------------
    # Building the map
    # ------------------------------------------------------------------
    def add(self, gx: int, gy: int, gw: int, gh: int, image: str) -> None:
        """Add a tile block at grid position (gx, gy) spanning gw × gh cells.

        Parameters
        ----------
        gx, gy    : int   Grid column / row of the top-left corner.
        gw, gh    : int   Size in grid cells.
        image     : str   PNG filename (e.g. "tiles/stone.png").
                          Falls back to the brick primitive if the file is missing.
        """
        self._tiles.append(Tile(tile_rect(gx, gy, gw, gh), image))

    # ------------------------------------------------------------------
    # Physics interface
    # ------------------------------------------------------------------
    @property
    def platforms(self) -> list[pygame.Rect]:
        """Pixel-space collision rects — pass to player.update / enemy.update."""
        return [t.rect for t in self._tiles]

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface, cam_x: float, cam_y: float = 0) -> None:
        from drawing import draw_platform   # late import — avoids circular dependency
        sw = surface.get_width()
        sh = surface.get_height()
        for tile in self._tiles:
            px = tile.rect.x - cam_x
            py = tile.rect.y - cam_y
            if px + tile.rect.width < -10 or px > sw + 10:
                continue
            if py + tile.rect.height < -10 or py > sh + 10:
                continue
            img = _load_tile_image(tile.image)
            if img is not None:
                _blit_tiled(surface, img, tile.rect, cam_x, cam_y)
            else:
                draw_platform(surface, tile.rect, cam_x, cam_y)


def _blit_tiled(surface: pygame.Surface, img: pygame.Surface,
                rect: pygame.Rect, cam_x: float, cam_y: float = 0) -> None:
    """Tile *img* (TILE_SIZE × TILE_SIZE) across *rect*, offset by camera."""
    sx = int(rect.x - cam_x)
    sy = int(rect.y - cam_y)
    pw, ph = rect.width, rect.height
    for row in range(0, ph, TILE_SIZE):
        for col in range(0, pw, TILE_SIZE):
            clip_w = min(TILE_SIZE, pw - col)
            clip_h = min(TILE_SIZE, ph - row)
            dest   = (sx + col, sy + row)
            if clip_w == TILE_SIZE and clip_h == TILE_SIZE:
                surface.blit(img, dest)
            else:
                surface.blit(img, dest, (0, 0, clip_w, clip_h))
