# The Blooming - 2D Point-and-Click Psychological Horror Game

Group 24 - CT029-3-2-Imaging and Special Effects

## Structure

```
blooming/
├── main.py              Entry point - wires all systems together
├── __init__.py          Package init
├── __main__.py          python -m blooming entry
├── utils/               Shared game systems
│   ├── __init__.py      Constants (COLORS, SCREEN dims)
│   ├── utils.py         load_image, render_text, make_font
│   ├── particles.py     ParticleSystem (pollen, spore, glow)
│   ├── screen_shake.py  ScreenShake class
│   ├── sanity.py        SanitySystem
│   ├── inventory.py     Inventory
│   ├── journal.py       Journal
│   └── dialogue.py      DialogueSystem
├── scenes/              Chapter scenes (one per team member)
│   ├── __init__.py
│   ├── scene1_arrival.py     Member A - Arrival & Orientation
│   ├── scene3_greenhouse.py  Member B - Greenhouse Exploration
│   ├── scene4_care.py        Member C - Plant Care & Watering
│   └── scene5_horror.py      Member D - Supernatural & Ending
├── assets/
│   └── images/              Concept art goes here
│       ├── greenhouse/
│       ├── flower/
│       ├── props/
│       ├── char/
│       └── ending/
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- Pygame 2.0+
- Pillow 10.0+

```bash
pip install -r requirements.txt
```

## Run

```bash
cd blooming
python -m blooming
```

## Controls

- **Mouse**: Click hotspots to interact
- **ESC**: Quit
- **J**: Toggle journal

## Team Chapters

| Member | Chapter | Scenes |
|--------|---------|--------|
| A | Arrival & Orientation | Scene1 (exterior), Scene2 (corridor) |
| B | Greenhouse | Scene3 (exploration, X-17 intro, observation) |
| C | Plant Care | Scene4 (watering puzzle, Mara leaves) |
| D | Supernatural | Scene5 (horror sequence, ending) |

## Gameplay Flow

1. **Chapter 1**: Arrive at facility, meet Mara, get access card, enter
2. **Chapter 2**: Explore greenhouse, find watering can, read care sheet, inspect X-17
3. **Chapter 3**: Water X-17 with 500 ml, Mara gets paged to Lab Two, leaves
4. **Chapter 4**: X-17 glows, supernatural whispers, horror response, ending

## Assets Needed

See the asset prompts in the project documentation. Priority order:

1. **HIGH**: Exterior background, corridor background, X-17 flower, Mara sprite
2. **MEDIUM**: Greenhouse interior, watering can, sink, clipboard, care sheet
3. **LOW**: Cabinet, thermometer, journal, sign, intercom, root sprite
