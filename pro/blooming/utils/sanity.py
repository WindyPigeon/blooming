"""Sanity system with visual meter and hallucination overlay."""

import pygame
from blooming.utils.utils import render_text, make_font
from blooming.utils import COLORS


class SanitySystem:
    """Tracks player sanity and triggers horror effects."""

    def __init__(self):
        self.sanity = 100
        self.max_sanity = 100
        self.hallucination_level = 0
        self.hallucination_timer = 0
        self.font = make_font(20)
        self.meter_font = make_font(16)

    def decrease_sanity(self, amount: int = 10):
        """Decrease sanity by amount."""
        self.sanity = max(0, self.sanity - amount)
        self.hallucination_level = (100 - self.sanity) // 20
        if self.hallucination_level > 5:
            self.hallucination_level = 5

    def decrease_by_percent(self, percent: int):
        """Decrease sanity by percentage of max."""
        amount = int((self.max_sanity - self.sanity) * percent / 100)
        self.decrease_sanity(max(amount, 1))

    def increase_sanity(self, amount: int = 10):
        """Increase sanity."""
        self.sanity = min(self.max_sanity, self.sanity + amount)
        self.hallucination_level = (100 - self.sanity) // 20

    def update(self):
        """Update internal timers."""
        self.hallucination_timer += 1

    def is_hallucinating(self) -> bool:
        return self.sanity < 50

    def is_critical(self) -> bool:
        return self.sanity <= 0

    def draw(self, screen):
        """Draw sanity meter at top-left corner."""
        meter_rect = pygame.Rect(20, 20, 200, 20)
        pygame.draw.rect(screen, COLORS['dark_gray'], meter_rect)
        pygame.draw.rect(screen, COLORS['white'], meter_rect, 2)

        fill_w = max(0, int((self.sanity / self.max_sanity) * 196))
        if self.sanity > 70:
            fill_c = COLORS['green']
        elif self.sanity > 40:
            fill_c = COLORS['orange']
        else:
            fill_c = COLORS['red']
        pygame.draw.rect(screen, fill_c,
                         (meter_rect.x + 2, meter_rect.y + 2, fill_w, 16))

        text_surf = render_text(self.font, f"Sanity: {self.sanity}%", COLORS['white'])
        screen.blit(text_surf, (meter_rect.x + 220, 20))

        # Hallucination overlay
        if self.is_hallucinating():
            overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
            alpha = int(50 + 50 * (self.hallucination_level / 5))
            overlay.fill((100, 0, 0, alpha))
            screen.blit(overlay, (0, 0))

        # Flicker effect when sanity is very low
        if self.sanity < 20 and self.hallucination_timer % 60 < 30:
            overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 40))
            screen.blit(overlay, (0, 0))

    def reset(self):
        """Reset sanity to full."""
        self.sanity = self.max_sanity
        self.hallucination_level = 0
