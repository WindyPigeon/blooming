"""
scenes/descent.py  -  SCENE 3: DESCENT INTO MADNESS
===================================================
Environment : Corrupted research facility
Objectives  : read the caretaker records, find the keycard, open restricted lab
Key events  : hallucinations intensify, plants seem to watch you, roots crawl
Effects     : screen distortion (sanity-driven), pulsating roots, heartbeat
Mechanics   : active SANITY DRAIN; distortion + hallucination figures scale
              with how low your sanity gets; a hidden keycard
"""

import math
import random
import pygame

import settings as S
from core import fx
from core.scene import Scene, Hotspot


class DescentScene(Scene):
    background_name = "facility"
    music_name = "horror"
    sanity_drain = S.SANITY_DRAIN_SCENE3

    def setup(self):
        self.title = "III  -  Descent into Madness"
        self.add_objective("Read the caretaker records")
        self.add_objective("Find the keycard")
        self.add_objective("Open the restricted lab")

        self.records_read = False
        self.has_keycard = False
        self.root_phase = 0.0
        self.eyes = [(random.randint(80, S.WIDTH - 80),
                      random.randint(120, 360)) for _ in range(6)]

        self.hs_records = Hotspot(
            (160, 320, 200, 200), "Personnel records",
            on_click=self._read_records, cursor="look")
        # Keycard hidden among the roots; only "found" on click.
        self.hs_keycard = Hotspot(
            (760, 470, 90, 70), "Something glinting", cursor="take",
            on_click=self._take_keycard)
        self.hs_lab = Hotspot(
            (S.WIDTH - 170, 220, 150, 360), "Restricted lab",
            on_click=self._open_lab, cursor="go", requires_item="keycard")

        self.hotspots = [self.hs_records, self.hs_keycard, self.hs_lab]

        self.say([
            "The walls are wrong. Roots run through the concrete like veins.",
            "My hands won't stop shaking. The whispering never stops now.",
            "Keep it together, Elias. Find out what happened to the others.",
        ], "Elias")

    # --- handlers ----------------------------------------------------------
    def _read_records(self, used_item=None):
        if not self.records_read:
            self.records_read = True
            self.complete("Read the caretaker records")
            self.ctx.journal.add(
                "Personnel file: every caretaker before me 'transferred' on the "
                "same date. No forwarding address. No bodies. The specimen log "
                "simply reads: 'fed'.")
            self.say([
                "'Caretaker transferred.' All of them. Same date.",
                "No transfer paperwork. No bodies. Just one word in the log...",
                "'Fed.'",
            ], "Elias")
            self.ctx.sanity.change(-8)

    def _take_keycard(self, used_item=None):
        if not self.has_keycard:
            self.has_keycard = True
            self.ctx.inventory.add("keycard", "Lab Keycard", "keycard")
            self.complete("Find the keycard")
            self.hs_keycard.enabled = False
            self.hs_keycard.visible = False
            self.say("A keycard, tangled in the roots. Still warm. Why is it warm?",
                     "Elias")

    def _open_lab(self, used_item=None):
        if used_item == "keycard" or self.ctx.inventory.has("keycard"):
            from scenes.blooming import BloomingScene
            self.assets.play_sound("unlock", 0.7)
            self.complete("Open the restricted lab")
            self.assets.play_sound("door", 0.6)
            self.go_to(BloomingScene)
        else:
            self.say("Locked. A keycard reader blinks red.", "Elias")

    # --- per-frame ---------------------------------------------------------
    def update_scene(self, dt):
        self.root_phase += dt
        # Corruption motes.
        self.particles.ambient_pollen(
            dt, pygame.Rect(0, 100, S.WIDTH, 400), density=0.5, col=S.ROT[:3] and (90, 50, 50))
        # Clicking nothing still advances dread: occasional root crack.
        if random.random() < 0.006:
            self.assets.play_sound("root_crack", 0.4)

        # If sanity bottoms out, the plant takes Elias here too (bad end -> finale).
        if self.ctx.sanity.value <= 0 and not self.ctx.fade.busy:
            from scenes.blooming import BloomingScene
            self.go_to(BloomingScene)

    def draw_scene(self, surf):
        # Pulsating roots crawling across the lower walls.
        self._draw_roots(surf)

        # The keycard glint.
        if self.hs_keycard.visible:
            card = self.assets.sprite("keycard", (70, 50))
            surf.blit(card, (765, 480))
            fx.glow(surf, (800, 505), 40, S.GOLD, intensity=80)

        # Watching eyes appear as sanity drops (hallucination).
        if self.ctx.sanity.hallucinating:
            amt = self.ctx.sanity.distortion_amount
            for ex, ey in self.eyes:
                a = int(120 * amt)
                eye = pygame.Surface((26, 14), pygame.SRCALPHA)
                pygame.draw.ellipse(eye, (200, 40, 50, a), eye.get_rect())
                pygame.draw.circle(eye, (10, 0, 0, a), (13, 7), 4)
                surf.blit(eye, (ex, ey))

        # Heartbeat-driven heat + distortion at low sanity (applied in scene draw
        # override below so it affects the whole frame).

    def _draw_roots(self, surf):
        pulse = 0.5 + 0.5 * math.sin(self.root_phase * 3)
        root = self.assets.sprite("root", (260, 140))
        for i, x in enumerate(range(-40, S.WIDTH, 240)):
            y = int(S.HEIGHT * 0.62 + math.sin(self.root_phase + i) * 14)
            r = root.copy()
            r.set_alpha(int(140 + 80 * pulse))
            surf.blit(r, (x, y))

    # Override draw to apply full-screen distortion at low sanity.
    def draw(self, surf):
        amt = self.ctx.sanity.distortion_amount
        if amt > 0:
            # Render scene to a temp surface, then distort it.
            temp = surf.copy()
            super().draw(temp)
            distorted = fx.distortion(temp, amt)
            surf.blit(distorted, (0, 0))
            fx.heat_pulse(surf, self.time, colour=(60, 10, 14),
                          base=10, amp=int(30 * amt))
            fx.vignette(surf, strength=140 + int(80 * amt))
        else:
            super().draw(surf)
            fx.vignette(surf, strength=120)
