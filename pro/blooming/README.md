# The Blooming - 2D Point-and-Click Psychological Horror Game

A complete Python/Pygame implementation of the psychological horror game based on the screenplay.

## Requirements

- Python 3.8+
- Pygame 2.0+

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

```bash
cd blooming
python main.py
```

Or:

```bash
python -m blooming
```

## Controls

- **Mouse**: Click hotspots to interact with objects, characters, and hotspots
- **ESC**: Quit the game
- **I**: Toggle inventory (visible by default at bottom)
- **J**: Toggle journal (shows objectives and notes)

## Gameplay Features

- **Point-and-click navigation**: Explore environments by clicking hotspots
- **Inventory system**: Collect and use items (access card, watering can)
- **Dialogue system**: Interact with characters and make choices
- **Observation mode**: Inspect specimens for clues
- **Puzzle solving**: Fill watering can with correct amount, use access card
- **Sanity meter**: Monitor sanity level during horror sequences
- **Particle effects**: Pollen, glow, and spore effects
- **Screen shake**: Distortion effects during horror sequences
- **Journal**: Track objectives and notes

## Scenes

1. **Scene 1 - Arrival**: Arrive at facility, interact with Mara, get access card, enter
2. **Scene 2 - Orientation**: Facility tour, follow Mara to greenhouse
3. **Scene 3 - Greenhouse**: Explore, find watering can, inspect X-17, water with 500ml
4. **Scene 4 - Blooming**: Supernatural event, X-17 glows, whispers, horror sequences
5. **Scene 5 - Ending**: The Blooming conclusion

## Hotspots

### Scene 1 (Arrival)
- Facility sign
- Security intercom  
- Security door
- Security panel (for access card)
- Dr. Mara Vale

### Scene 2 (Orientation)
- Restricted Laboratory door
- Staff Office door
- Storage door
- Greenhouse door
- Dr. Mara Vale

### Scene 3 (Greenhouse)
- Watering can
- Filtered water sink
- Care instruction clipboard
- Greenhouse thermometer
- Storage cabinet
- Old research journal
- Specimen X-17
- Dr. Mara Vale

## Game Flow

1. Talk to Mara to receive access card
2. Select access card and use on security panel to enter
3. Follow Mara through facility to greenhouse
4. Take watering can and fill with 500ml filtered water
5. Read care instructions
6. Water X-17 with 500ml
7. Experience supernatural events as X-17 glows and whispers
8. Make horror response choices
9. End of Day 1
