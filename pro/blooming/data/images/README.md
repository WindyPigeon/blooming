# ASSET LIST — The Blooming

## Game Specs

- **Resolution:** 1024x768
- **Style:** 2D point-and-click psychological horror, dark muted color palette
- **Color Palette:** desaturated greens, deep grays, sickly yellows, cold blues, blood reds for horror
- **Format:** PNG (transparency for sprites/props), JPG for backgrounds
- **All files go in:** `pro/blooming/assets/images/`

---

## DIRECTORY MAP

```
assets/images/
├── backgrounds/          ← 1024x768 full-screen backgrounds (7 files)
├── char/                 ← Character sprites, PNG with transparency (2-4 files)
├── props/                ← All interactive objects + X-17 flower (14 files)
├── vfx/                  ← Horror overlay images + particle sprites (2 files)
└── ending/               ← Ending/title-specific assets (3 files)
```

**Folder purpose rules:**
- `backgrounds/` — only full-screen 1024x768 backgrounds
- `char/` — only character sprite sheets or static poses
- `props/` — only interactive scene objects (plants, tools, signs, doors, tables, etc.)
- `vfx/` — only reusable visual effects (flicker, vines, particle sprites)
- `ending/` — only assets unique to the ending sequence

---

## BACKGROUND ASSETS (1024x768 each)

### 1. `backgrounds/title-screen.png` — TITLE SCREEN
**Used by:** `title_screen.py` — game title screen
**Scene:** Title / Menu
**Description:** Dark atmospheric background for the game title. Misty forest edge at dawn with a faint silhouette of a greenhouse structure barely visible through fog. Cold desaturated greens and grays. Moody, unsettling mood. No text — title is rendered in-game.
**Prompt:** `Dark atmospheric forest scene at dawn, misty fog between trees, faint silhouette of a greenhouse building barely visible through the fog, cold desaturated green and gray color palette, moody psychological horror atmosphere, cinematic composition, no text, 1024x768 resolution`

---

### 2. `backgrounds/exterior-facility.png` — FACILITY EXTERIOR (SEQ 01)
**Used by:** `scene1_arrival.py` — Arrival scene
**Scene:** SEQ 01 — Ext. Blackwood Botanical Research Facility — Morning
**Description:** Remote botanical research facility building exterior surrounded by dense forest. Morning mist between trees. Rainwater dripping from the roof. A security door is visible on one side of the building. A facility sign stands near the entrance path. Somber, overcast sky. The building should look isolated and slightly foreboding but not overtly scary yet.
**Prompt:** `Remote botanical research facility building exterior surrounded by dense dark forest, morning mist between trees, rainwater dripping from roof, overcast gray sky, isolated foreboding atmosphere, facility sign near entrance path, security door visible on building side, muted desaturated greens and grays, cinematic wide shot, 1024x768 resolution`

---

### 3. `backgrounds/corridor.png` — MAIN CORRIDOR (SEQ 02)
**Used by:** `scene2_orientation.py` — Facility orientation
**Scene:** SEQ 02 — Int. Blackwood Facility — Main Corridor — Morning
**Description:** Narrow research corridor with fluorescent lights humming overhead. Four doors visible: Staff Office (left), Storage (opposite), Restricted Laboratory (right, marked with red indicator), and Greenhouse (at the far end, with green glow from behind). Concrete walls, sterile institutional feel. Cold fluorescent lighting casting harsh shadows.
**Prompt:** `Narrow research corridor interior with fluorescent lights overhead, concrete walls, four visible doors: Staff Office door, Storage door, Restricted Laboratory door with red indicator light, Greenhouse door at far end with soft green glow from behind, sterile institutional atmosphere, cold blue-white fluorescent lighting, harsh shadows, muted grays and greens, 1024x768 resolution`

---

### 4. `backgrounds/greenhouse-interior.png` — GREENHOUSE INTERIOR (SEQ 03)
**Used by:** `scene3_greenhouse.py` and `scene4_care.py` — Greenhouse exploration
**Scene:** SEQ 03 — Int. Research Greenhouse — Morning
**Description:** Warm sunlight streaming through glass greenhouse roof. Rows of lush plants filling the room. Irrigation pipes overhead with water droplets falling. A central specimen table. A filtered water sink area. A glass ceiling with metal framing. Floating pollen particles visible in sunlight beams. Warm, inviting but with an undercurrent of unease.
**Prompt:** `Interior of a research greenhouse, warm sunlight streaming through glass ceiling panels with metal framing, rows of lush green plants filling the room, overhead irrigation pipes with water droplets, central specimen table, filtered water sink area, floating pollen particles visible in sunbeams, warm golden-green lighting, inviting but with subtle unease, 1024x768 resolution`

