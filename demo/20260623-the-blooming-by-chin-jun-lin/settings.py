"""
settings.py
===========
Central configuration for THE BLOOMING.

THIS IS THE MAIN FILE YOU EDIT to plug in your own art and audio.

How asset loading works (see core/assets.py):
  - The game looks for a file in the matching assets/ sub-folder.
  - If the file exists, it is used.
  - If it is missing, a procedural placeholder is generated automatically
    so the game still runs. You will see a friendly note in the console
    telling you which file to add.

So you can run the game right now with zero art, then drop real files in
later WITHOUT touching any code, as long as you keep the filenames below.
"""

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "The Blooming"

# ---------------------------------------------------------------------------
# Colour palette (R, G, B)   -- used by the procedural placeholders + UI
# ---------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (235, 235, 235)
DIM = (150, 150, 150)
GREEN = (60, 140, 80)
DARK_GREEN = (18, 40, 28)
NIGHT = (10, 18, 26)
ROT = (40, 22, 22)
BLOOD = (120, 20, 30)
GOLD = (210, 170, 90)
POLLEN = (200, 220, 140)
SPORE = (180, 120, 200)
UI_BG = (12, 14, 16)
UI_LINE = (70, 80, 70)

# ---------------------------------------------------------------------------
# Asset folders (relative to the game root)
# ---------------------------------------------------------------------------
ASSET_ROOT = "assets"
DIR_BACKGROUNDS = "backgrounds"
DIR_SPRITES = "sprites"
DIR_MUSIC = "music"
DIR_SOUNDS = "sounds"
DIR_FONTS = "fonts"

# Accepted file extensions (the loader tries each in this order).
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
AUDIO_EXTS = (".ogg", ".wav", ".mp3")

# ---------------------------------------------------------------------------
# ASSET MANIFEST
# ---------------------------------------------------------------------------
# Logical name  ->  filename (without folder).
# Drop a file with this name into the matching assets/ sub-folder and it will
# be used automatically. Change the right-hand side if you prefer other names.

BACKGROUNDS = {
    "menu":             "menu.png",
    "greenhouse":       "greenhouse.png",          # Scene 1
    "greenhouse_night": "greenhouse_night.png",    # Scene 2
    "facility":         "facility.png",            # Scene 3
    "heart_chamber":    "heart_chamber.png",       # Scene 4
    "ending":           "ending.png",
}

SPRITES = {
    "plant":         "plant.png",          # the mysterious flower (Scenes 1-2)
    "plant_glow":    "plant_glow.png",     # glowing version after watering
    "giant_flower":  "giant_flower.png",   # Scene 4 carnivorous bloom
    "watering_can":  "watering_can.png",
    "note":          "note.png",
    "keycard":       "keycard.png",
    "shadow_figure": "shadow_figure.png",  # hallucination figure
    "root":          "root.png",           # crawling root tile
    "elias_face":    "elias_face.png",     # final flower bearing Elias' face
}

MUSIC = {
    "menu":          "menu_theme.ogg",
    "greenhouse":    "greenhouse_ambience.ogg",   # Scene 1
    "suspense":      "suspense_theme.ogg",        # Scene 2
    "horror":        "horror_atmosphere.ogg",     # Scene 3
    "final":         "final_encounter.ogg",       # Scene 4
}

SOUNDS = {
    "whisper":     "whisper.ogg",
    "whisper_layered": "whisper_layered.ogg",
    "water":       "water.ogg",
    "glow":        "glow.ogg",
    "pickup":      "pickup.ogg",
    "click":       "click.ogg",
    "denied":      "denied.ogg",
    "unlock":      "unlock.ogg",
    "root_crack":  "root_crack.ogg",
    "heartbeat":   "heartbeat.ogg",
    "door":        "door.ogg",
    "spore_burst": "spore_burst.ogg",
    "bloom":       "bloom.ogg",
}

# Optional custom font. Leave the file out to use the built-in system font.
FONT_MAIN = "main.ttf"

# ---------------------------------------------------------------------------
# Gameplay tuning
# ---------------------------------------------------------------------------
SANITY_MAX = 100
SANITY_START = 100
# Sanity drain per second while inside the "madness" scenes.
SANITY_DRAIN_SCENE3 = 1.6
SANITY_DRAIN_SCENE4 = 2.4
# Below this value, hallucination / distortion effects kick in.
SANITY_HALLUCINATION_THRESHOLD = 55

# Scene 2 door code. Clues are scattered in the notes the player collects.
DOOR_CODE = "412"

# Save file
SAVE_FILE = "savegame.json"
