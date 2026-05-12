from grid            import TileMap, to_px
from enemy           import Enemy
from delivery_target import DeliveryTarget
from levels.base     import Level, GROUND_ROW, GROUND_Y


class Level1(Level):
    """Level 1.

    Rough layout (S = stone platform, G = ground):
      row  8:   SSS      SS
      row  7:        SS
      row 10: GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   GGGGGGGGGGGGGGGG
      row 11: GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   GGGGGGGGGGGGGGGG
    """

    def build(self) -> tuple[TileMap, list[Enemy], DeliveryTarget]:
        tilemap = TileMap()

        S = "tiles/stone.png"
        tilemap.add( 3, 8, 3, 1, S)
        tilemap.add( 9, 7, 2, 1, S)
        tilemap.add(13, 8, 2, 1, S)

        tilemap.add( 0, GROUND_ROW, 36, 2, "tiles/ground.png")   # cols  0–35
        tilemap.add(39, GROUND_ROW, 16, 2, "tiles/ground.png")   # cols 39–54

        ey = GROUND_Y - 46
        enemies = [
            Enemy(to_px( 9), ey, to_px( 4), to_px(15), 60),
            Enemy(to_px(20), ey, to_px(14), to_px(26), 60),
            Enemy(to_px(31), ey, to_px(23), to_px(35), 60),
        ]
        delivery = DeliveryTarget(to_px(41), to_px(GROUND_ROW - 2))
        return tilemap, enemies, delivery, [], []
