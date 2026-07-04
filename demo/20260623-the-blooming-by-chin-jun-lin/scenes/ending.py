"""
scenes/ending.py  -  ENDING CUTSCENE
====================================
A new caretaker arrives at the facility, while a flower bearing Elias' face
quietly blooms among the greenhouse plants. Returns to the menu at the end.
"""

import pygame

import settings as S
from core import fx
from core.scene import Scene


class EndingScene(Scene):
    background_name = "ending"
    music_name = "greenhouse"   # calm ambience returns -> unsettling

    def setup(self):
        self.lines = [
            ("Weeks later.", ""),
            ("A new caretaker arrives at the isolated facility.", ""),
            ("'They said the last one transferred out. Lucky me -- "
             "quiet posting.'", "New Caretaker"),
            ("Among the greenhouse plants, one flower turns toward her.", ""),
            ("It wears a face she will never recognise.", ""),
            ("It is already whispering her name.", "the flower"),
        ]
        self.idx = 0
        self.face_reveal = 0.0
        self.center = (int(S.WIDTH * 0.62), int(S.HEIGHT * 0.55))
        self._advance()

    def _advance(self):
        if self.idx < len(self.lines):
            text, speaker = self.lines[self.idx]
            self.say(text, speaker)
            self.idx += 1
        else:
            from scenes.menu import MenuScene
            self.assets.play_music("menu")
            self.go_to(MenuScene)

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.ctx.textbox.active:
                if self.ctx.textbox.revealed < len(self.ctx.textbox.text):
                    self.ctx.textbox.advance()
                else:
                    self._advance()
            else:
                self._advance()
            return
        if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_RETURN):
            self._advance()

    def update_scene(self, dt):
        # The face-bearing flower fades in over the second half.
        if self.idx >= 4:
            self.face_reveal = min(1.0, self.face_reveal + dt * 0.4)
        self.particles.ambient_pollen(
            dt, pygame.Rect(0, 100, S.WIDTH, 300), density=0.5, col=S.POLLEN)

    def draw_scene(self, surf):
        if self.face_reveal > 0:
            size = 180
            face = self.assets.sprite("elias_face", (size, size)).copy()
            face.set_alpha(int(255 * self.face_reveal))
            surf.blit(face, (self.center[0] - size // 2,
                             self.center[1] - size // 2))
            fx.glow(surf, self.center, 120, S.POLLEN,
                    intensity=int(70 * self.face_reveal))

    # Ending has no HUD; draw cleanly.
    def draw(self, surf):
        surf.blit(self.assets.background(self.background_name), (0, 0))
        self.draw_scene(surf)
        self.particles.draw(surf)
        fx.vignette(surf, strength=160)
        self.ctx.textbox.draw(surf)
