from grid            import TileMap
from enemy           import Enemy
from delivery_target import DeliveryTarget
from levels.base     import Level, GROUND_ROW


class Level2(Level):
    def build(self) -> tuple[TileMap, list[Enemy], DeliveryTarget]:
        tilemap = TileMap()

        S = "tiles/stone.png"
        G = "tiles/ground.png"

        # draw the first bit of ground
        tilemap.add_range(0, GROUND_ROW, 18, GROUND_ROW, G)

        # first impenetrable wall. Change this code to get past here!
        tilemap.add_range(5, GROUND_ROW, 5, 0, S)

        # second gap, too big to cross. Fix this to make it past!
        tilemap.add_range(26, GROUND_ROW, 60, GROUND_ROW, G)

        # add some stairs before the target
        tilemap.add(26, 9, 1, 1, S)
        tilemap.add(27, 8, 1, 1, S)
        tilemap.add(27, 9, 1, 1, S)

        enemies = [
            Enemy(9,  GROUND_ROW, 5, 6, 60),
            Enemy(12, GROUND_ROW, 2, 2, 60),
            Enemy(16, GROUND_ROW, 1, 2, 60),
            Enemy(18, GROUND_ROW, 1, 2, 60),
        ]

        deliveries = [
            DeliveryTarget(10, GROUND_ROW - 1.5, required_slices=2),
            DeliveryTarget(29, GROUND_ROW - 1.5, required_slices=3),
        ]

        return tilemap, enemies, deliveries, [], []
