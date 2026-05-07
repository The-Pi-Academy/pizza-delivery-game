# Pizza Quest: Medieval Delivery

You are a pizza delivery person... in medieval times. Fight your way through
guards, leap across gaps, and get the pizza to the door before it gets cold!

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