---

### 5. `backgrounds/greenhouse-horror.png` — HORROR GREENHOUSE (SEQ 05)
**Used by:** `scene5_horror.py` — Supernatural horror sequence
**Scene:** SEQ 05 — Greenhouse at night/later
**Description:** Same greenhouse as SEQ 03 but darkened and corrupted. Dim red emergency lighting. Flickering fluorescent lights. Thick fog/mist. Vines and roots creeping along walls. The plants look twisted and overgrown. Central specimen table with X-17 glowing. Deep shadows everywhere. Eerie, claustrophobic, threatening atmosphere.
**Prompt:** `Corrupted research greenhouse interior, dark and corrupted, dim red emergency lighting, flickering fluorescent lights, thick fog and mist, twisted overgrown vines creeping along walls, central specimen table with a glowing pale flower, deep foreboding shadows everywhere, claustrophobic threatening atmosphere, desaturated sickly color palette with red accents, 1024x768 resolution`

---

### 6. `backgrounds/ending-dark.png` — ENDING SCREEN
**Used by:** `scene5_horror.py` — Game ending
**Scene:** Final ending
**Description:** Pitch black background. A single thin root visible reaching toward the viewer from darkness. Subtle faint glow at the very tip of the root. Minimal, stark, terrifying.
**Prompt:** `Pitch black void background, a single thin pale root barely visible reaching toward viewer from darkness, faint sickly green glow at root tip, minimal stark terrifying composition, 1024x768 resolution`

---

## CHARACTER SPRITES

### 7. `char/elias-hart.png` — ELIAS HART (player character)
**Used by:** Dialogue system (speaker portrait), all scenes
**Scene:** All scenes
**Description:** Young male botanist, early 20s. Wearing a slightly worn white lab coat over dark clothing. Messy dark hair. Anxious but intelligent expression. Slouched posture suggesting discomfort. Medium shot (head to waist). Transparent background. Should look like someone out of their element in this isolated place.
**Prompt:** `Young male botanist, early 20s, wearing slightly worn white lab coat over dark clothes, messy dark hair, anxious but intelligent expression, slouched posture, medium shot head to waist, transparent background, dark muted color palette, realistic illustration style, psychological horror game character sprite`

---

### 8. `char/mara-vale.png` — DR. MARA VALE
**Used by:** All scenes where Mara appears
**Scene:** SEQ 01-07
**Description:** Middle-aged woman botanist. Professional, sharp, slightly cold demeanor. Wearing a clean lab coat. Hair tied back. Sharp features, piercing eyes. Confident posture. Medium shot. Should convey authority and subtle mystery — someone who knows more than she lets on.
**Prompt:** `Middle-aged woman botanist, professional sharp appearance, wearing clean white lab coat, hair tied back neatly, sharp piercing eyes, confident cold authoritative posture, medium shot head to waist, transparent background, dark muted color palette, realistic illustration style, psychological horror game character sprite`

---

### 9. `char/mara-left.png` — MARA (leaving / walking away)
**Used by:** `scene4_care.py` — When Mara exits greenhouse
**Scene:** SEQ 07
**Description:** Mara walking toward greenhouse exit, seen from behind or side profile. Slightly turned head as if about to look back. Same outfit as base sprite but different pose.
**Prompt:** `Middle-aged woman botanist walking away toward exit, seen from behind or side profile, slightly turned head as if about to look back, wearing white lab coat, hair tied back, transparent background, dark muted color palette, psychological horror game character sprite, walking pose`

---

### 10. `char/elias-fear.png` — ELIAS (fear expression)
**Used by:** `scene5_horror.py` — Horror response moments
**Scene:** SEQ 05
**Description:** Elias with terrified expression. Wide eyes, slightly open mouth. Hand raised defensively. Lab coat slightly disheveled. Shows genuine fear — the moment his skepticism breaks.
**Prompt:** `Young male botanist with terrified expression, wide eyes, slightly open mouth, hand raised defensively, white lab coat slightly disheveled, showing genuine fear, dark muted color palette, psychological horror game character sprite, fear expression`

