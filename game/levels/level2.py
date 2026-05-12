from grid            import TileMap, to_px
from enemy           import Enemy
from delivery_target import DeliveryTarget
from levels.base     import Level, GROUND_ROW, GROUND_Y


class Level2(Level):
    """Level 2 — identical to level 1 for now; edit freely."""

    def build(self) -> tuple[TileMap, list[Enemy], DeliveryTarget]:
        tilemap = TileMap()

        S = "tiles/stone.png"
        tilemap.add( 36, 1, 1, 10, S)

        tilemap.add(0, GROUND_ROW, 100, 2, "tiles/ground.png")   # cols 39–54

        ey = GROUND_Y - 46
        enemies = [
            Enemy(to_px( 9), ey, to_px( 4), to_px(15), 60),
            Enemy(to_px(20), ey, to_px(14), to_px(26), 60),
            Enemy(to_px(31), ey, to_px(23), to_px(35), 60),
        ]
        delivery = DeliveryTarget(to_px(41), to_px(GROUND_ROW - 2))
        return tilemap, enemies, delivery, [], []
