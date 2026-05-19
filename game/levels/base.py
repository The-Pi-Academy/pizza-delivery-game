from grid            import TileMap, to_px
from enemy           import Enemy
from delivery_target import DeliveryTarget

GROUND_ROW = 10
GROUND_Y   = to_px(GROUND_ROW)


class Level:
    def build(self) -> tuple[TileMap, list[Enemy], list[DeliveryTarget], list, list]:
        raise NotImplementedError
