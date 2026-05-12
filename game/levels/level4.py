from grid        import TileMap, to_px
from levels.base import Level, GROUND_ROW


class Level4(Level):
    def build(self):
        tilemap = TileMap()

        tilemap.add(0, GROUND_ROW, 50, 2, "tiles/stone.png")

        return tilemap, [], None, [], []
