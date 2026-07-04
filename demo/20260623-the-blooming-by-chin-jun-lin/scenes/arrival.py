"""
scenes/arrival.py  -  SCENE 1: ARRIVAL
======================================
Environment : Research Greenhouse (day)
Objectives  : inspect the equipment, find the watering can, water the plant
Key events  : plant glows after watering, first whisper, journal unlocked
Effects     : floating pollen particles, petal glow, ambient greenhouse audio
Mechanics introduced: look, take, USE item ON target, inventory, journal
"""

import pygame

import settings as S
from core import fx
from core.scene import Scene, Hotspot


class ArrivalScene(Scene):
    background_name = "greenhouse"
    music_name = "greenhouse"
    sanity_drain = 0.0

    def setup(self):
        self.title = "I  -  Arrival"
        self.add_objective("Inspect the equipment")
        self.add_objective("Find the watering can")
        self.add_objective("Water the plant")

        self.watered = False
        self.plant_pos = (S.WIDTH // 2, int(S.HEIGHT * 0.52))
        self.glow_t = 0.0

        # --- Hotspots ------------------------------------------------------
        self.hs_equipment = Hotspot(
            (120, 360, 220, 220), "Lab equipment",
            on_click=self._inspect_equipment, cursor="look")
        self.hs_can = Hotspot(
            (940, 470, 110, 150), "Watering can",
            on_click=self._take_can, cursor="take")
        self.hs_plant = Hotspot(
            (self.plant_pos[0] - 90, self.plant_pos[1] - 90, 180, 200),
            "The flower", on_click=self._use_on_plant, cursor="use")
        self.hs_door = Hotspot(
            (S.WIDTH - 150, 200, 130, 360), "Greenhouse door",
            on_click=self._try_door, cursor="go", visible=False)

        self.hotspots = [self.hs_equipment, self.hs_can,
                         self.hs_plant, self.hs_door]

        self.say([
            "Day one. They left the key under a rock, of all things.",
            "My job is simple: keep the new specimen alive until the seniors return.",
            "A flower from an uncharted forest. How hard can it be?",
        ], "Elias")

    # --- hotspot handlers --------------------------------------------------
    def _inspect_equipment(self, used_item=None):
        self.complete("Inspect the equipment")
        self.ctx.journal.add(
            "Greenhouse log: specimen requires daily watering. "
            "Caretaker rotation handled by previous staff (names redacted).")
        self.say([
            "Watering schedules, soil charts... and a redacted staff roster.",
            "Every previous caretaker's name is blacked out. Strange.",
        ], "Elias")

    def _take_can(self, used_item=None):
        if not self.ctx.inventory.has("watering_can"):
            self.ctx.inventory.add("watering_can", "Watering Can", "watering_can")
            self.complete("Find the watering can")
            self.hs_can.enabled = False
            self.say("A watering can, still half full. This will do.", "Elias")

    def _use_on_plant(self, used_item=None):
        if self.watered:
            self.say("It pulses softly, as if it is breathing.", "Elias")
            return
        if used_item == "watering_can":
            self.watered = True
            self.complete("Water the plant")
            self.assets.play_sound("water", 0.7)
            self.ctx.inventory.selected = None
            # First supernatural beat.
            pygame.time.set_timer(pygame.USEREVENT + 1, 1400, loops=1)
            self.say([
                "The water sinks in instantly. The petals brighten...",
                "...did it just lean toward me?",
            ], "Elias")
        else:
            self.say("A pale, beautiful flower. I shouldn't touch it bare-handed.",
                     "Elias")

    def _try_door(self, used_item=None):
        from scenes.whispering import WhisperingScene
        self.assets.play_sound("door", 0.6)
        self.go_to(WhisperingScene)

    # --- per-frame ---------------------------------------------------------
    def handle_event(self, e):
        super().handle_event(e)
        if e.type == pygame.USEREVENT + 1:
            # The first whisper + journal unlock, a beat after watering.
            self.assets.play_sound("whisper", 0.7)
            self.ctx.journal.add(
                "I heard a whisper near the flower. No one else is here. "
                "I must be more tired than I thought.")
            self.say([
                "...elias...",
                "Who said that? ...There's no one here.",
                "I should rest. The door to the wing is just there.",
            ], "the flower")

    def update_scene(self, dt):
        # Ambient pollen across the upper greenhouse.
        self.particles.ambient_pollen(
            dt, pygame.Rect(0, 80, S.WIDTH, 320), density=0.7, col=S.POLLEN)
        if self.watered:
            self.glow_t += dt
            # Occasional pollen puff from the plant.
            if pygame.time.get_ticks() % 6 < 1:
                self.particles.emit(*self.plant_pos, 2, col=S.POLLEN,
                                    speed=12, life=(1.0, 2.0))
            # Reveal the exit once watered.
            self.hs_door.visible = True

        if self.all_done() and self.watered:
            self.complete("Water the plant")

    def draw_scene(self, surf):
        # Draw the watering can sprite (if not taken).
        if self.hs_can.enabled:
            can = self.assets.sprite("watering_can", (90, 120))
            surf.blit(can, (950, 480))

        # Draw the plant; glowing once watered.
        sprite_name = "plant_glow" if self.watered else "plant"
        plant = self.assets.sprite(sprite_name, (180, 200))
        if self.watered:
            pulse = 200 + int(40 * abs(pygame.math.Vector2(1, 0)
                              .rotate(self.glow_t * 120).x))
            fx.glow(surf, self.plant_pos, 130, S.POLLEN, intensity=pulse % 160 + 40)
        surf.blit(plant, (self.plant_pos[0] - 90, self.plant_pos[1] - 100))

        # Hint arrow / shimmer on the door once available.
        if self.hs_door.visible:
            f = self.assets.font(24)
            t = f.render("-> exit", True, S.GOLD)
            surf.blit(t, (S.WIDTH - 150, 170))
