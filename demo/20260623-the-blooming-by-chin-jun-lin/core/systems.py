"""
core/systems.py
===============
The three persistent gameplay systems carried across scenes:

  Inventory - items the player has picked up; one can be "selected" and then
              used on a hotspot (classic point-and-click verb: USE item ON x)
  Journal   - Elias' notes / clues, toggled with the J key or button
  Sanity    - mental condition meter. Drains in the later scenes; low values
              feed the distortion + hallucination effects in core/fx.py
"""

import pygame
import settings as S


class Inventory:
    def __init__(self, assets):
        self.assets = assets
        self.items = []           # list of dicts: {id, name, sprite}
        self.selected = None      # id of currently selected item
        self.slot = 78
        self.pad = 12

    def add(self, item_id, name, sprite_name=None):
        if any(i["id"] == item_id for i in self.items):
            return
        self.items.append({"id": item_id, "name": name,
                           "sprite": sprite_name or item_id})
        self.assets.play_sound("pickup", 0.6)

    def has(self, item_id):
        return any(i["id"] == item_id for i in self.items)

    def remove(self, item_id):
        self.items = [i for i in self.items if i["id"] != item_id]
        if self.selected == item_id:
            self.selected = None

    def rects(self):
        """Yield (item, rect) for hit-testing the bottom-left item bar."""
        x = 30
        y = S.HEIGHT - self.slot - 16
        for it in self.items:
            yield it, pygame.Rect(x, y, self.slot, self.slot)
            x += self.slot + self.pad

    def handle_click(self, pos):
        for it, r in self.rects():
            if r.collidepoint(pos):
                self.selected = None if self.selected == it["id"] else it["id"]
                self.assets.play_sound("click", 0.4)
                return True
        return False

    def draw(self, surf):
        for it, r in self.rects():
            sel = (self.selected == it["id"])
            bg = pygame.Surface((self.slot, self.slot), pygame.SRCALPHA)
            bg.fill((20, 24, 22, 220))
            surf.blit(bg, r.topleft)
            border = S.GOLD if sel else S.UI_LINE
            pygame.draw.rect(surf, border, r, 2)
            spr = self.assets.sprite(it["sprite"], (self.slot - 16, self.slot - 16))
            surf.blit(spr, (r.x + 8, r.y + 8))


class Journal:
    def __init__(self, assets):
        self.assets = assets
        self.entries = []
        self.open = False
        self.title_font = assets.font(40)
        self.font = assets.font(26)
        self.new_flag = False

    def add(self, text):
        if text not in self.entries:
            self.entries.append(text)
            self.new_flag = True

    def toggle(self):
        self.open = not self.open
        if self.open:
            self.new_flag = False
        self.assets.play_sound("click", 0.4)

    def draw(self, surf):
        if not self.open:
            return
        from core.ui import wrap_text
        w, h = surf.get_size()
        panel = pygame.Surface((w - 200, h - 160), pygame.SRCALPHA)
        panel.fill((10, 12, 12, 240))
        pygame.draw.rect(panel, S.UI_LINE, panel.get_rect(), 2)
        surf.blit(panel, (100, 80))

        surf.blit(self.title_font.render("Journal", True, S.GOLD), (140, 110))
        y = 180
        if not self.entries:
            surf.blit(self.font.render("(empty)", True, S.DIM), (140, y))
        for e in self.entries:
            for line in wrap_text("- " + e, self.font, w - 320):
                surf.blit(self.font.render(line, True, S.WHITE), (140, y))
                y += 32
            y += 10
        hint = self.font.render("press J to close", True, S.DIM)
        surf.blit(hint, (w - 100 - hint.get_width(), h - 110))


class Sanity:
    def __init__(self, assets):
        self.assets = assets
        self.value = S.SANITY_START
        self.font = assets.font(22)
        self.drain = 0.0          # per-second drain set by each scene
        self._beat_timer = 0.0

    def set_drain(self, rate):
        self.drain = rate

    def change(self, amount):
        self.value = max(0, min(S.SANITY_MAX, self.value + amount))

    @property
    def fraction(self):
        return self.value / S.SANITY_MAX

    @property
    def hallucinating(self):
        return self.value < S.SANITY_HALLUCINATION_THRESHOLD

    @property
    def distortion_amount(self):
        """0 above threshold, ramping to 1 as sanity approaches 0."""
        thr = S.SANITY_HALLUCINATION_THRESHOLD
        if self.value >= thr:
            return 0.0
        return min(1.0, (thr - self.value) / thr)

    def update(self, dt):
        if self.drain:
            self.change(-self.drain * dt)
        # Heartbeat speeds up as sanity falls.
        if self.hallucinating:
            interval = 0.5 + 1.2 * self.fraction
            self._beat_timer += dt
            if self._beat_timer >= interval:
                self._beat_timer = 0.0
                self.assets.play_sound("heartbeat", 0.5 + 0.5 * (1 - self.fraction))

    def draw(self, surf):
        x, y = S.WIDTH - 250, 24
        surf.blit(self.font.render("SANITY", True, S.WHITE), (x, y - 4))
        bar = pygame.Rect(x, y + 22, 210, 16)
        pygame.draw.rect(surf, (40, 40, 40), bar)
        frac = self.fraction
        col = (int(200 * (1 - frac) + 60), int(180 * frac + 20), 60)
        pygame.draw.rect(surf, col, (bar.x, bar.y, int(bar.w * frac), bar.h))
        pygame.draw.rect(surf, S.UI_LINE, bar, 2)