---

## FLOWER / X-17 SPRITES

### 11. `props/flower.png` — SPECIMEN X-17 (normal/closed)
**Used by:** `scene3_greenhouse.py`, `scene4_care.py` — X-17 interaction
**Scene:** SEQ 04-06
**Description:** A small pale closed flower bud growing from dark soil in a simple black flowerpot. The petals are pale white/cream, tightly closed. The stem is thin but upright. A small metal label reads "SPECIMEN X-17". The flower looks fragile but with something subtly wrong — the petals have a slightly unnatural texture. The flowerpot sits on a metal specimen table.
**Prompt:** `Small pale white cream closed flower bud in simple black flowerpot, petals tightly closed thin upright stem, dark soil in pot, metal specimen table underneath, flower looks fragile but subtly wrong, petals have slightly unnatural texture, simple metal label on pot, dark muted color palette, top-down angled view, 1024x768 game asset`

---

### 12. `props/flower-glow.png` — X-17 (glowing)
**Used by:** `scene3_greenhouse.py` (after watering), `scene5_horror.py` — supernatural event
**Scene:** SEQ 07, SEQ 08
**Description:** Same X-17 flower but now with an eerie supernatural glow emanating from within the petals. Soft yellow-green bioluminescent light. The closed petals are slightly parted as if breathing. Pollen particles floating around it. The glow should be visible from within the petals, creating an unsettling warm light that contrasts with the dark background.
**Prompt:** `Small pale flower in black flowerpot with eerie supernatural bioluminescent yellow-green glow emanating from within closed petals, petals slightly parted as if breathing, floating pollen particles around it, unsettling warm glow, dark background, supernatural horror aesthetic, 1024x768 game asset`

---

### 13. `props/flower-glowing-closed.png` — X-17 (fully closed after fear)
**Used by:** `scene5_horror.py` phase 3+ — after horror response
**Scene:** SEQ 08
**Description:** X-17 flower fully closed tight with the glow pulsing intensely. The pot looks slightly cracked. Dark soil appears to be shifting. The glow is now more red-tinged and aggressive.
**Prompt:** `Small pale flower in cracked black flowerpot, flower fully closed tight with intense pulsing yellow-green-red bioluminescent glow, dark soil shifting inside pot, aggressive unsettling glow, supernatural horror aesthetic, dark background, 1024x768 game asset`

---

## GREENHOUSE ASSETS

### 14. `backgrounds/greenhouse-exterior.png` — GREENHOUSE EXTERIOR (for title/menu)
**Used by:** Title screen background or chapter select
**Scene:** Menu/Title
**Description:** A glass greenhouse building surrounded by dense dark forest at twilight. Fog rolling around the base. One light on inside, casting an eerie warm glow through the glass. Creepy isolated atmosphere.
**Prompt:** `Glass greenhouse building surrounded by dense dark forest at twilight, fog rolling around base, single warm light visible inside greenhouse casting eerie glow through glass panels, isolated creepy atmosphere, muted desaturated greens and grays, cinematic wide shot, 1024x768 resolution`

---

### 15. `backgrounds/corridor-exterior.png` — CORRIDOR EXTERIOR VIEW
**Used by:** Scene transition or as alternative background
**Scene:** SEQ 02 transition
**Description:** View from the corridor looking toward the greenhouse door from inside. The door is slightly ajar with green light seeping through the crack.
**Prompt:** `Corridor interior looking toward greenhouse door, door slightly ajar with green light seeping through crack, narrow perspective, institutional fluorescent lighting fading to green glow, 1024x768 resolution`

---

## PROPS / HOTSPOTS (PNG with transparency, various sizes)

### 16. `props/access-card.png` — ACCESS CARD (Level 1)
**Used by:** Inventory system, door interaction
**Scene:** SEQ 01
**Description:** Small rectangular access card, white/light gray with "LEVEL 1" printed on it. Black barcode at bottom. Looks like a standard facility ID card.
**Prompt:** `Small rectangular white access card with LEVEL 1 printed on it, black barcode at bottom, standard facility ID card design, clean minimal look, transparent background, game prop asset`

