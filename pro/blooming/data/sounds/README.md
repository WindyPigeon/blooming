# Sound Effects Library

## Files Available

### `click_mouse.ogg`
- **Scene:** UI — title_screen, chapter_select, pause_menu
- **Description:** Button click / selection
- **Type:** Short, clean click, 1 shot
- **Source:** pygame `pygame-menu` — `click_mouse.ogg`

### `widget_selection.ogg`
- **Scene:** Chapter 1 (chapter1_arrival)
- **Description:** Interaction selection cue
- **Type:** Short selection sound, 1 shot
- **Source:** pygame `pygame-menu` — `widget_selection.ogg`

### `key_add.ogg`
- **Scene:** Chapter 1 (chapter1_arrival)
- **Description:** Text / dialogue tick
- **Type:** Short key press sound, 1 shot
- **Source:** pygame `pygame-menu` — `key_add.ogg`

### `scan.ogg`
- **Scene:** Sequence 01, Sequence 02, Sequence 09
- **Description:** Card scan swipe sound
- **Type:** Short electronic swipe, 1 shot
- **Source:** pygame `zanthor` — `upgrade.ogg` (GPL 2)

### `door_close.ogg`
- **Scene:** Sequence 09
- **Description:** Greenhouse door closing
- **Type:** Short mechanical close, 1 shot
- **Source:** pygame `zanthor` — `hitwall.ogg` (GPL 2)

### `ouch.ogg`
- **Scene:** Sequence 09
- **Description:** Low horror stinger (root reveals)
- **Type:** Short sharp sting, ~1–2 seconds
- **Source:** pygame `zanthor` — `ouch1.ogg` (GPL 2)

### `pickup.wav`
- **Scene:** Sequence 01, Sequence 03
- **Description:** Item acquired into inventory
- **Type:** Short positive chime, 1 shot
- **Source:** pygame `solarwolf` — `chimein.wav` (LGPL 2.1)

### `splash.ogg`
- **Scene:** Sequence 07
- **Description:** Water pouring onto soil from watering can
- **Type:** 2–3 seconds, triggered on watering X-17
- **Source:** pygame `stuntcat` — `splash.ogg` (LGPL 2.1)

### `whisper.ogg`
- **Scene:** Sequence 08
- **Description:** Whispered "Elias..." from the plant
- **Type:** Pan & reverb, loops during horror sequence
- **Source:** pygame `stuntcat` — `boo.ogg` (LGPL 2.1)

### `rain.ogg`
- **Scene:** Sequence 01 (chapter1_arrival)
- **Description:** Continuous rain falling at the facility exterior
- **Type:** Loopable ambience
- **Source:** Custom SFX

---

## Files Still Needed

These SFX are referenced in code but **not available** in `data/sounds/`:

| Filename | Scene | Description |
|---|---|---|
| `spark` | Ch1, Ch3 | Sharp electrical click (intercom dies) |
| `door_open` | Ch1 | Automatic door sliding open |
| `static` | Ch3 | Radio static crackle |
| `lock` | Ch3 | Electronic lock engaging |
| `intercom` | Ch3 | Intercom button press / activation |
| `page` | Ch2 | Dialogue box advance / page turn |
| `hum` | Ch4 | Low ethereal hum as X-17 glows |
| `heartbeat` | Ch4 | Low heartbeat pulse |
| `music_sting` | Ch4 | Short horror sting |
| `glitch` | Ch4 | Subtle audio glitch / distortion |
| `buzz` | Ch4 | Electrical buzz during light flicker |

---

## Notes

- Default SFX volume: **0.7** (configured in `main.py` and `pause_menu.py`).
- Audio is gracefully disabled if `pygame.mixer` is unavailable.
- Horror SFX should use **stereo panning** to enhance immersion (plant whispers, heartbeat, root sounds).
- Filenames follow the [pygame official games convention](https://github.com/python-pillow/pygame): simple, lowercase, descriptive names without prefixes or underscores.
- Audio from pygame's official games:
  - **pygame-menu**: MIT
  - **zanthor**: GPL 2
  - **solarwolf**: LGPL 2.1
  - **stuntcat**: LGPL 2.1
  - These are bundled for development use. Verify licensing before public distribution.
