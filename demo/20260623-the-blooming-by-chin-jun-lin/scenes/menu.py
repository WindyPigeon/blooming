"""
scenes/menu.py  -  Main menu / title screen.
"""

import pygame

import settings as S
from core import fx
from core.scene import Scene
from core.ui import Button


class MenuScene(Scene):
    background_name = "menu"
    music_name = "menu"

    def setup(self):
        cx = S.WIDTH // 2
        # Imported lazily inside callbacks to avoid circular imports.
        from scenes.arrival import ArrivalScene

        self.buttons = [
            Button("Begin", (cx, 420), self.assets, 44,
                   callback=lambda: self.go_to(ArrivalScene)),
            Button("Quit", (cx, 490), self.assets, 36,
                   callback=self._quit),
        ]
        self.title_font = self.assets.font(96)
        self.sub_font = self.assets.font(30)

    def _quit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for b in self.buttons:
                if b.handle_click(e.pos):
                    return

    def update_scene(self, dt):
        # Drifting spores over the title for atmosphere.
        self.particles.ambient_pollen(
            dt, pygame.Rect(0, 0, S.WIDTH, S.HEIGHT),
            density=0.5, col=S.SPORE)
        for b in self.buttons:
            b.update(pygame.mouse.get_pos())

    def draw_scene(self, surf):
        # Darken for legibility.
        veil = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 110))
        surf.blit(veil, (0, 0))

        title = self.title_font.render("THE BLOOMING", True, S.WHITE)
        surf.blit(title, (S.WIDTH // 2 - title.get_width() // 2, 210))
        sub = self.sub_font.render(
            "a flora-themed psychological horror", True, S.GOLD)
        surf.blit(sub, (S.WIDTH // 2 - sub.get_width() // 2, 320))

        for b in self.buttons:
            b.draw(surf)

        hint = self.sub_font.render(
            "J = journal   |   click items, then click where to use them",
            True, S.DIM)
        surf.blit(hint, (S.WIDTH // 2 - hint.get_width() // 2, S.HEIGHT - 60))

    # Menu has no hotspots/objectives/UI bars; override draw to keep it clean.
    def draw(self, surf):
        surf.blit(self.assets.background(self.background_name), (0, 0))
        self.draw_scene(surf)
        self.particles.draw(surf)
        fx.vignette(surf, strength=160)
