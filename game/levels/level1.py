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
        G = "tiles/ground.png"
        enemies = []
        ey = GROUND_Y - 46
        # first structure to force player to fight enemy
        tilemap.add( 3, 8, 12, 1, S)
        tilemap.add_range(3, 7, 3, 0, S)
        enemies.append(Enemy(to_px(5), ey, 0, 0, 60, True))

        #fist gap
        tilemap.add( 0, GROUND_ROW, 18, 2, G)   # cols  0–35
        tilemap.add( 20, GROUND_ROW, 19, 2, G)   # cols  0–35

        # enemies after first gap
        enemies.append(Enemy(to_px(20), ey, 0, 0, 60, True))
        enemies.append(Enemy(to_px(25), ey, to_px(21), to_px(29)))
        enemies.append(Enemy(to_px(30), ey, to_px(21), to_px(35)))

        tilemap.add(42, GROUND_ROW, 16, 2, G)   # cols 39–54

        #stairs
        tilemap.add_range(38, 9, 50, 9, S)
        tilemap.add_range(40, 8, 50, 8, S)
        enemies.append(Enemy(to_px(40), 8, 0, 0, 60, True))
        tilemap.add_range(42, 7, 50, 7, S)
        tilemap.add_range(44, 6, 50, 6, S)

        deliveries = [DeliveryTarget(to_px(49), to_px(4.5), required_slices=3)]
        return tilemap, enemies, deliveries, [], []
