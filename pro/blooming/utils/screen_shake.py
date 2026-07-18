"""Screen shake effect for horror sequences."""

import pygame


class ScreenShake:
    """Produces temporary screen displacement for horror effects."""

    def __init__(self):
        self.intensity = 0
        self.duration = 0
        self.elapsed = 0
        self.offset_x = 0
        self.offset_y = 0

    def shake(self, intensity: int = 10, duration: int = 60):
        """Trigger screen shake."""
        self.intensity = intensity
        self.duration = duration
        self.elapsed = 0
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        """Update shake offset."""
        if self.duration > 0:
            self.elapsed += 1
            self.duration -= 1
            # Ramp up in first 10 frames, ramp down in last 10
            if self.elapsed < 10:
                ramp = self.elapsed / 10.0
            elif self.elapsed > self.duration + 10:
                ramp = (self.duration + 10 - self.elapsed) / 10.0
            else:
                ramp = 1.0
            effective = int(self.intensity * ramp)
            if effective == 0:
                effective = 1
            self.offset_x = (pygame.time.get_ticks() % (effective * 2)) - effective
            self.offset_y = (pygame.time.get_ticks() % (effective * 2)) - effective
        else:
            self.offset_x = 0
            self.offset_y = 0
            self.elapsed = 0

    def is_active(self) -> bool:
        return self.duration > 0

    def get_offset(self):
        return (self.offset_x, self.offset_y)
