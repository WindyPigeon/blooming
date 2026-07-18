"""Dialogue system with text rendering and choice handling."""

import pygame
from blooming.utils.utils import render_text, text_size, make_font
from blooming.utils import COLORS


class DialogueSystem:
    """Manages character dialogue with choices."""

    def __init__(self, screen):
        self.screen = screen
        self.font = make_font(32)
        self.text_font = make_font(24)
        self.choice_font = make_font(24)
        self.current_dialogue = None
        self.choices = []
        self.choice_callback = None
        self.auto_advance = False
        self.auto_advance_timer = 0.0
        self.typewriter_text = ""
        self.typewriter_index = 0
        self.typewriter_timer = 0
        self.typewriter_speed = 3
        self.typewriter_active = False
        self.box_rect = pygame.Rect(50, 500, 1024 - 100, 200)

    def show_dialogue(self, text: str, speaker: str = "Elias",
                      choices=None, callback=None, auto_advance=False):
        """Display a dialogue box with optional choices."""
        self.current_dialogue = {
            'text': text,
            'speaker': speaker,
            'lines': self._wrap_text(text, 550),
        }
        self.choices = choices or []
        self.choice_callback = callback
        self.typewriter_text = text
        self.typewriter_index = 0
        self.typewriter_active = False
        # Auto-advance after short delay for typewriter effect
        self.typewriter_delay = len(text) * self.typewriter_speed
        self.auto_advance = auto_advance
        self.auto_advance_timer = 0.0

    def _wrap_text(self, text: str, max_width: int) -> list:
        """Wrap text into lines that fit within max_width."""
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            w, _ = text_size(self.text_font, test_line)
            if w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        if current_line:
            lines.append(current_line)
        return lines

    def update(self, events: list):
        """Process events for dialogue interaction."""
        # Don't auto-consume clicks — scenes handle their own dialogue advancement.
        # Only handle choice clicks here (choices are only used by scene3).
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_dialogue and self.choice_callback and self.choices:
                    pos = pygame.mouse.get_pos()
                    for i, choice in enumerate(self.choices):
                        y_pos = 620 + i * 40
                        if (150 <= pos[0] <= 1024 - 150
                                and y_pos <= pos[1] <= y_pos + 30):
                            self.choice_callback(choice)
                            self.current_dialogue = None
                            self.choices = []
                            self.choice_callback = None
                            return

        # Auto-clear dialogues that have no choices
        if (self.auto_advance
                and self.current_dialogue
                and not self.choices):
            self.auto_advance_timer += 0.016
            if self.auto_advance_timer >= 1.0:
                self.current_dialogue = None
                self.typewriter_index = 0
                self.typewriter_active = False
                self.auto_advance = False
                self.auto_advance_timer = 0.0

    def draw(self):
        """Draw the dialogue box."""
        if not self.current_dialogue:
            return

        # Semi-transparent background
        bg_surf = pygame.Surface((self.box_rect.width, self.box_rect.height),
                                 pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))
        self.screen.blit(bg_surf, (self.box_rect.x, self.box_rect.y))
        pygame.draw.rect(self.screen, COLORS['white'], self.box_rect, 2)

        # Speaker name
        speaker_surf = render_text(self.font, self.current_dialogue['speaker'],
                                   COLORS['yellow'])
        self.screen.blit(speaker_surf,
                         (self.box_rect.x + 10, self.box_rect.y + 10))

        # Text lines
        y_off = self.box_rect.y + 50
        display_text = self.typewriter_text[:self.typewriter_index] \
            if self.typewriter_active else self.current_dialogue['text']
        lines = self._wrap_text(display_text, 550)
        for line in lines:
            text_surf = render_text(self.text_font, line, COLORS['white'])
            self.screen.blit(text_surf,
                             (self.box_rect.x + 10, y_off))
            y_off += 30

        # Choices
        if self.choices and self.choice_callback:
            y_off = 620
            for choice in self.choices:
                choice_rect = pygame.Rect(150, y_off, 1024 - 300, 30)
                pygame.draw.rect(self.screen, COLORS['gray'], choice_rect)
                pygame.draw.rect(self.screen, COLORS['white'], choice_rect, 1)
                choice_surf = render_text(self.choice_font, '  ' + choice,
                                          COLORS['white'])
                self.screen.blit(choice_surf,
                                 (choice_rect.x + 10, choice_rect.y + 5))
                y_off += 40

        # Click hint
        if not self.choices:
            hint_surf = render_text(make_font(16), "[click to continue]",
                                    COLORS['gray'])
            self.screen.blit(hint_surf,
                             (self.box_rect.x + 10, self.box_rect.y + self.box_rect.height - 25))

    def clear(self):
        """Clear current dialogue."""
        self.current_dialogue = None
        self.choices = []
        self.choice_callback = None
