"""
core/fx.py
==========
Visual special effects, all drawn procedurally so they work with or without
your art:

  ParticleSystem  - floating pollen, spores, root bursts, corruption motes
  vignette()      - dark frame around the screen (horror framing)
  flicker_overlay - random light flicker (Scene 2)
  light_mask()    - darkness with a soft light circle around the cursor
  distortion()    - wavy / chromatic screen shake when sanity is low
  glow()          - additive glow halo around a point (petal glow, auras)
  heat_pulse()    - red breathing pulse for the Heart Chamber
"""

import math
import random
import pygame

import settings as S


# ---------------------------------------------------------------------------
#  PARTICLES
# ---------------------------------------------------------------------------
class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "size", "col", "grav")

    def __init__(self, x, y, vx, vy, life, size, col, grav=0.0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = self.max_life = life
        self.size = size
        self.col = col
        self.grav = grav

    def update(self, dt):
        self.vy += self.grav * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        a = max(0, min(255, int(255 * (self.life / self.max_life))))
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.col, a), (self.size, self.size), self.size)
        surf.blit(s, (self.x - self.size, self.y - self.size),
                  special_flags=pygame.BLEND_PREMULTIPLIED if False else 0)


class ParticleSystem:
    """A reusable emitter. Configure it per scene for pollen / spores / etc."""

    def __init__(self):
        self.particles = []

    def emit(self, x, y, count, *, spread=40, speed=20, up=True,
             size=(2, 5), life=(1.5, 3.5), col=S.POLLEN, grav=0.0):
        for _ in range(count):
            ang = random.uniform(0, math.tau)
            sp = random.uniform(0, speed)
            vx = math.cos(ang) * sp
            vy = math.sin(ang) * sp
            if up:
                vy = -abs(vy) - speed * 0.3
            self.particles.append(Particle(
                x + random.uniform(-spread, spread),
                y + random.uniform(-spread, spread),
                vx, vy,
                random.uniform(*life),
                random.randint(*size),
                col, grav))

    def ambient_pollen(self, dt, area_rect, density=0.6, col=S.POLLEN):
        """Continuously spawn slow drifting motes inside a rect."""
        if random.random() < density:
            x = random.uniform(area_rect.left, area_rect.right)
            y = random.uniform(area_rect.top, area_rect.bottom)
            self.particles.append(Particle(
                x, y,
                random.uniform(-6, 6), random.uniform(-14, -4),
                random.uniform(3, 6), random.randint(1, 3), col))

    def burst(self, x, y, count=120, col=S.SPORE):
        for _ in range(count):
            ang = random.uniform(0, math.tau)
            sp = random.uniform(40, 260)
            self.particles.append(Particle(
                x, y, math.cos(ang) * sp, math.sin(ang) * sp,
                random.uniform(0.6, 1.6), random.randint(2, 6), col, grav=60))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


# ---------------------------------------------------------------------------
#  SCREEN-SPACE EFFECTS
# ---------------------------------------------------------------------------
def vignette(surf, strength=180, radius_scale=0.75):
    """Darken the edges of the screen."""
    w, h = surf.get_size()
    v = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, h // 2
    max_r = math.hypot(cx, cy)
    steps = 24
    for i in range(steps, 0, -1):
        t = i / steps
        r = int(max_r * t)
        a = int(strength * (t - radius_scale) / (1 - radius_scale)) if t > radius_scale else 0
        a = max(0, min(255, a))
        if a:
            pygame.draw.circle(v, (0, 0, 0, a), (cx, cy), r)
    surf.blit(v, (0, 0))


def flicker_overlay(surf, intensity):
    """Random darkening to fake failing fluorescent lights. intensity 0..1."""
    if random.random() < 0.12 * intensity:
        a = random.randint(40, int(40 + 140 * intensity))
        s = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, a))
        surf.blit(s, (0, 0))


def light_mask(surf, center, radius=240, darkness=235):
    """Cover the screen in darkness with a soft light hole at `center`."""
    w, h = surf.get_size()
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    mask.fill((0, 0, 0, darkness))
    steps = 14
    cx, cy = center
    for i in range(steps):
        t = i / steps
        r = int(radius * (1 - t))
        a = int(darkness * t)
        pygame.draw.circle(mask, (0, 0, 0, a), (int(cx), int(cy)), r)
    surf.blit(mask, (0, 0))


def distortion(surf, amount):
    """
    Cheap 'sanity loss' wobble: slice the screen into horizontal bands and
    offset each one, plus a faint red/cyan split. amount 0..1.
    """
    if amount <= 0:
        return surf
    w, h = surf.get_size()
    out = surf.copy()
    bands = 18
    bh = h // bands
    t = pygame.time.get_ticks() / 200.0
    for i in range(bands):
        off = int(math.sin(t + i * 0.7) * 14 * amount)
        y = i * bh
        band = surf.subsurface((0, y, w, min(bh, h - y))).copy()
        out.blit(band, (off, y))
    # chromatic aberration
    if amount > 0.4:
        shift = int(6 * amount)
        red = out.copy()
        red.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
        out.blit(red, (shift, 0), special_flags=pygame.BLEND_ADD)
    return out


def glow(surf, center, radius, colour, intensity=120):
    """Additive soft halo (petal glow, healing aura, etc.)."""
    g = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    steps = 12
    for i in range(steps, 0, -1):
        t = i / steps
        a = int(intensity * (1 - t))
        pygame.draw.circle(g, (*colour, a), (radius, radius), int(radius * t))
    surf.blit(g, (center[0] - radius, center[1] - radius),
              special_flags=pygame.BLEND_ADD)


def heat_pulse(surf, t, colour=S.BLOOD, base=20, amp=35):
    """Breathing red wash for the Heart Chamber. t is seconds."""
    a = int(base + amp * (0.5 + 0.5 * math.sin(t * 2.0)))
    s = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    s.fill((*colour, a))
    surf.blit(s, (0, 0))
