Blooming - A 2D Point-and-Click Psychological Horror Game
==========================================================

Group 24 - CT029-3-2-Imaging and Special Effects

A flora-themed psychological horror game developed using Pygame.

## Features

- 2D point-and-click gameplay mechanics
- Inventory system for item collection and usage
- Journal system for narrative tracking
- Sanity system with hallucination effects
- Particle effects system for special effects
- Dialogue system with branching choices
- Screen shake effects for horror sequences

## Game Structure

The game follows the screenplay and consists of 5 scenes:

1. **Arrival** - Player arrives at Blackwood Research Facility
2. **Orientation** - Facility tour with Dr. Mara Vale
3. **Greenhouse** - Player explores greenhouse and cares for X-17
4. **Blooming** - Horror sequence with the flower's true nature revealed
5. **Ending** - The conclusion of Day 1

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python -m blooming
```

or

```bash
python blooming/main.py
```

## Controls

- Mouse - Click to interact with hotspots
- I - Toggle inventory
- J - Toggle journal
- ESC - Quit game

## Technical Details

- **Engine**: Pygame 2.0+
- **Language**: Python 3.7+
- **File Format**: Single module architecture

## Special Effects Implemented

1. **Particle Systems**
   - Pollen floating particles
   - Spore explosion effects
   - Glow pulsation effects

2. **Visual Effects**
   - Screen shake/distortion
   - Sanity meter with color changes
   - Hallucination overlay effects

3. **Audio Effects** (simulated through visual cues)
   - Whispers (text-based)
   - Sound cues (indicated in dialogue)

## Gameplay Mechanics

1. **Point-and-Click Navigation**
   - Hotspot detection system
   - Click-based interaction

2. **Inventory System**
   - Item collection (access card, watering can)
   - Item usage on hotspots
   - Selected item tracking

3. **Journal System**
   - Unlockable entries
   - Story progression tracking

4. **Sanity System**
   - Progressive sanity loss
   - Hallucination effects
   - Horror sequence triggers

5. **Dialogue System**
   - Text-based conversations
   - Branching choices
   - Callback-based interactions

## Project Structure

```
pro/
├── blooming/
│   ├── __init__.py
│   ├── __main__.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Group Members

- Chin Jun Lin (TP078844)
- Lee Chen Hong (TP134345)
- Cheah Han Liang (TP086650)
- Shao Xiaoyi

## License

This project is developed for educational purposes as part of 
CT029-3-2-Imaging and Special Effects coursework.
