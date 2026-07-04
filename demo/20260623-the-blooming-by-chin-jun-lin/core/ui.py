"""
core/ui.py
==========
Reusable interface pieces used across every scene:

  TextBox   - bottom narration / dialogue box with typewriter reveal
  Button    - simple clickable text button (menus)
  HoverLabel- floating label that shows the name of the hotspot under cursor
  Fade      - full-screen fade in/out for scene transitions
  wrap_text - helper to word-wrap a string to a width
"""

import pygame
import settings as S


def wrap_text(text, font, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class TextBox:
    """Bottom-of-screen narration box with a typewriter effect.

    Call show(text). Click or press space advances / closes.
    """

    def __init__(self, assets):
        self.assets = assets
        self.font = assets.font(26)
        self.name_font = assets.font(22)
        self.queue = []
        self.text = ""
        self.speaker = ""
        self.revealed = 0.0
        self.active = False
        self.speed = 45  # chars per second

    def show(self, text, speaker=""):
        """Queue one or more lines. text can be a str or list of str."""
        items = text if isinstance(text, list) else [text]
        for it in items:
            self.queue.append((it, speaker))
        if not self.active:
            self._next()

    def _next(self):
        if self.queue:
            self.text, self.speaker = self.queue.pop(0)
            self.revealed = 0.0
            self.active = True
        else:
            self.active = False
            self.text = ""

    def advance(self):
        """Player clicked/space: finish reveal, or go to next line."""
        if not self.active:
            return False
        if self.revealed < len(self.text):
            self.revealed = len(self.text)
        else:
            self._next()
        return True

    def update(self, dt):
        if self.active and self.revealed < len(self.text):
            self.revealed = min(len(self.text), self.revealed + self.speed * dt)

    def draw(self, surf):
        if not self.active:
            return
        w, h = surf.get_size()
        box_h = 170
        box = pygame.Surface((w - 80, box_h), pygame.SRCALPHA)
        box.fill((*S.UI_BG, 225))
        pygame.draw.rect(box, (*S.UI_LINE, 255), box.get_rect(), 2)
        surf.blit(box, (40, h - box_h - 30))

        x, y = 70, h - box_h - 10
        if self.speaker:
            name = self.name_font.render(self.speaker, True, S.GOLD)
            surf.blit(name, (x, y))
            y += 32
        shown = self.text[:int(self.revealed)]
        for line in wrap_text(shown, self.font, w - 160):
            surf.blit(self.font.render(line, True, S.WHITE), (x, y))
            y += 32

        if not self.queue and self.revealed >= len(self.text):
            hint = self.name_font.render("click to continue", True, S.DIM)
            surf.blit(hint, (w - 70 - hint.get_width(), h - 60))


class Button:
    def __init__(self, text, center, assets, size=40, callback=None):
        self.assets = assets
        self.text = text
        self.font = assets.font(size)
        self.callback = callback
        self.center = center
        self.hover = False
        self._render()

    def _render(self):
        col = S.GOLD if self.hover else S.WHITE
        self.surf = self.font.render(self.text, True, col)
        self.rect = self.surf.get_rect(center=self.center)

    def update(self, mouse_pos):
        h = self.rect.collidepoint(mouse_pos)
        if h != self.hover:
            self.hover = h
            self._render()

    def handle_click(self, pos):
        if self.rect.collidepoint(pos) and self.callback:
            self.assets.play_sound("click", 0.5)
            self.callback()
            return True
        return False

    def draw(self, surf):
        if self.hover:
            pad = self.rect.inflate(40, 16)
            glow = pygame.Surface(pad.size, pygame.SRCALPHA)
            glow.fill((*S.GOLD, 25))
            surf.blit(glow, pad.topleft)
        surf.blit(self.surf, self.rect)


class HoverLabel:
    """Shows the display name of whatever hotspot the cursor is over."""

    def __init__(self, assets):
        self.font = assets.font(22)

    def draw(self, surf, text, pos):
        if not text:
            return
        label = self.font.render(text, True, S.WHITE)
        pad = 8
        bg = pygame.Surface((label.get_width() + pad * 2,
                             label.get_height() + pad * 2), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 200))
        x, y = pos[0] + 18, pos[1] + 18
        surf.blit(bg, (x, y))
        surf.blit(label, (x + pad, y + pad))


class Fade:
    """Full-screen fade. Drive with update(dt); draw() over everything."""

    def __init__(self):
        self.alpha = 0
        self.target = 0
        self.speed = 320  # alpha per second
        self._cb = None

    def to_black(self, callback=None):
        self.target = 255
        self._cb = callback

    def to_clear(self, callback=None):
        self.target = 0
        self._cb = callback

    def update(self, dt):
        if self.alpha < self.target:
            self.alpha = min(self.target, self.alpha + self.speed * dt)
        elif self.alpha > self.target:
            self.alpha = max(self.target, self.alpha - self.speed * dt)
        if self.alpha == self.target and self._cb:
            cb, self._cb = self._cb, None
            cb()

    @property
    def busy(self):
        return self.alpha != self.target

    def draw(self, surf):
        if self.alpha > 0:
            s = pygame.Surface(surf.get_size())
            s.fill((0, 0, 0))
            s.set_alpha(int(self.alpha))
            surf.blit(s, (0, 0))
