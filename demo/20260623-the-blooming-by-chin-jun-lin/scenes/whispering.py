"""
scenes/whispering.py  -  SCENE 2: WHISPERING GROWTH
===================================================
Environment : Greenhouse at night
Objectives  : collect the 3 research notes, solve the lock, open the door
Key events  : lights flicker, shadows pass, whispers swell
Effects     : dynamic light mask around the cursor, fluorescent flicker,
              drifting shadow figures, whisper audio that builds
Mechanics   : collect items, an on-screen KEYPAD puzzle (code in settings)
"""

import random
import pygame

import settings as S
from core import fx
from core.scene import Scene, Hotspot
from core.ui import wrap_text


class WhisperingScene(Scene):
    background_name = "greenhouse_night"
    music_name = "suspense"
    sanity_drain = 0.0

    def setup(self):
        self.title = "II  -  Whispering Growth"
        self.add_objective("Collect 3 research notes")
        self.add_objective("Unlock the wing door")

        self.notes_found = 0
        self.keypad_open = False
        self.entered = ""
        self.unlocked = False
        self.whisper_t = 0.0
        self.shadows = []   # drifting shadow figures: [x, y, speed, alpha]

        # Three notes hidden around the room.
        note_spots = [(180, 250), (620, 520), (1040, 300)]
        self.note_hotspots = []
        clues = [
            "Note 1: 'The lock needs three digits. The first is the number "
            "of petals I counted on the first bloom: four.'",
            "Note 2: 'Second digit: the specimen was logged on the 1st of the "
            "month.'",
            "Note 3: 'Last digit... it whispers a number to me at night. Two. "
            "Always two.'",
        ]
        for i, (x, y) in enumerate(note_spots):
            hs = Hotspot((x, y, 80, 80), f"Research note {i+1}",
                         cursor="take")
            hs.clue = clues[i]
            hs.idx = i
            hs.on_click = (lambda used_item=None, h=hs: self._take_note(h))
            self.note_hotspots.append(hs)

        self.hs_door = Hotspot(
            (S.WIDTH // 2 - 70, 180, 140, 380), "Locked wing door",
            on_click=self._touch_door, cursor="go")

        self.hotspots = self.note_hotspots + [self.hs_door]

        self.say([
            "The lights cut out an hour ago. Only the emergency strips remain.",
            "The whispering... it isn't in my head. It's coming from the plants.",
            "There's a coded lock on the wing door. The notes must hold the code.",
        ], "Elias")

    # --- handlers ----------------------------------------------------------
    def _take_note(self, hs):
        if not hs.enabled:
            return
        hs.enabled = False
        hs.visible = False
        self.notes_found += 1
        self.ctx.inventory.add(f"note{hs.idx}", f"Note {hs.idx+1}", "note")
        self.ctx.journal.add(hs.clue)
        self.assets.play_sound("whisper", 0.4)
        if self.notes_found >= 3:
            self.complete("Collect 3 research notes")
            self.say("Four... one... two. I think that's the code. The door.",
                     "Elias")
        else:
            self.say("A torn page. The handwriting grows more frantic each note.",
                     "Elias")

    def _touch_door(self, used_item=None):
        if self.unlocked:
            from scenes.descent import DescentScene
            self.assets.play_sound("door", 0.6)
            self.go_to(DescentScene)
            return
        self.keypad_open = True

    # --- keypad ------------------------------------------------------------
    def _keypad_rects(self):
        rects = {}
        bx, by = S.WIDTH // 2 - 110, 230
        for i in range(9):
            r = pygame.Rect(bx + (i % 3) * 80, by + (i // 3) * 80, 64, 64)
            rects[str(i + 1)] = r
        rects["0"] = pygame.Rect(bx + 80, by + 240, 64, 64)
        rects["C"] = pygame.Rect(bx, by + 240, 64, 64)
        rects["OK"] = pygame.Rect(bx + 160, by + 240, 64, 64)
        return rects

    def _keypad_click(self, pos):
        for key, r in self._keypad_rects().items():
            if r.collidepoint(pos):
                self.assets.play_sound("click", 0.4)
                if key == "C":
                    self.entered = ""
                elif key == "OK":
                    self._check_code()
                elif len(self.entered) < 3:
                    self.entered += key
                return True
        # click outside closes
        panel = pygame.Rect(S.WIDTH // 2 - 150, 150, 300, 420)
        if not panel.collidepoint(pos):
            self.keypad_open = False
        return True

    def _check_code(self):
        if self.entered == S.DOOR_CODE:
            self.unlocked = True
            self.keypad_open = False
            self.complete("Unlock the wing door")
            self.assets.play_sound("unlock", 0.8)
            self.say("A heavy click. The wing door drifts open into the dark.",
                     "Elias")
        else:
            self.assets.play_sound("denied", 0.6)
            self.entered = ""
            self.ctx.sanity.change(-4)

    # --- input -------------------------------------------------------------
    def handle_event(self, e):
        if self.keypad_open and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self._keypad_click(e.pos)
            return
        super().handle_event(e)

    # --- per-frame ---------------------------------------------------------
    def update_scene(self, dt):
        self.whisper_t += dt
        # Whisper swells the longer you stay / the more notes you read.
        if self.whisper_t > max(5.0, 9.0 - self.notes_found * 1.5):
            self.whisper_t = 0.0
            self.assets.play_sound("whisper_layered", 0.3 + 0.15 * self.notes_found)

        # Spawn drifting shadow figures occasionally.
        if random.random() < 0.004 + 0.004 * self.notes_found and len(self.shadows) < 3:
            y = random.randint(220, 420)
            self.shadows.append([-120, y, random.uniform(40, 80),
                                 random.randint(60, 120)])
        for s in self.shadows:
            s[0] += s[2] * dt
        self.shadows = [s for s in self.shadows if s[0] < S.WIDTH + 140]

        self.particles.ambient_pollen(
            dt, pygame.Rect(0, 120, S.WIDTH, 260), density=0.3, col=S.SPORE)

    def draw_scene(self, surf):
        # Draw remaining notes.
        for hs in self.note_hotspots:
            if hs.visible:
                note = self.assets.sprite("note", (70, 70))
                surf.blit(note, hs.rect.topleft)

        # Shadow figures behind the light mask.
        for x, y, _spd, alpha in self.shadows:
            fig = self.assets.sprite("shadow_figure", (110, 250)).copy()
            fig.set_alpha(alpha)
            surf.blit(fig, (int(x), int(y)))

        # Dynamic darkness with a light around the cursor (only when no overlay).
        if not (self.ctx.journal.open or self.keypad_open):
            fx.light_mask(surf, pygame.mouse.get_pos(), radius=300, darkness=215)
        # Failing-light flicker.
        fx.flicker_overlay(surf, intensity=0.6 + 0.1 * self.notes_found)

        if self.keypad_open:
            self._draw_keypad(surf)

    def _draw_keypad(self, surf):
        panel = pygame.Rect(S.WIDTH // 2 - 150, 150, 300, 420)
        s = pygame.Surface(panel.size, pygame.SRCALPHA)
        s.fill((14, 16, 18, 245))
        surf.blit(s, panel.topleft)
        pygame.draw.rect(surf, S.UI_LINE, panel, 2)

        f = self.assets.font(40)
        disp = self.entered.ljust(3, "_")
        t = f.render(disp, True, S.GOLD)
        surf.blit(t, (S.WIDTH // 2 - t.get_width() // 2, 175))

        kf = self.assets.font(30)
        for key, r in self._keypad_rects().items():
            col = (40, 60, 50) if key not in ("C", "OK") else (60, 40, 40)
            pygame.draw.rect(surf, col, r, border_radius=6)
            pygame.draw.rect(surf, S.UI_LINE, r, 2, border_radius=6)
            lab = kf.render(key, True, S.WHITE)
            surf.blit(lab, (r.centerx - lab.get_width() // 2,
                            r.centery - lab.get_height() // 2))
