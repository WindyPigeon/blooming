"""
core/assets.py
==============
The AssetManager loads images, fonts and audio by logical name.

THE IMPORTANT IDEA:
  - If the real file exists in assets/<folder>/, it is loaded and used.
  - If it is missing, a procedural PLACEHOLDER is generated so the game
    never crashes for a missing asset, and a one-line note is printed
    telling you exactly which file to add.

That means you (the artist) can keep working in parallel with the code:
just drop correctly named files into the assets/ folders and re-run.
"""

import os
import math
import random
import pygame

import settings as S


class AssetManager:
    def __init__(self):
        self.images = {}      # cache: name -> Surface
        self.sounds = {}      # cache: name -> Sound (or None)
        self.fonts = {}       # cache: (name, size) -> Font
        self.current_music = None
        self.missing = []     # list of (kind, expected_path) for the report
        self.audio_ok = pygame.mixer.get_init() is not None

    # ---- path helpers -----------------------------------------------------
    def _find(self, folder, filename, exts):
        """Return the first existing path for filename, trying each extension."""
        base = os.path.join(S.ASSET_ROOT, folder, filename)
        if os.path.isfile(base):
            return base
        stem, _ = os.path.splitext(base)
        for ext in exts:
            cand = stem + ext
            if os.path.isfile(cand):
                return cand
        return None

    def _note_missing(self, kind, folder, filename):
        path = os.path.join(S.ASSET_ROOT, folder, filename)
        if path in [m[1] for m in self.missing]:
            return  # only report each missing asset once
        self.missing.append((kind, path))
        print(f"  [placeholder] {kind:10s} -> add your file at: {path}")

    # ====================================================================
    #  IMAGES
    # ====================================================================
    def background(self, name):
        """Full-screen background by logical name (see settings.BACKGROUNDS)."""
        key = f"bg::{name}"
        if key in self.images:
            return self.images[key]
        filename = S.BACKGROUNDS.get(name, name)
        path = self._find(S.DIR_BACKGROUNDS, filename, S.IMAGE_EXTS)
        if path:
            img = pygame.image.load(path).convert()
            img = pygame.transform.smoothscale(img, (S.WIDTH, S.HEIGHT))
        else:
            self._note_missing("background", S.DIR_BACKGROUNDS, filename)
            img = self._placeholder_background(name)
        self.images[key] = img
        return img

    def sprite(self, name, size=None):
        """Sprite by logical name (see settings.SPRITES). Optional (w,h) scale.

        The base (unscaled) image is cached by name only, so animated sprites
        that change size every frame don't regenerate the placeholder each
        time -- they just rescale the cached base.
        """
        base = self._sprite_base(name)
        if size and size != base.get_size():
            return pygame.transform.smoothscale(base, size)
        return base

    def _sprite_base(self, name):
        key = f"sp::{name}"
        if key in self.images:
            return self.images[key]
        filename = S.SPRITES.get(name, name)
        path = self._find(S.DIR_SPRITES, filename, S.IMAGE_EXTS)
        if path:
            img = pygame.image.load(path).convert_alpha()
        else:
            self._note_missing("sprite", S.DIR_SPRITES, filename)
            img = self._placeholder_sprite(name)
        self.images[key] = img
        return img

    # ====================================================================
    #  FONTS
    # ====================================================================
    def font(self, size):
        key = ("main", size)
        if key in self.fonts:
            return self.fonts[key]
        path = self._find(S.DIR_FONTS, S.FONT_MAIN, (".ttf", ".otf"))
        try:
            f = pygame.font.Font(path, size) if path else pygame.font.SysFont(
                "georgia,timesnewroman,serif", size)
        except Exception:
            f = pygame.font.SysFont(None, size)
        self.fonts[key] = f
        return f

    # ====================================================================
    #  AUDIO
    # ====================================================================
    def sound(self, name):
        """Sound effect by logical name. Returns a Sound or None (silent)."""
        if not self.audio_ok:
            return None
        if name in self.sounds:
            return self.sounds[name]
        filename = S.SOUNDS.get(name, name)
        path = self._find(S.DIR_SOUNDS, filename, S.AUDIO_EXTS)
        snd = None
        if path:
            try:
                snd = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"  [audio] could not load {path}: {e}")
        else:
            # Try to synthesise a simple stand-in so effects are still audible.
            snd = self._synth_sound(name)
            if snd is None:
                self._note_missing("sound", S.DIR_SOUNDS, filename)
        self.sounds[name] = snd
        return snd

    def play_sound(self, name, volume=1.0):
        snd = self.sound(name)
        if snd:
            snd.set_volume(volume)
            snd.play()

    def play_music(self, name, volume=0.5, loop=True):
        """Stream looping background music by logical name."""
        if not self.audio_ok:
            return
        if self.current_music == name:
            return
        filename = S.MUSIC.get(name, name)
        path = self._find(S.DIR_MUSIC, filename, S.AUDIO_EXTS)
        if not path:
            self._note_missing("music", S.DIR_MUSIC, filename)
            pygame.mixer.music.stop()
            self.current_music = name
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = name
        except Exception as e:
            print(f"  [music] could not play {path}: {e}")

    def stop_music(self):
        if self.audio_ok:
            pygame.mixer.music.fadeout(600)
        self.current_music = None

    # ====================================================================
    #  PROCEDURAL PLACEHOLDERS
    #  (everything below only runs when a real asset is missing)
    # ====================================================================
    def _placeholder_background(self, name):
        surf = pygame.Surface((S.WIDTH, S.HEIGHT)).convert()
        # Pick a mood tint per scene.
        top, bottom = {
            "menu":             ((8, 14, 12), (2, 4, 3)),
            "greenhouse":       ((30, 70, 50), (10, 28, 20)),
            "greenhouse_night": ((10, 20, 30), (3, 7, 12)),
            "facility":         ((30, 18, 18), (8, 5, 6)),
            "heart_chamber":    ((70, 10, 22), (15, 2, 6)),
            "ending":           ((20, 35, 28), (5, 10, 8)),
        }.get(name, ((25, 30, 30), (5, 8, 8)))
        # Vertical gradient.
        for y in range(S.HEIGHT):
            t = y / S.HEIGHT
            col = [int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)]
            pygame.draw.line(surf, col, (0, y), (S.WIDTH, y))
        # Suggest a horizon / floor and a few vertical "structures".
        rng = random.Random(hash(name) & 0xFFFF)
        for _ in range(14):
            x = rng.randint(0, S.WIDTH)
            w = rng.randint(30, 90)
            h = rng.randint(120, S.HEIGHT)
            shade = rng.randint(-18, 18)
            col = [max(0, min(255, bottom[i] + shade + 10)) for i in range(3)]
            r = pygame.Rect(x, S.HEIGHT - h, w, h)
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((*col, 60))
            surf.blit(s, r.topleft)
        # Floor line.
        pygame.draw.line(surf, (0, 0, 0), (0, int(S.HEIGHT * 0.78)),
                         (S.WIDTH, int(S.HEIGHT * 0.78)), 3)
        # Watermark label so you know which background this stands in for.
        f = self.font(26)
        label = f.render(f"[ placeholder background: {name} ]", True, (180, 180, 180))
        label.set_alpha(120)
        surf.blit(label, (20, 20))
        return surf

    def _placeholder_sprite(self, name):
        # Default size; many call sites rescale anyway.
        if "flower" in name or name == "plant" or name == "plant_glow":
            return self._draw_flower(glow=("glow" in name),
                                     big=("giant" in name))
        if name == "watering_can":
            return self._draw_simple_icon((120, 150, 190), "can")
        if name == "note":
            return self._draw_simple_icon((230, 225, 200), "note")
        if name == "keycard":
            return self._draw_simple_icon((200, 180, 90), "key")
        if name == "root":
            return self._draw_root()
        if name == "shadow_figure":
            return self._draw_shadow_figure()
        if name == "elias_face":
            return self._draw_flower(glow=True, face=True)
        return self._draw_simple_icon((180, 120, 200), name[:4])

    def _draw_flower(self, glow=False, big=False, face=False):
        size = 360 if big else 160
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2
        petal_col = (150, 40, 70) if not glow else (220, 90, 130)
        # Petals.
        petals = 8 if not big else 12
        for i in range(petals):
            ang = (math.tau / petals) * i
            px = cx + math.cos(ang) * size * 0.30
            py = cy + math.sin(ang) * size * 0.30
            pygame.draw.ellipse(
                surf, petal_col,
                (px - size * 0.16, py - size * 0.10, size * 0.32, size * 0.20))
        # Core.
        core = (230, 200, 90) if not face else (210, 180, 160)
        pygame.draw.circle(surf, core, (cx, cy), int(size * 0.18))
        if glow:
            glow_s = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(glow_s, (255, 180, 200, 70), (cx, cy),
                               int(size * 0.42))
            surf.blit(glow_s, (0, 0))
        if face:
            # Two hollow eyes + a thin mouth -> uncanny "Elias' face" hint.
            pygame.draw.circle(surf, (20, 10, 12), (cx - 14, cy - 6), 6)
            pygame.draw.circle(surf, (20, 10, 12), (cx + 14, cy - 6), 6)
            pygame.draw.arc(surf, (20, 10, 12),
                            (cx - 16, cy, 32, 22), math.pi, math.tau, 2)
        # Stem.
        pygame.draw.rect(surf, (40, 90, 50),
                         (cx - 4, cy + size * 0.18, 8, size * 0.30))
        return surf

    def _draw_simple_icon(self, colour, label):
        surf = pygame.Surface((96, 96), pygame.SRCALPHA)
        pygame.draw.rect(surf, (*colour, 235), (8, 8, 80, 80), border_radius=10)
        pygame.draw.rect(surf, (0, 0, 0), (8, 8, 80, 80), 2, border_radius=10)
        f = self.font(20)
        t = f.render(label, True, (10, 10, 10))
        surf.blit(t, (48 - t.get_width() // 2, 48 - t.get_height() // 2))
        return surf

    def _draw_root(self):
        surf = pygame.Surface((220, 120), pygame.SRCALPHA)
        rng = random.Random(7)
        x, y = 0, 60
        pts = [(x, y)]
        while x < 220:
            x += rng.randint(14, 30)
            y = 60 + rng.randint(-26, 26)
            pts.append((x, y))
        if len(pts) > 1:
            pygame.draw.lines(surf, (60, 35, 30), False, pts, 9)
            pygame.draw.lines(surf, (90, 55, 45), False, pts, 4)
        return surf

    def _draw_shadow_figure(self):
        surf = pygame.Surface((140, 320), pygame.SRCALPHA)
        col = (6, 8, 10, 180)
        pygame.draw.ellipse(surf, col, (30, 0, 80, 110))          # head
        pygame.draw.polygon(surf, col, [(20, 110), (120, 110),
                                        (95, 320), (45, 320)])     # body
        return surf

    # ---- tiny synthesised SFX (used only if no audio file is present) -----
    def _synth_sound(self, name):
        """Make a crude stand-in sound with numpy, if numpy + mixer exist."""
        try:
            import numpy as np
        except Exception:
            return None
        init = pygame.mixer.get_init()
        if not init:
            return None
        rate = init[0]
        channels = init[2] if len(init) > 2 else 2

        def to_sound(wave):
            wave = np.clip(wave, -1, 1)
            data = (wave * 32767).astype(np.int16)
            if channels == 2:
                data = np.column_stack((data, data))
            return pygame.sndarray.make_sound(np.ascontiguousarray(data))

        rng = np.random.default_rng(abs(hash(name)) % (2**32))
        if name in ("heartbeat",):
            t = np.linspace(0, 0.5, int(rate * 0.5), False)
            env = np.exp(-t * 18)
            beat = np.sin(2 * np.pi * 55 * t) * env
            t2 = np.linspace(0, 0.5, int(rate * 0.5), False)
            beat2 = np.sin(2 * np.pi * 50 * t2) * np.exp(-t2 * 18) * 0.7
            wave = np.concatenate([beat, np.zeros(int(rate * 0.12)), beat2])
            return to_sound(wave * 0.6)
        if name in ("whisper", "whisper_layered"):
            n = int(rate * 1.2)
            noise = rng.standard_normal(n)
            # crude band-pass via cumulative smoothing
            for _ in range(6):
                noise = np.convolve(noise, np.ones(8) / 8, mode="same")
            env = np.sin(np.linspace(0, np.pi, n))
            return to_sound(noise / (np.max(np.abs(noise)) + 1e-6) * env * 0.35)
        if name in ("root_crack", "door", "spore_burst", "bloom"):
            n = int(rate * 0.4)
            noise = rng.standard_normal(n) * np.exp(-np.linspace(0, 6, n))
            return to_sound(noise * 0.5)
        if name in ("water", "glow", "pickup", "click", "unlock"):
            dur = 0.18
            t = np.linspace(0, dur, int(rate * dur), False)
            freq = {"click": 600, "pickup": 880, "unlock": 520,
                    "glow": 740, "water": 300}.get(name, 660)
            wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 8)
            return to_sound(wave * 0.4)
        if name == "denied":
            t = np.linspace(0, 0.25, int(rate * 0.25), False)
            wave = np.sin(2 * np.pi * 160 * t) * np.exp(-t * 6)
            return to_sound(wave * 0.4)
        return None
