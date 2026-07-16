"""Title screen with Start button."""

import pygame
from blooming.utils.utils import render_text, make_font, load_image, scale_image_keep_ratio, load_image
from blooming.utils import COLORS


class TitleScreen:
    """Main title screen with Start button."""

    def __init__(self, screen):
        self.screen = screen
        self.font = make_font(64)
        self.small_font = make_font(32)
        self.hovered = False
        self.start_rect = pygame.Rect(412, 384, 200, 60)
        self.rects = []
        self.bg_img = load_image('backgrounds/greenhouse-exterior.png')
        self._build_rects()

    def _build_rects(self):
        """Rebuild rects after resize."""
        self.rects = []
        self.rects.append(pygame.Rect(412, 384, 200, 60))

    def draw(self):
        """Draw the title screen."""
        if self.bg_img:
            bg_scaled, bx, by = scale_image_keep_ratio(self.bg_img, 1024, 768)
            self.screen.blit(bg_scaled, (bx, by))
        else:
            self.screen.fill(COLORS['dark_fog'])

        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))

        # Title
        title_surf = render_text(self.font, "THE BLOOMING",
                                 COLORS['red'])
        self.screen.blit(title_surf, (1024 // 2 - 180, 120))

        # Subtitle
        sub = render_text(self.small_font, "A Psychological Horror",
                          COLORS['gray'])
        self.screen.blit(sub, (1024 // 2 - 140, 210))

        # Start button
        is_hover = self.hovered
        btn_color = COLORS['red'] if is_hover else COLORS['dark_gray']
        text_color = COLORS['white']
        pygame.draw.rect(self.screen, btn_color, self.start_rect)
        if is_hover:
            pygame.draw.rect(self.screen, COLORS['yellow'], self.start_rect, 2)

        start_surf = render_text(self.small_font, "START", text_color)
        self.screen.blit(start_surf, (480 - start_surf.get_width() // 2,
                                       398))

        # Hint
        hint = render_text(make_font(18), "Click to begin",
                           COLORS['gray'])
        self.screen.blit(hint, (1024 // 2 - 60, 470))

    def update(self, events: list):
        """Handle mouse events. Returns 'start' if Start clicked."""
        self.hovered = self.start_rect.collidepoint(pygame.mouse.get_pos())

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.start_rect.collidepoint(event.pos):
                    return 'start'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return 'start'
                elif event.key == pygame.K_ESCAPE:
                    return 'quit'
        return None
