"""Chapter title screen - brief intro before each chapter."""

import pygame
from blooming.utils.utils import render_text, make_font, scale_image_keep_ratio
from blooming.utils import COLORS


class ChapterTitleScreen:
    """Displays chapter name with fade-in animation before a chapter begins."""

    def __init__(self, chapter_num, chapter_title):
        self.chapter_num = chapter_num
        self.chapter_title = chapter_title
        self.font = make_font(72)
        self.small_font = make_font(32)
        self.hint_font = make_font(20)
        self.done = False
        self.alpha = 0
        self.fade_speed = 5
        self.waiting = False
        self.wait_timer = 0
        self.bg_img = None
        try:
            from blooming.utils.utils import load_image
            self.bg_img = load_image('backgrounds/greenhouse-exterior.png')
        except Exception:
            pass

    def draw(self, screen):
        """Draw the chapter title screen."""
        # Background
        if self.bg_img:
            bg_scaled, bx, by = scale_image_keep_ratio(self.bg_img, 1024, 768)
            screen.blit(bg_scaled, (bx, by))
        else:
            screen.fill((20, 20, 30))

        # Dark overlay with dynamic alpha
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(150 * self.alpha)))
        screen.blit(overlay, (0, 0))

        if self.alpha < 0.01:
            return

        surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
        surf.fill((0, 0, 0, int(80 * self.alpha)))
        screen.blit(surf, (0, 0))

        # Chapter number
        num_text = render_text(self.small_font, f"CHAPTER {self.chapter_num}",
                               COLORS['red'])
        screen.blit(num_text, (1024 // 2 - num_text.get_width() // 2, 250))

        # Chapter title
        title_text = render_text(self.font, self.chapter_title, COLORS['white'])
        screen.blit(title_text, (1024 // 2 - title_text.get_width() // 2, 340))

        # Hint
        if self.waiting:
            hint = render_text(self.hint_font, "[Click or press any key to continue]",
                               COLORS['gray'])
            screen.blit(hint, (1024 // 2 - hint.get_width() // 2, 480))

    def update(self, events: list):
        """Update animation. Returns True when player should proceed."""
        if self.done:
            return True

        # Fade in
        if self.alpha < 1.0:
            self.alpha = min(1.0, self.alpha + self.fade_speed * 0.01)

        # Check for player input
        if self.alpha >= 0.5:
            if not self.waiting:
                self.waiting = True
                self.wait_timer = pygame.time.get_ticks()

            now = pygame.time.get_ticks()
            if now - self.wait_timer > 500:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.done = True
                        return True
                    elif event.type == pygame.KEYDOWN:
                        self.done = True
                        return True

            # Auto-advance after 2.5 seconds
            if now - self.wait_timer > 2500:
                self.done = True
                return True

        return False

