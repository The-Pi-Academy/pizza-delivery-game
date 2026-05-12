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
        raw_image    = pygame.image.load(filename).convert_alpha()
        scaled_image = pygame.transform.scale(raw_image, (TILE_SIZE, TILE_SIZE))
        _image_cache[filename] = scaled_image
        return scaled_image
    _image_cache[filename] = None
    return None


# ---------------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------------
def tile_rect(grid_x: int, grid_y: int, grid_width: int = 1, grid_height: int = 1) -> pygame.Rect:
    """Convert grid coordinates to a pixel-space pygame.Rect.

    Parameters
    ----------
    grid_x, grid_y     : int   Grid column / row of the top-left corner.
    grid_width, grid_height : int   Width and height in grid cells (default 1).
    """
    return pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, grid_width * TILE_SIZE, grid_height * TILE_SIZE)


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
    def add(self, grid_x: int, grid_y: int, grid_width: int, grid_height: int, image: str) -> None:
        """Add a tile block at grid position (grid_x, grid_y) spanning grid_width × grid_height cells.

        Parameters
        ----------
        grid_x, grid_y         : int   Grid column / row of the top-left corner.
        grid_width, grid_height : int   Size in grid cells.
        image                  : str   PNG filename (e.g. "tiles/stone.png").
                                       Falls back to the brick primitive if the file is missing.
        """
        self._tiles.append(Tile(tile_rect(grid_x, grid_y, grid_width, grid_height), image))

    def add_range(self, x1: int, y1: int, x2: int, y2: int, image: str) -> None:
        """Add a tile block spanning from grid cell (x1, y1) to (x2, y2) inclusive.

        Coordinates can be given in any order — top-to-bottom or bottom-to-top,
        left-to-right or right-to-left.

        Parameters
        ----------
        x1, y1 : int   One corner in grid columns / rows.
        x2, y2 : int   The opposite corner (inclusive).
        image   : str   PNG filename (e.g. "tiles/stone.png").
        """
        left = min(x1, x2)
        top  = min(y1, y2)
        self.add(left, top, abs(x2 - x1) + 1, abs(y2 - y1) + 1, image)

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
        surface_width  = surface.get_width()
        surface_height = surface.get_height()
        for tile in self._tiles:
            pixel_x = tile.rect.x - cam_x
            pixel_y = tile.rect.y - cam_y
            if pixel_x + tile.rect.width < -10 or pixel_x > surface_width + 10:
                continue
            if pixel_y + tile.rect.height < -10 or pixel_y > surface_height + 10:
                continue
            tile_image = _load_tile_image(tile.image)
            if tile_image is not None:
                _blit_tiled(surface, tile_image, tile.rect, cam_x, cam_y)
            else:
                draw_platform(surface, tile.rect, cam_x, cam_y)


def _blit_tiled(surface: pygame.Surface, tile_image: pygame.Surface,
                rect: pygame.Rect, cam_x: float, cam_y: float = 0) -> None:
    """Tile *tile_image* (TILE_SIZE × TILE_SIZE) across *rect*, offset by camera."""
    screen_x    = int(rect.x - cam_x)
    screen_y    = int(rect.y - cam_y)
    tile_width  = rect.width
    tile_height = rect.height
    for y_offset in range(0, tile_height, TILE_SIZE):
        for x_offset in range(0, tile_width, TILE_SIZE):
            clip_width  = min(TILE_SIZE, tile_width  - x_offset)
            clip_height = min(TILE_SIZE, tile_height - y_offset)
            draw_position = (screen_x + x_offset, screen_y + y_offset)
            if clip_width == TILE_SIZE and clip_height == TILE_SIZE:
                surface.blit(tile_image, draw_position)
            else:
                surface.blit(tile_image, draw_position, (0, 0, clip_width, clip_height))
