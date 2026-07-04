# The Blooming - Implementation Summary

## Created Files

### `/mnt/wwn-0x5000c5007c9be4ca-part1/evan-zhenfeng-li/apu/level-2/semester-2/imaging-and-special-effects/blooming/pro/blooming/main.py`
Complete game implementation with all features.

### `/mnt/wwn-0x5000c5007c9be4ca-part1/evan-zhenfeng-li/apu/level-2/semester-2/imaging-and-special-effects/blooming/pro/blooming/requirements.txt`
Pygame dependency file.

### `/mnt/wwn-0x5000c5007c9be4ca-part1/evan-zhenfeng-li/apu/level-2/semester-2/imaging-and-special-effects/blooming/pro/blooming/__init__.py`
Package initialization.

### `/mnt/wwn-0x5000c5007c9be4ca-part1/evan-zhenfeng-li/apu/level-2/semester-2/imaging-and-special-effects/blooming/pro/blooming/__main__.py`
Module entry point.

### `/mnt/wwn-0x5000c5007c9be4ca-part1/evan-zhenfeng-li/apu/level-2/semester-2/imaging-and-special-effects/blooming/pro/blooming/README.md`
Documentation and usage instructions.

## Features Implemented

### 1. Core Game Systems
- **Point-and-click navigation**: Interactive hotspots throughout all scenes
- **Inventory system**: Access card, watering can with fill levels
- **Dialogue system**: Multiple choice branches with callbacks
- **Journal system**: Track objectives and notes
- **Sanity meter**: Visual indicator with hallucination effects
- **Particle systems**: Pollen, spore, and glow effects
- **Screen shake**: Distortion effects during horror sequences

### 2. Scene Implementation (Exact from screenplay)

#### Scene 1 - Arrival at Facility
- Facility sign (inspection)
- Security intercom (optional interaction)
- Security door with lock state
- Security panel for access card
- Dr. Mara Vale interaction
- Access card acquisition and usage flow
- Branch: Wrong action (click door without card)
- Correct action (select card, use on panel)

#### Scene 2 - Facility Orientation
- Restricted Laboratory door
- Staff Office door
- Storage door
- Greenhouse door
- Mara tour and rule setting
- Greenhouse entrance

#### Scene 3 - Greenhouse Exploration
- Watering can (pickup)
- Filtered water sink
- Care instruction clipboard (500ml requirement)
- Greenhouse thermometer
- Storage cabinet
- Old research journal
- Specimen X-17 (inspection tutorial)
- Watering X-17 with correct amount

#### Scene 4 - First Meeting with X-17
- Three dialogue choices:
  - "It looks dangerous."
  - "It's beautiful."
  - "It looks unusual."
- Observation mode with three inspection points
- Soil dryness dialogue choice (correct: "Water it.")
- Watering can selection and usage
- 500ml quantity selection (250ml and 750ml wrong, 500ml correct)
- X-17 watering

#### Scene 5 - Supernatural Event
- X-17 glow effect
- Whispers through intercom
- Three horror response branches:
  - Call Mara (Intercom)
  - Try to leave (Escape)
  - Approach flower (Flower)
- Screen distortion
- Sanity decrease
- Exit scene with knocking sound

## Hotspots

### Scene 1 (Arrival)
- Facility sign → Inspection text
- Intercom → "Security intercom is active"
- Door → "The door is locked"
- Door panel → Access card interaction
- Mara → Access card interaction with choice

### Scene 2 (Orientation)
- Restricted Laboratory → "Need higher clearance"
- Staff Office → Visible but no interaction
- Storage → Visible but no interaction
- Greenhouse door → Mara interaction, then entrance
- Mara → "Before we go inside, one rule"

### Scene 3 (Greenhouse)
- Watering can → Pickup and fill
- Sink → "Filtered water system"
- Clipboard → Full care instructions display
- Thermometer → "24 degrees Celsius"
- Cabinet → "Contains general supplies"
- Journal → "Better not touch it"
- X-17 → Inspection tutorial, then watering
- Mara → "Come here"

## Dialogue Choices

### X-17 First Impression
- "It looks dangerous." → Flag: FIRST_IMPRESSION=DANGEROUS
- "It's beautiful." → Flag: FIRST_IMPRESSION=BEAUTIFUL
- "It looks unusual." → Flag: FIRST_IMPRESSION=UNUSUAL

### Soil Dryness
- "Water it." → CORRECT → Continue
- "Change the soil." → Wrong → Return to choice
- "Move it into sunlight." → Wrong → Return to choice

### Watering Quantity
- "250 ML" → Wrong → Reset to empty
- "500 ML" → CORRECT → Continue
- "750 ML" → Wrong → Reset to empty

### Horror Response
- "Look at the flower" → Flag: FIRST_HORROR_RESPONSE=FLOWER
- "Try to leave" → Flag: FIRST_HORROR_RESPONSE=ESCAPE
- "Intercom" → Flag: FIRST_HORROR_RESPONSE=INTERCOM

## Special Effects

1. **Particle System**
   - Pollen: Floating yellow particles in greenhouse
   - Spore: Explosion particles during horror
   - Glow: Pulsating effect around X-17

2. **Screen Shake**
   - Triggered during horror sequence
   - Intensity: 20, Duration: 60 frames

3. **Sanity Effects**
   - Visual meter at top-left
   - Red overlay when sanity < 50%
   - Decreases during whispers

## Controls

- **Mouse**: Click hotspots to interact
- **ESC**: Quit game
- **I**: Toggle inventory (always visible)
- **J**: Toggle journal view

## Running the Game

```bash
cd /mnt/wwn-0x5000c5007c9be4ca-part1/evan-zhenfeng-li/apu/level-2/semester-2/imaging-and-special-effects/blooming/pro
python -m blooming
```

Or:

```bash
cd blooming
python main.py
```

## Requirements

```bash
pip install -r requirements.txt
```

Dependencies:
- pygame>=2.0.0

## Implementation Details

1. **Game Loop**: 60 FPS with proper delta time handling
2. **Scene Management**: State machine with scene transitions
3. **Dialogue System**: Callback-based choice handling
4. **Inventory**: Selection and usage tracking
5. **Flags System**: Global state tracking for game progression
6. **Journal**: Unlock entries based on game events

## Testing

The game imports successfully without errors. To test:
1. Run the game
2. Follow the dialogue choices exactly as in screenplay
3. Collect access card → Use on panel
4. Follow Mara to greenhouse
5. Take watering can → Fill with 500ml
6. Read care instructions
7. Water X-17
8. Experience horror sequence
9. Choose response and exit
