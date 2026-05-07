import sys
import os

# Find the game/ folder relative to this file, no matter where you run from
game_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game")

# Tell Python where to find the game's modules (player.py, level.py, etc.)
sys.path.insert(0, game_dir)

# Step into game/ so tile images and the save file resolve to the right paths
os.chdir(game_dir)

import main
main.main()
