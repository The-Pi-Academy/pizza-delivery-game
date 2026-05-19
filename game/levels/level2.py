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
        ey = GROUND_Y - 46

        # draw the first bit of ground
        tilemap.add_range(0, GROUND_ROW, 20, GROUND_ROW, G)

        # first impenetrable wall. Change this code to get past here!
        tilemap.add_range(5, GROUND_Y, 5, 0, S)

        # after first wall add some enemies
        enemies.append(Enemy(to_px(9), ey, to_px( 4), to_px(15), 60))
        enemies.append(Enemy(to_px(12), ey, to_px(10), to_px(14), 60))

        # second gap, too big to cross. Fix this to make it past!
        tilemap.add_range

        delivery = DeliveryTarget(to_px(41), to_px(GROUND_ROW - 2))
        return tilemap, enemies, delivery, [], []