---

### 17. `props/watering-can.png` — WATERING CAN
**Used by:** `scene3_greenhouse.py`, `scene4_care.py` — watering puzzle
**Scene:** SEQ 03, SEQ 06
**Description:** Standard metal watering can, silver-gray, about 500ml capacity. Simple utilitarian design. Handle on top, long spout on one side.
**Prompt:** `Standard silver-gray metal watering can, 500ml capacity, simple utilitarian design, handle on top, long spout, transparent background, game prop asset, 80x80 pixels`

---

### 18. `props/sink.png` — FILTERED WATER SINK
**Used by:** `scene3_greenhouse.py` — water filling station
**Scene:** SEQ 06
**Description:** Small stainless steel laboratory sink with water faucet. Clean, functional. Water flowing from faucet (visible stream).
**Prompt:** `Small stainless steel laboratory sink with water faucet, clean functional design, water flowing from faucet visible stream, transparent background, game prop asset, 80x80 pixels`

---

### 19. `props/clipboard.png` — CARE INSTRUCTION CLIPBOARD
**Used by:** `scene3_greenhouse.py` — care sheet document
**Scene:** SEQ 06
**Description:** White clipboard with paper attached showing care instructions. Text visible: "SPECIMEN X-17 / DAILY CARE PROCEDURE". Paper is slightly crumpled.
**Prompt:** `White clipboard with crumpled paper attached showing text SPECIMEN X-17 DAILY CARE PROCEDURE, visible typed instructions, metal clip at top, transparent background, game prop asset, 80x80 pixels`

---

### 20. `props/thermometer.png` — GREENHOUSE THERMOMETER
**Used by:** `scene3_greenhouse.py` — temperature check
**Scene:** SEQ 03
**Description:** Wall-mounted glass thermometer showing 24°C. Red mercury line visible. Mounted on glass wall or greenhouse frame.
**Prompt:** `Wall-mounted glass thermometer showing 24 degrees Celsius, red mercury line visible, mounted on glass greenhouse frame, transparent background, game prop asset, 60x120 pixels`

---

### 21. `props/storage-cabinet.png` — STORAGE CABINET
**Used by:** `scene3_greenhouse.py` — storage item
**Scene:** SEQ 03
**Description:** Tall gray metal storage cabinet with doors. Contains general supplies and extra pots. Industrial, slightly rusted look.
**Prompt:** `Tall gray metal storage cabinet with doors, contains general supplies and extra pots visible through glass panel, industrial slightly rusted look, transparent background, game prop asset, 80x80 pixels`

---

### 22. `props/old-journal.png` — OLD RESEARCH JOURNAL
**Used by:** `scene3_greenhouse.py` — journal interaction
**Scene:** SEQ 03
**Description:** Old leather-bound research journal lying open on a table. Yellowed pages with handwritten notes. Cover looks worn and aged.
**Prompt:** `Old leather-bound research journal lying open on table, yellowed pages with handwritten notes, worn aged cover, mysterious antique look, transparent background, game prop asset, 80x80 pixels`

---

### 23. `props/facility-sign.png` — FACILITY SIGN
**Used by:** `scene1_arrival.py` — sign interaction
**Scene:** SEQ 01
**Description:** Metal sign reading "BLACKWOOD BOTANICAL RESEARCH FACILITY / AUTHORIZED PERSONNEL ONLY". Weathered, slightly rusted edges. Mounted on a metal post.
**Prompt:** `Metal sign reading BLACKWOOD BOTANICAL RESEARCH FACILITY AUTHORIZED PERSONNEL ONLY, weathered slightly rusted edges, mounted on metal post, outdoor sign, transparent background, game prop asset`

---

### 24. `props/security-door.png` — SECURITY DOOR (with panel)
**Used by:** `scene1_arrival.py` — main door interaction
**Scene:** SEQ 01
**Description:** Heavy metal security door with access card panel beside it. Red indicator light (locked state). Panel has a card slot and small LED display.
**Prompt:** `Heavy metal security door with access card panel beside it, red indicator light showing locked state, card slot and small LED display on panel, industrial security door design, transparent background, game prop asset`

---

