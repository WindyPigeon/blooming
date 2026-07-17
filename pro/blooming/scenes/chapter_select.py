"""Chapter Select menu - lets player skip to any chapter."""

import pygame
from blooming.utils.utils import render_text, make_font
from blooming.utils import COLORS


class ChapterSelect:
    """Menu to select which chapter to start."""

    def __init__(self, screen):
        self.screen = screen
        self.font = make_font(32)
        self.small_font = make_font(24)
        self.hovered = -1  # which chapter is hovered
        self.selected = 0  # which chapter to start

        # Chapter info: (title, description, start_scene_class)
        self.chapters = [
            {
                'title': 'Chapter 1 - Arrival',
                'desc': 'Arrive at Blackwood Facility.\nMeet Dr. Mara. Get your\naccess card.',
                'key': 'arrival',
            },
            {
                'title': 'Chapter 2 - Greenhouse',
                'desc': 'Explore the greenhouse.\nMeet Specimen X-17.\nInspection tutorial.',
                'key': 'greenhouse',
            },
            {
                'title': 'Chapter 3 - Plant Care',
                'desc': 'Water X-17 with 500 ml.\nMara gets paged and leaves.\nThe greenhouse goes quiet.',
                'key': 'care',
            },
            {
                'title': 'Chapter 4 - Supernatural',
                'desc': 'X-17 glows and whispers.\nHorror response choices.\nEnd of Day 1.',
                'key': 'horror',
            },
        ]

        self.button_rects = []
        self._build_buttons()

        # Back button rect
        self.back_rect = pygame.Rect(20, 700, 120, 40)

    def _build_buttons(self):
        """Create button rects for each chapter."""
        self.button_rects = []
        btn_w = 500
        btn_h = 80
        gap = 20
        total_h = len(self.chapters) * (btn_h + gap) - gap
        start_y = (768 - total_h) // 2

        for i, ch in enumerate(self.chapters):
            x = (1024 - btn_w) // 2
            y = start_y + i * (btn_h + gap)
            self.button_rects.append(pygame.Rect(x, y, btn_w, btn_h))

    def draw(self):
        """Draw the chapter select menu."""
        self.screen.fill(COLORS['dark_fog'])

        # Title
        title_surf = render_text(self.font, "THE BLOOMING",
                                 COLORS['red'])
        self.screen.blit(title_surf, (1024 // 2 - 150, 30))

        sub = render_text(self.small_font, "Select Chapter to Start",
                          COLORS['gray'])
        self.screen.blit(sub, (1024 // 2 - 160, 80))

        # Chapter buttons
        for i, (ch, rect) in enumerate(zip(self.chapters, self.button_rects)):
            is_hover = i == self.hovered
            color = COLORS['white'] if is_hover else COLORS['dark_gray']
            text_color = COLORS['black'] if is_hover else COLORS['white']

            pygame.draw.rect(self.screen, color, rect)
            if is_hover:
                pygame.draw.rect(self.screen, COLORS['yellow'], rect, 2)

            title_surf = render_text(self.small_font, ch['title'],
                                     text_color)
            self.screen.blit(title_surf, (rect.x + 15, rect.y + 10))

            # Draw description lines
            lines = ch['desc'].split('\n')
            desc_font = make_font(16)
            for j, line in enumerate(lines):
                l = render_text(desc_font, line,
                                COLORS['gray'] if is_hover else
                                (COLORS['gray']))
                self.screen.blit(l, (rect.x + 15, rect.y + 40 + j * 18))

        # Back button
        self._draw_back_button()

    def _draw_back_button(self):
        """Draw a back button at bottom-left."""
        is_hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        color = COLORS['yellow'] if is_hover else COLORS['dark_gray']
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=4)
        if is_hover:
            pygame.draw.rect(self.screen, COLORS['white'],
                             self.back_rect, 2, border_radius=4)
        lbl = render_text(make_font(16), "← Back", COLORS['black'])
        self.screen.blit(lbl, (self.back_rect.x + 25,
                               self.back_rect.y + 10))

        # Hint
        hint = render_text(make_font(20),
                           "Click a chapter to start | ESC for menu",
                           COLORS['white'])
        self.screen.blit(hint, (1024 // 2 - 200, 720))

    def update(self, events: list):
        """Handle mouse events."""
        self.hovered = -1
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.hovered = i

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    # Back button
                    if self.back_rect.collidepoint(pos):
                        return 'back'
                    # Chapter buttons
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(pos):
                            self.selected = i
                            return self.chapters[i]['key']
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'back'
        return None
