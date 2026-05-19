from grid            import TileMap, to_px
from enemy           import Enemy
from delivery_target import DeliveryTarget
from jetpack         import JetpackItem
from gas_can         import GasCan
from levels.base     import Level, GROUND_ROW, GROUND_Y


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

        ey = lambda row: to_px(row) - 46
        enemies = [
            Enemy(to_px( 7), ey( 7), to_px( 5), to_px(13), 60),   # step 1
            Enemy(to_px( 5), ey( 1), to_px( 4), to_px(13), 60),   # step 3
            Enemy(to_px( 6), ey(-6), to_px( 4), to_px(13), 80),   # step 5
            Enemy(to_px( 6), ey(-13),to_px( 4), to_px(14), 80),   # step 7
        ]

        deliveries = [DeliveryTarget(to_px(18), to_px(-19))]

        jetpack_items = [JetpackItem(to_px(4), GROUND_Y - JetpackItem.H)]

        gc_h = GasCan.H
        gas_cans = [
            GasCan(to_px(9),  GROUND_Y - gc_h),           # ground, before step 1
            GasCan(to_px(5),  to_px( 1) - gc_h),          # step 3
            GasCan(to_px(18), to_px(-10) - gc_h),         # step 6
            GasCan(to_px( 5), to_px(-13) - gc_h),         # step 7
        ]

        return tilemap, enemies, deliveries, jetpack_items, gas_cans
