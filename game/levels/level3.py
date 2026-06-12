from grid            import TileMap
from enemy           import Enemy
from delivery_target import DeliveryTarget
from jetpack         import JetpackItem
from gas_can         import GasCan
from levels.base     import Level, GROUND_ROW


class Level3(Level):
    """Level 3 — Sky High Delivery.

    The delivery target is far above the ground. A jetpack is provided at the
    start. Gas cans scattered on platforms refuel it. Several platform gaps
    require jetpack thrust to cross.

    Platform layout (S = stone, row 0 = y=0, negative rows go upward):
      row  10: GGGGGGGGGGGGGGGG...  (wide ground)
      row   7: SSSSSSSS             (step 1 — double-jump gap)
      row   4:          SSSSSSSS    (step 2)
      row   1: SSSSSSSSS            (step 3 — gas can)
      row  -2:           SSSSSSSS   (step 4)
      row  -6: SSSSSSSSS            (step 5 — 4-row gap, jetpack helpful)
      row -10:           SSSSSSSS   (step 6 — 4-row gap, jetpack needed)
      row -13: SSSSSSSSSS           (step 7 — gas can)
      row -17:            SSSSSSS   (step 8 — 4-row gap, jetpack needed)
      row -20: [DeliveryTarget]
    """

    def build(self):
        tilemap = TileMap()
        S = "tiles/stone.png"
        G = "tiles/ground.png"

        tilemap.add( 0, GROUND_ROW, 50,  2, G)   # wide ground

        tilemap.add( 5,  7,  8, 1, S)   # step 1
        tilemap.add(16,  4,  8, 1, S)   # step 2
        tilemap.add( 4,  1,  9, 1, S)   # step 3
        tilemap.add(17, -2,  8, 1, S)   # step 4
        tilemap.add( 4, -6,  9, 1, S)   # step 5  (4-row gap from step 4)
        tilemap.add(17,-10,  8, 1, S)   # step 6  (4-row gap from step 5)
        tilemap.add( 4,-13, 10, 1, S)   # step 7
        tilemap.add(17,-17,  7, 1, S)   # step 8  (4-row gap from step 7)
        tilemap.add(26, 0, 3, 1, S)

        enemies = [
            Enemy( 7,  7,  2, 6, 60),   # step 1
            Enemy( 5,  1,  1, 8, 60),   # step 3
            Enemy( 6, -6,  2, 7, 80),   # step 5
            Enemy( 6, -13, 2, 8, 80),   # step 7
            Enemy( 6, -13, 2, 8, 80),   # step 7
            Enemy( 22, -3, 0, 0, 80),
        ]

        deliveries = [DeliveryTarget(18, -19, 2), DeliveryTarget(24, -3, 4), DeliveryTarget(27, 0, 3)]

        jetpack_items = [JetpackItem(4, GROUND_ROW)]

        gas_cans = [
            GasCan(9, GROUND_ROW),           # ground, before step 1
            # ADD MORE GAS CANS HERE
        ]

        return tilemap, enemies, deliveries, jetpack_items, gas_cans
