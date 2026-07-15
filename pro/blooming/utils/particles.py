"""Particle effects: pollen, spore, glow, and ambient particles."""

import math

import pygame
from typing import Dict, List, Any


class ParticleSystem:
    """Manages floating particles for atmosphere and horror effects."""

    def __init__(self):
        self.particles: List[Dict[str, Any]] = []

    def add_pollen(self, x: int, y: int, count: int = 5):
        """Add floating yellow pollen particles."""
        for _ in range(count):
            angle = (pygame.time.get_ticks() % 360)
            speed = 0.5 + (pygame.time.get_ticks() % 2) * 0.2
            self.particles.append({
                'x': x,
                'y': y,
                'vx': speed * math.cos(math.radians(angle)),
                'vy': -speed * math.sin(math.radians(angle)) - 0.3,
                'size': 2 + (pygame.time.get_ticks() % 3),
                'alpha': 255,
                'color': (255, 255, 200),
                'type': 'pollen',
                'wobble': pygame.time.get_ticks() * 0.01,
            })

    def add_spore(self, x: int, y: int, count: int = 10):
        """Add explosive green spore particles."""
        for _ in range(count):
            angle = pygame.time.get_ticks() % 360
            speed = 1 + (pygame.time.get_ticks() % 3)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': speed * math.cos(math.radians(angle)),
                'vy': speed * math.sin(math.radians(angle)),
                'size': 3 + (pygame.time.get_ticks() % 4),
                'alpha': 255,
                'color': (200, 255, 200),
                'type': 'spore',
            })

    def add_glow(self, x: int, y: int, radius: int = 50):
        """Add a pulsating glow particle."""
        self.particles.append({
            'x': x,
            'y': y,
            'radius': radius,
            'max_radius': radius + 20,
            'pulse': 0,
            'alpha': 128,
            'color': (255, 255, 200),
            'type': 'glow',
        })

    def add_ambient(self, x: int, y: int, count: int = 3):
        """Add small ambient floating dust particles."""
        for _ in range(count):
            self.particles.append({
                'x': x + (pygame.time.get_ticks() % 50) - 25,
                'y': y + (pygame.time.get_ticks() % 30) - 15,
                'vx': (pygame.time.get_ticks() % 2 - 1) * 0.3,
                'vy': -0.1 - (pygame.time.get_ticks() % 2) * 0.1,
                'size': 1,
                'alpha': 100,
                'color': (200, 200, 200),
                'type': 'ambient',
                'wobble': pygame.time.get_ticks() * 0.005,
            })

    def update(self, dt: float = 0.016):
        """Update all particles."""
        for p in self.particles[:]:
            if p['type'] in ('pollen', 'spore', 'ambient'):
                wobble = p.get('wobble', 0)
                p['x'] += p['vx'] + math.sin(wobble) * 0.2
                p['y'] += p['vy']
                p['alpha'] -= (2 if p['type'] == 'spore' else 1)
                if p.get('size', 1) == 1:
                    p['alpha'] -= 1
                if p['alpha'] <= 0:
                    self.particles.remove(p)
            elif p['type'] == 'glow':
                p['pulse'] += 0.1
                p['alpha'] = int(128 + 127 * math.sin(p['pulse']))

    def draw(self, screen):
        """Draw all particles on screen."""
        for p in self.particles:
            if p['type'] in ('pollen', 'spore', 'ambient'):
                s = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
                s.fill((*p['color'][:3], max(0, p['alpha'])))
                screen.blit(s, (p['x'], p['y']))
            elif p['type'] == 'glow':
                s = pygame.Surface((p['radius'] * 2, p['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'][:3], max(0, p['alpha'])),
                                  (p['radius'], p['radius']), p['radius'])
                screen.blit(s, (p['x'] - p['radius'], p['y'] - p['radius']))

    def clear(self):
        """Remove all particles."""
        self.particles.clear()
