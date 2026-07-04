"""
scenes/blooming.py  -  SCENE 4: THE BLOOMING   (Chin Jun Lin's scene)
=====================================================================
Environment : Heart Chamber
Objectives  : confront the flower's true form, complete the final ritual
Key events  : giant carnivorous flower emerges, final hallucination,
              Elias sacrifices himself
Effects     : root-growth animation, spore explosion particles, layered
              whispers, bloom transformation, red heart-pulse lighting

This scene also INTEGRATES every system (inventory, journal, sanity, FX) and
hands off to the ending cutscene -- it is the integration + post-production
piece in the workload matrix.
"""

import math
import random
import pygame

import settings as S
from core import fx
from core.scene import Scene, Hotspot


class BloomingScene(Scene):
    background_name = "heart_chamber"
    music_name = "final"
    sanity_drain = S.SANITY_DRAIN_SCENE4

    # Phases of the finale.
    INTRO, RITUAL, BLOOM, DONE = range(4)

    def setup(self):
        self.title = "IV  -  The Blooming"
        self.add_objective("Confront the flower")
        self.add_objective("Complete the ritual")

        self.phase = self.INTRO
        self.flower_scale = 0.2          # grows during INTRO -> RITUAL
        self.center = (S.WIDTH // 2, int(S.HEIGHT * 0.55))
        self.whisper_t = 0.0
        self.bloom_t = 0.0
        self.root_grow = 0.0             # 0..1 root growth animation

        # Ritual: five glowing nodes that must be clicked in order.
        self.nodes = []
        self.next_node = 0
        radius = 230
        for i in range(5):
            ang = -math.pi / 2 + (math.tau / 5) * i
            nx = self.center[0] + math.cos(ang) * radius
            ny = self.center[1] + math.sin(ang) * radius
            self.nodes.append([nx, ny, False])   # x, y, lit

        self.hs_flower = Hotspot(
            (self.center[0] - 120, self.center[1] - 120, 240, 240),
            "The flower's heart", on_click=self._touch_flower, cursor="use")
        self.hotspots = [self.hs_flower]

        self.say([
            "The heart chamber. The flower fills it now, wall to wall.",
            "It is beautiful. It is the only beautiful thing left.",
            "It is calling my name. ...All right. I'm here.",
        ], "Elias")

    # --- handlers ----------------------------------------------------------
    def _touch_flower(self, used_item=None):
        if self.phase == self.INTRO:
            self.phase = self.RITUAL
            self.complete("Confront the flower")
            self.assets.play_sound("bloom", 0.6)
            self.say([
                "Petals open into a ring of light. Five points pulse around it.",
                "It wants me to complete the circle. To finish the bloom.",
                "Touch each light, in turn. Let it in.",
            ], "the flower")

    def _ritual_click(self, pos):
        """Return True if a node was clicked."""
        for i, node in enumerate(self.nodes):
            nx, ny, lit = node
            if lit:
                continue
            if math.hypot(pos[0] - nx, pos[1] - ny) < 44:
                if i == self.next_node:
                    node[2] = True
                    self.next_node += 1
                    self.assets.play_sound("glow", 0.7)
                    self.assets.play_sound("whisper_layered", 0.4)
                    self.particles.emit(nx, ny, 30, col=S.SPORE, speed=80,
                                        life=(0.5, 1.2))
                    self.ctx.sanity.change(-6)
                    if self.next_node >= len(self.nodes):
                        self._begin_bloom()
                else:
                    # wrong order: a jolt
                    self.assets.play_sound("denied", 0.5)
                    self.ctx.sanity.change(-3)
                return True
        return False

    def _begin_bloom(self):
        self.phase = self.BLOOM
        self.complete("Complete the ritual")
        self.bloom_t = 0.0
        self.assets.play_sound("spore_burst", 0.9)
        self.particles.burst(*self.center, count=220, col=S.SPORE)
        self.ctx.journal.add(
            "Final entry: I understand now. The previous caretakers did not "
            "vanish. They bloomed. As I will. As the next one will.")
        self.say([
            "The petals close around me. There is no fear. Only pollen, and warmth.",
            "I am not being eaten. I am being planted.",
            "...Let me bloom.",
        ], "Elias")

    # --- input -------------------------------------------------------------
    def handle_event(self, e):
        if (self.phase == self.RITUAL and not self.ctx.textbox.active
                and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1):
            if self._ritual_click(e.pos):
                return
        super().handle_event(e)

    # --- per-frame ---------------------------------------------------------
    def update_scene(self, dt):
        self.whisper_t += dt
        self.root_grow = min(1.0, self.root_grow + dt * 0.15)

        if self.phase == self.INTRO:
            self.flower_scale = min(1.0, self.flower_scale + dt * 0.25)
        if self.whisper_t > 4.0:
            self.whisper_t = 0.0
            self.assets.play_sound("whisper_layered", 0.5)

        if self.phase == self.BLOOM:
            self.bloom_t += dt
            # Continuous spore drift during transformation.
            self.particles.emit(*self.center, 3, col=S.SPORE, speed=40,
                                life=(1.0, 2.0))
            # After the transformation plays out, go to the ending.
            if self.bloom_t > 6.0 and not self.ctx.fade.busy:
                from scenes.ending import EndingScene
                self.phase = self.DONE
                self.go_to(EndingScene)

    def draw_scene(self, surf):
        # Animated roots growing up the chamber walls.
        self._draw_growing_roots(surf)

        # The giant flower, scaling/breathing.
        base = 360
        breathe = 1.0 + 0.04 * math.sin(self.time * 2)
        size = int(base * self.flower_scale * breathe)
        if self.phase == self.BLOOM:
            # swells open during the bloom
            size = int(base * (1.0 + self.bloom_t * 0.18))
        flower = self.assets.sprite("giant_flower", (size, size))
        surf.blit(flower, (self.center[0] - size // 2,
                           self.center[1] - size // 2))

        # Red heart-pulse glow.
        fx.glow(surf, self.center, int(size * 0.7), S.BLOOD,
                intensity=70 + int(40 * math.sin(self.time * 2)))

        # Ritual nodes.
        if self.phase == self.RITUAL:
            for i, (nx, ny, lit) in enumerate(self.nodes):
                if lit:
                    fx.glow(surf, (nx, ny), 40, S.POLLEN, intensity=140)
                    pygame.draw.circle(surf, S.WHITE, (int(nx), int(ny)), 12)
                else:
                    pulse = 0.5 + 0.5 * math.sin(self.time * 4 + i)
                    col = S.GOLD if i == self.next_node else S.DIM
                    pygame.draw.circle(surf, col, (int(nx), int(ny)),
                                       int(10 + 6 * pulse), 3)

        # White-out flash at the climax of the bloom.
        if self.phase == self.BLOOM and self.bloom_t > 4.0:
            a = int(min(255, (self.bloom_t - 4.0) * 130))
            flash = pygame.Surface((S.WIDTH, S.HEIGHT))
            flash.fill((255, 240, 245))
            flash.set_alpha(a)
            surf.blit(flash, (0, 0))

    def _draw_growing_roots(self, surf):
        root = self.assets.sprite("root", (260, 140))
        rows = int(self.root_grow * 4) + 1
        for row in range(rows):
            y = S.HEIGHT - 80 - row * 90
            for i, x in enumerate(range(-60, S.WIDTH, 230)):
                r = root.copy()
                wobble = math.sin(self.time + i + row) * 10
                r.set_alpha(160)
                surf.blit(r, (x + wobble, y))

    # Full-frame heat pulse + distortion for the finale.
    def draw(self, surf):
        amt = max(self.ctx.sanity.distortion_amount, 0.3)
        temp = surf.copy()
        super().draw(temp)
        if amt > 0:
            temp = fx.distortion(temp, min(amt, 0.6))
        surf.blit(temp, (0, 0))
        fx.heat_pulse(surf, self.time, colour=S.BLOOD, base=14, amp=24)
        fx.vignette(surf, strength=170)