### 25. `props/intercom.png` — INTERCOM
**Used by:** `scene1_arrival.py`, `scene5_horror.py` — intercom interaction
**Scene:** SEQ 01, SEQ 08
**Description:** Wall-mounted intercom box with speaker grille, call button, and small display screen. Industrial gray metal.
**Prompt:** `Wall-mounted industrial gray metal intercom box with speaker grille, call button, and small display screen, security intercom design, transparent background, game prop asset, 100x100 pixels`

---

### 26. `props/specimen-table.png` — CENTRAL SPECIMEN TABLE
**Used by:** `scene3_greenhouse.py`, `scene4_care.py` — X-17 display table
**Scene:** SEQ 04-06
**Description:** Stainless steel laboratory specimen table. Flat surface with drainage grooves. Industrial medical-grade appearance.
**Prompt:** `Stainless steel laboratory specimen table, flat surface with drainage grooves, industrial medical-grade appearance, transparent background, game prop asset, 220x130 pixels`

---

## EFFECTS / OVERLAYS

### 27. `vfx/screen-flicker.png` — SCREEN FLICKER OVERLAY
**Used by:** `scene5_horror.py` — light flicker effect
**Scene:** SEQ 08
**Description:** Semi-transparent dark overlay with vertical scan-line pattern. Should be partially transparent so it darkens the screen without completely obscuring it.
**Prompt:** `Semi-transparent dark overlay with subtle vertical scan-line pattern, flicker effect design, 1024x768 resolution`

---

### 28. `vfx/vine-overlay.png` — VINE ROOT OVERLAY
**Used by:** `scene5_horror.py` — horror vines
**Scene:** SEQ 08
**Description:** Dark purple-black creeping vines/roots growing along walls and floor. Organic, threatening, slightly bioluminescent edges.
**Prompt:** `Dark purple-black creeping vines and roots growing along walls and floor, organic threatening pattern, slight bioluminescent purple edges, transparent background, horror game overlay asset`

---

### 29. `vfx/pollen-particles.png` — POLLEN PARTICLE SPRITE
**Used by:** `scene3_greenhouse.py` — ambient pollen particles
**Scene:** SEQ 03
**Description:** Small circular glow sprite — soft yellow-gold particle, 4x4 to 8x8 pixels. Should look like a tiny glowing speck.
**Prompt:** `Small circular soft yellow-gold glowing particle, 4x4 pixels, tiny glowing speck, transparent background, game particle sprite`

---

## ENDING ASSETS

### 30. `ending/root.png` — ROOT EXTENDING FROM GREENHOUSE
**Used by:** `scene5_horror.py`, `scene5_ending.py` — final scene
**Scene:** End of SEQ 08 / game ending
**Description:** A thin pale root extending from the greenhouse door frame, reaching across the floor toward the viewer. Subtly glowing at the tip. Creepy, unsettling, barely visible in darkness.
**Prompt:** `Thin pale root extending from greenhouse door frame, reaching across dark floor toward viewer, subtle glow at tip, creepy unsettling barely visible in darkness, transparent background, horror game asset`

---

### 31. `ending/title-card.png` — END OF DAY 1 TITLE CARD
**Used by:** `scene5_horror.py` — phase 4 title screen
**Scene:** End of Day 1
**Description:** Black screen with "END OF DAY 1" in stark red text centered. Faint green whisper text below it barely visible. Minimal, clean, chilling.
**Prompt:** `Black screen with END OF DAY 1 in stark red centered text, faint green whisper text below barely visible, minimal clean chilling design, 1024x768 resolution`

---

### 32. `ending/heart-pulse.png` — HEART PULSE VFX
**Used by:** `scene5_horror.py` — heartbeat visual
**Scene:** SEQ 08
**Description:** Simple red heartbeat pulse line — like an ECG monitor line. Thin, pulsing. Should be subtle, not cartoonish.
**Prompt:** `Simple red heartbeat pulse line like ECG monitor, thin pulsing line, subtle not cartoonish, transparent background, horror game VFX asset`

---

## PRIORITY ORDER

