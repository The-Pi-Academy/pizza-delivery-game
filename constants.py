import pygame

pygame.init()

# Screen / timing
SCREEN_W = 1280
SCREEN_H  = 720
FPS       = 60
LEVEL_W   = 3500

# Physics
GRAVITY       = 0.78
JUMP_FORCE    = -15.5
MOVE_SPEED    = 5
DASH_SPEED    = 17
DASH_FRAMES   = 13
DASH_COOLDOWN = 52

# Weapon states
WEAPON_NONE  = 0
WEAPON_SWORD = 1
WEAPON_BOW   = 2

# Colours
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (210,  50,  50)
DARK_RED   = (130,  20,  20)
GREEN      = ( 55, 185,  55)
YELLOW     = (255, 215,  50)
ORANGE     = (255, 140,   0)
DK_ORANGE  = (200, 100,   0)
BROWN      = (139,  90,  43)
DK_BROWN   = ( 85,  55,  20)
GRAY       = (160, 160, 160)
DK_GRAY    = ( 75,  75,  75)
LT_GRAY    = (205, 205, 205)
PURPLE     = (110,  55, 165)
LT_PURPLE  = (160, 100, 220)
SKIN       = (255, 205, 155)
SKY        = (125, 195, 230)
STONE      = (162, 158, 148)
DK_STONE   = ( 98,  94,  84)
BLUE       = ( 60, 110, 215)
LT_BLUE    = (160, 190, 235)
CREAM      = (255, 245, 210)
