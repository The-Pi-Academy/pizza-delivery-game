from grid            import TileMap
from enemy           import Enemy
from delivery_target import DeliveryTarget
from levels.base     import Level, GROUND_ROW


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

        # first structure to force player to fight enemy
        tilemap.add( 3, 8, 12, 1, S)
        tilemap.add_range(3, 7, 3, 0, S)

        #fist gap
        tilemap.add( 0, GROUND_ROW, 18, 2, G)   # cols  0–35
        tilemap.add( 20, GROUND_ROW, 19, 2, G)   # cols  0–35

        tilemap.add(42, GROUND_ROW, 16, 2, G)   # cols 39–54

        #stairs
        tilemap.add_range(38, 9, 50, 9, S)
        tilemap.add_range(40, 8, 50, 8, S)
        tilemap.add_range(42, 7, 50, 7, S)
        tilemap.add_range(44, 6, 50, 6, S)

        enemies = [
            Enemy(5,  GROUND_ROW, 0, 0, 60),   # guards the first structure
            Enemy(20, GROUND_ROW, 0, 0, 60),   # after the first gap
            Enemy(25, GROUND_ROW, 4, 4),       # patrols after the first gap
            Enemy(30, GROUND_ROW, 9, 5),       # patrols after the first gap
            Enemy(40, 8, 0, 0, 60),            # on the stairs
        ]

        deliveries = [DeliveryTarget(49, 4.5, required_slices=3)]

        return tilemap, enemies, deliveries, [], []