### TIER 1 — CRITICAL (must have first)
| # | File | Used In |
|---|------|---------|
| 1 | `char/elias-hart.png` | Dialogue portraits, all scenes |
| 2 | `char/mara-vale.png` | Dialogue portraits, all scenes |
| 3 | `backgrounds/exterior-facility.png` | Scene 1 background |
| 4 | `backgrounds/greenhouse-interior.png` | Scene 3/4 background |
| 5 | `backgrounds/corridor.png` | Scene 2 background |
| 6 | `props/flower.png` | X-17 normal state |
| 7 | `props/flower-glow.png` | X-17 glowing state |
| 8 | `props/flower-glowing-closed.png` | X-17 horror state |

### TIER 2 — IMPORTANT (scenes won't look complete without these)
| # | File | Used In |
|---|------|---------|
| 9 | `props/access-card.png` | Inventory, door puzzle |
| 10 | `props/watering-can.png` | Watering puzzle |
| 11 | `props/sink.png` | Water filling station |
| 12 | `props/clipboard.png` | Care instructions |
| 13 | `props/thermometer.png` | Temperature check |
| 14 | `props/storage-cabinet.png` | Storage prop |
| 15 | `props/old-journal.png` | Journal interaction |
| 16 | `props/facility-sign.png` | Sign hotspot |
| 17 | `props/security-door.png` | Door hotspot |
| 18 | `props/intercom.png` | Intercom hotspot |
| 19 | `props/specimen-table.png` | X-17 display table |

### TIER 3 — HORROR / ATMOSPHERE (makes the game scary)
| # | File | Used In |
|---|------|---------|
| 20 | `backgrounds/greenhouse-horror.png` | Horror scene background |
| 21 | `char/mara-left.png` | Mara leaving |
| 22 | `char/elias-fear.png` | Fear expression |
| 23 | `vfx/screen-flicker.png` | Light flicker |
| 24 | `vfx/vine-overlay.png` | Horror vines |
| 25 | `vfx/pollen-particles.png` | Ambient particles |

### TIER 4 — ENDING (wrap up)
| # | File | Used In |
|---|------|---------|
| 26 | `ending/root.png` | Final scene |
| 27 | `ending/title-card.png` | End of Day 1 |
| 28 | `ending/heart-pulse.png` | Heartbeat VFX |
| 29 | `backgrounds/title-screen.png` | Title screen |
| 30 | `backgrounds/greenhouse-exterior.png` | Menu/transition |
| 31 | `backgrounds/corridor-exterior.png` | Transition view |

---

## HOW AI AGENTS SHOULD USE THIS FILE

### When generating assets:
1. **Always check the PRIORITY TIER first** — generate Tier 1 before anything else
2. **Use the exact filenames** listed — scenes import by these paths via `load_image()`
3. **Follow the prompt format** — each prompt includes subject, style, colors, and resolution
4. **PNG with transparency** for all sprites/props/backgrounds
5. **1024x768 resolution** for all backgrounds

### When reading this file:
1. This file maps each asset to its **scene file** and **screenplay sequence**
2. The `Used by` column tells you exactly which Python file uses each asset
3. The screenplay sequence (SEQ 01-08) connects the asset to the narrative
4. Directory paths must match exactly — assets not in the right folder won't load
5. The game falls back to **colored rectangles** if an asset is missing — so the game won't crash without art

### Asset loading in code:
```python
# All assets loaded via this function:
from blooming.utils.utils import load_image
self.my_img = load_image('folder/filename.png')
# e.g.: load_image('props/flower.png')
# e.g.: load_image('props/watering-can.png')
```

### Scene-to-background mapping:
| Scene | Python File | Background |
|-------|------------|------------|
| SEQ 01 | `scene1_arrival.py` | `backgrounds/exterior-facility.png` |
| SEQ 02 | `scene2_orientation.py` | `backgrounds/corridor.png` |
| SEQ 03 | `scene3_greenhouse.py` | `backgrounds/greenhouse-interior.png` |
| SEQ 04 | `scene3_greenhouse.py` | `backgrounds/greenhouse-interior.png` |
| SEQ 05 | `scene4_care.py` | `backgrounds/greenhouse-interior.png` |
| SEQ 06 | `scene4_care.py` | `backgrounds/greenhouse-interior.png` |
| SEQ 07 | `scene4_care.py` | `backgrounds/greenhouse-interior.png` |
| SEQ 08 | `scene5_horror.py` | `backgrounds/greenhouse-horror.png` |
