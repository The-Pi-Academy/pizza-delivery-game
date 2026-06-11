from grid            import TileMap, to_px
from enemy           import Enemy
from delivery_target import DeliveryTarget
from levels.base     import Level, GROUND_ROW, GROUND_Y


class Level2(Level):
    def build(self) -> tuple[TileMap, list[Enemy], DeliveryTarget]:
        tilemap = TileMap()

        S = "tiles/stone.png"
        G = "tiles/ground.png"
        enemies = []
        deliveries = []
        ey = GROUND_Y - 46

        # draw the first bit of ground
        tilemap.add_range(0, GROUND_ROW, 20, GROUND_ROW, G)

        # first impenetrable wall. Change this code to get past here!
        tilemap.add_range(5, GROUND_Y, 5, 0, S)

        # add first delivery target
        deliveries.append(DeliveryTarget(to_px(10), to_px(GROUND_ROW - 1.5), required_slices=2))

        # after first wall add some enemies
        enemies.append(Enemy(to_px(9), ey, to_px( 4), to_px(15), 60))
        enemies.append(Enemy(to_px(12), ey, to_px(10), to_px(14), 60))
        enemies.append(Enemy(to_px(16), ey, to_px(15), to_px(18), 60))
        enemies.append(Enemy(to_px(18), ey, to_px(17), to_px(20), 60))

        # second gap, too big to cross. Fix this to make it past!
        tilemap.add_range(26, GROUND_ROW, 60, GROUND_ROW, G)

        # add some stairs before the target
        tilemap.add(26, 9, 1, 1, S)
        tilemap.add(27, 8, 1, 1, S)
        tilemap.add(27, 9, 1, 1, S)
        deliveries.append(DeliveryTarget(to_px(29), to_px(GROUND_ROW - 1.5), required_slices=3))
        return tilemap, enemies, deliveries, [], []
