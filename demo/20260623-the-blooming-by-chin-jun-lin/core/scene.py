"""
core/scene.py
=============
The point-and-click framework.

  Hotspot   - a clickable region on the screen with a name, a cursor label,
              and an on_click handler. Supports "use item on hotspot".
  Scene     - base class every scene inherits. Owns its hotspots, particles,
              background name, music, and objective list.
  GameContext - the shared bundle (assets + inventory + journal + sanity +
                textbox + fade) passed to every scene so state persists.
  SceneManager - swaps scenes with a fade transition.
"""

import pygame

import settings as S
from core import fx, ui
from core.systems import Inventory, Journal, Sanity


class Hotspot:
    def __init__(self, rect, name, on_click=None, *, label=None,
                 requires_item=None, visible=True, cursor="look"):
        self.rect = pygame.Rect(rect)
        self.name = name
        self.label = label if label is not None else name
        self.on_click = on_click
        self.requires_item = requires_item   # item id needed to interact
        self.visible = visible               # if False, ignored + not drawn
        self.cursor = cursor                 # "look" / "take" / "use" / "go"
        self.enabled = True

    def hit(self, pos):
        return self.enabled and self.visible and self.rect.collidepoint(pos)


class GameContext:
    """Everything that must survive between scenes lives here."""

    def __init__(self, assets):
        self.assets = assets
        self.inventory = Inventory(assets)
        self.journal = Journal(assets)
        self.sanity = Sanity(assets)
        self.textbox = ui.TextBox(assets)
        self.hover = ui.HoverLabel(assets)
        self.fade = ui.Fade()
        self.flags = {}          # arbitrary story flags shared across scenes
        self.manager = None      # set by SceneManager


class Scene:
    background_name = None
    music_name = None
    sanity_drain = 0.0

    def __init__(self, ctx):
        self.ctx = ctx
        self.assets = ctx.assets
        self.hotspots = []
        self.particles = fx.ParticleSystem()
        self.time = 0.0
        self.title = ""
        self.title_timer = 3.0   # seconds the scene title card stays up
        self.objectives = {}     # label -> bool(done)
        self.setup()

    # ---- override these in subclasses -------------------------------------
    def setup(self):
        """Create hotspots, set objectives, queue intro narration."""

    def on_enter(self):
        """Called when the scene becomes active (after fade-in)."""
        if self.background_name:
            self.assets.background(self.background_name)  # warm the cache
        if self.music_name:
            self.assets.play_music(self.music_name)
        self.ctx.sanity.set_drain(self.sanity_drain)

    def update_scene(self, dt):
        """Per-frame scene logic (particles, timers, triggers)."""

    def draw_scene(self, surf):
        """Draw scene-specific layers above the background, below the UI."""

    # ---- shared helpers ---------------------------------------------------
    def add_objective(self, label):
        self.objectives[label] = False

    def complete(self, label):
        if label in self.objectives and not self.objectives[label]:
            self.objectives[label] = True

    def all_done(self):
        return self.objectives and all(self.objectives.values())

    def go_to(self, scene_factory):
        self.ctx.manager.change(scene_factory)

    def say(self, text, speaker=""):
        self.ctx.textbox.show(text, speaker)

    # ---- input ------------------------------------------------------------
    def handle_event(self, e):
        ctx = self.ctx
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_j:
                ctx.journal.toggle()
                return
            if e.key in (pygame.K_SPACE, pygame.K_RETURN):
                ctx.textbox.advance()
                return
        if ctx.journal.open:
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            # Dialogue eats the click first.
            if ctx.textbox.active:
                ctx.textbox.advance()
                return
            # Inventory bar.
            if ctx.inventory.handle_click(e.pos):
                return
            # Hotspots (topmost last drawn wins -> iterate reversed).
            for hs in reversed(self.hotspots):
                if hs.hit(e.pos):
                    self._click_hotspot(hs)
                    return

    def _click_hotspot(self, hs):
        ctx = self.ctx
        sel = ctx.inventory.selected
        if hs.requires_item and sel != hs.requires_item:
            if hs.requires_item and sel is None:
                self.say("I should examine this... maybe I need something first.",
                         "Elias")
            else:
                self.assets.play_sound("denied", 0.5)
            if hs.on_click:
                hs.on_click(used_item=sel)   # let handler decide anyway
            return
        if hs.on_click:
            hs.on_click(used_item=sel)

    # ---- main loop hooks --------------------------------------------------
    def update(self, dt):
        self.time += dt
        if self.title_timer > 0:
            self.title_timer -= dt
        self.ctx.textbox.update(dt)
        self.ctx.sanity.update(dt)
        self.particles.update(dt)
        self.update_scene(dt)

    def _hovered(self, mouse_pos):
        if self.ctx.journal.open or self.ctx.textbox.active:
            return None
        for hs in reversed(self.hotspots):
            if hs.hit(mouse_pos):
                return hs
        return None

    def draw(self, surf):
        ctx = self.ctx
        surf.blit(self.assets.background(self.background_name), (0, 0))
        self.draw_scene(surf)
        self.particles.draw(surf)

        # Scene title card.
        if self.title and self.title_timer > 0:
            a = min(255, int(self.title_timer * 160))
            f = self.assets.font(56)
            t = f.render(self.title, True, S.WHITE)
            t.set_alpha(a)
            surf.blit(t, (S.WIDTH // 2 - t.get_width() // 2, 120))

        # Objectives tracker (top-left).
        self._draw_objectives(surf)

        # UI layers.
        ctx.inventory.draw(surf)
        ctx.sanity.draw(surf)
        hs = self._hovered(pygame.mouse.get_pos())
        ctx.hover.draw(surf, hs.label if hs else "", pygame.mouse.get_pos())
        ctx.textbox.draw(surf)
        ctx.journal.draw(surf)

    def _draw_objectives(self, surf):
        if not self.objectives:
            return
        f = self.assets.font(22)
        x, y = 30, 24
        surf.blit(f.render("Objectives", True, S.GOLD), (x, y))
        y += 30
        for label, done in self.objectives.items():
            mark = "x" if done else "o"
            col = S.DIM if done else S.WHITE
            surf.blit(f.render(f"[{mark}] {label}", True, col), (x, y))
            y += 26


class SceneManager:
    def __init__(self, ctx):
        self.ctx = ctx
        ctx.manager = self
        self.current = None
        self._pending = None

    def change(self, scene_factory):
        """Fade to black, swap scene, fade back in."""
        def swap():
            self.current = scene_factory(self.ctx)
            self.current.on_enter()
            self.ctx.fade.to_clear()
        self.ctx.fade.to_black(swap)

    def start(self, scene_factory):
        self.current = scene_factory(self.ctx)
        self.current.on_enter()

    def handle_event(self, e):
        if self.ctx.fade.busy:
            return
        if self.current:
            self.current.handle_event(e)

    def update(self, dt):
        self.ctx.fade.update(dt)
        if self.current:
            self.current.update(dt)

    def draw(self, surf):
        if self.current:
            self.current.draw(surf)
        self.ctx.fade.draw(surf)
