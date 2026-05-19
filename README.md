# Pizza Quest: Medieval Delivery

You are a pizza delivery person... in medieval times. Fight your way through
guards, leap across gaps, and get the pizza to the door before it gets cold!

The intention of this game is to teach campers the fundamentals of game development
 with little to no programming experience. 
 
 # Levels 
 There are three levels total, with an empty fourth level provided for anyone who wants to take a crack at making their own level from scratch.

 ## Level 1
 Basic level that teaches the player basic contols, weapons, enemies, etc. Can be completed with no edits.

 ## Level 2
 On its own the level cannot be completed, players are immediately blocked by a giant wall
 and must determine how they can get around the wall. The ideal way they solve this blocker is by removing or changing the wall in `levels/level2.py`. There is a comment locating the line of code adding thish wall.
 

 # Things to Go Over With Campers
 1. The file system - Show them how to open the game files, explain important files such as 
 run.py, reset.py, the levels directory, etc.

 2. The game loop - 



---

## What you need

- A Raspberry Pi 4 or 5 (or any Mac/Linux computer)
- Python 3 (already installed on Raspberry Pi OS)
- That's it — the setup script handles the rest

---

## Getting started

Open a terminal and go to the project folder, then run:

```bash
bash setup.sh
```

This sets everything up for you. It's safe to run more than once.

When it finishes, it will tell you exactly what to type next.

---

## Launching the game

```bash
source venv/bin/activate
python run.py
```

Or if you prefer to work inside the game folder:

```bash
source venv/bin/activate
cd game
python main.py
```

A window will pop up. Choose a level and start delivering!

---

## Controls

| Key | What it does |
|-----|--------------|
| A / D | Walk left / right |
| SPACE | Jump |
| LEFT SHIFT | Dash (quick burst of speed) |
| 1 | Hold sword |
| 2 | Hold bow |
| ENTER | Swing sword — or charge up and release an arrow |
| E | Pick up or put down the jetpack |
| R | Try again after dying / move to next level after winning |
| ESC | Quit |

---

## The levels

**Level 1** — Guards patrol the ground between you and the delivery door.
Get past them to make the drop.

**Level 2** — Something is in your way. Figure out how to get through.

**Level 3** — Sky High Delivery. The door is way up in the clouds. Find the
jetpack near the start and hunt for gas cans on the platforms to keep it
fuelled.

The game remembers your best time on each level and shows it on the menu.

---

## Troubleshooting

**"No module named pygame"**
Make sure you ran `bash setup.sh` and then activated the environment:
```bash
source venv/bin/activate
```

**The window doesn't open / black screen**
Make sure you are inside the `game/` folder when you run `python main.py`.

**Something else is broken**
Read the error message carefully — it usually tells you exactly which file
and line number to look at. That's where to start!
