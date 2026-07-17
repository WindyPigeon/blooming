"""Pause menu - settings overlay with volume controls."""

import pygame
import json
import os
from blooming.utils.utils import render_text, make_font
from blooming.utils import COLORS

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'settings.json')


class PauseMenu:
    """In-game pause overlay with volume controls and quit option."""

    def __init__(self, screen):
        self.screen = screen
        self.font = make_font(36)
        self.small_font = make_font(28)
        self.btn_font = make_font(24)
        self.hovered = -1  # which button is hovered
        self.dragging_slider = None  # which slider is being dragged
        self.mouse_pressed = False

        # Load or default settings
        self.bgm_volume = self._load_setting('bgm_volume', 0.7)
        self.sfx_volume = self._load_setting('sfx_volume', 0.7)

        # Button rects (centered)
        self._build_buttons()

    def _load_setting(self, key, default):
        """Load a setting from file or return default."""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get(key, default)
        except (json.JSONDecodeError, IOError):
            pass
        return default

    def _save_setting(self, key, value):
        """Save a setting to file."""
        try:
            data = {}
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
            data[key] = value
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass

    def _build_buttons(self):
        """Create button rects for pause menu items."""
        self.continue_rect = pygame.Rect(362, 480, 300, 50)
        self.bgm_rect = pygame.Rect(362, 200, 300, 50)
        self.sfx_rect = pygame.Rect(362, 320, 300, 50)
        self.quit_rect = pygame.Rect(362, 560, 300, 50)

        self.bgm_slider_rect = pygame.Rect(450, 215, 180, 20)
        self.sfx_slider_rect = pygame.Rect(450, 335, 180, 20)

        self.buttons = [
            ('Continue', self.continue_rect),
            ('BGM Volume', self.bgm_rect),
            ('SFX Volume', self.sfx_rect),
            ('Quit', self.quit_rect),
        ]

    def draw(self):
        """Draw the pause overlay."""
        # Dark overlay
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Semi-transparent panel
        panel = pygame.Rect(262, 80, 500, 540)
        pygame.draw.rect(self.screen, (30, 30, 40), panel, border_radius=8)
        pygame.draw.rect(self.screen, COLORS['gray'], panel, 2, border_radius=8)

        # Title
        title = render_text(self.font, "PAUSED", COLORS['white'])
        self.screen.blit(title, (1024 // 2 - 80, 100))

        # Hover detection
        self.hovered = -1
        for i, (name, rect) in enumerate(self.buttons):
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.hovered = i

        # Continue button
        self._draw_button('CONTINUE', self.continue_rect, index=0)

        # BGM Volume slider
        self._draw_slider("BGM Volume", self.bgm_rect,
                          self.bgm_slider_rect, self.bgm_volume,
                          'bgm', index=1)

        # SFX Volume slider
        self._draw_slider("SFX Volume", self.sfx_rect,
                          self.sfx_slider_rect, self.sfx_volume,
                          'sfx', index=2)

        # Quit button
        self._draw_button('QUIT', self.quit_rect, index=3)

        # Close hint
        close_hint = render_text(make_font(18),
                                 "Click Continue to resume",
                                 COLORS['gray'])
        close_rect = close_hint.get_rect(center=(1024 // 2, 650))
        self.screen.blit(close_hint, close_rect)

    def _draw_button(self, label, rect, index=-1):
        """Draw a single button."""
        is_hover = index == self.hovered
        color = COLORS['yellow'] if is_hover else COLORS['dark_gray']
        pygame.draw.rect(self.screen, color, rect, border_radius=4)
        if is_hover:
            pygame.draw.rect(self.screen, COLORS['white'], rect, 2,
                             border_radius=4)
        lbl = render_text(self.btn_font, label, COLORS['black'])
        lbl_rect = lbl.get_rect(center=rect.center)
        self.screen.blit(lbl, lbl_rect)

    def _draw_slider(self, label, button_rect, slider_rect,
                     value, setting_key, index=-1):
        """Draw a volume slider."""
        is_hover = (index == self.hovered or
                    self.dragging_slider == setting_key)
        is_slider_hover = slider_rect.collidepoint(pygame.mouse.get_pos())

        # Label
        lbl = render_text(self.small_font, label, COLORS['white'])
        lbl_rect = lbl.get_rect(midright=(button_rect.x - 15,
                                           button_rect.y + 25))
        self.screen.blit(lbl, lbl_rect)

        # Value text
        val_text = render_text(self.small_font,
                               f"{int(value * 100)}%", COLORS['gray'])
        val_rect = val_text.get_rect(midleft=(button_rect.x + 310,
                                               button_rect.y + 15))
        self.screen.blit(val_text, val_rect)

        # Background track
        track_color = COLORS['dark_gray']
        pygame.draw.rect(self.screen, track_color, slider_rect,
                         border_radius=4)

        # Filled portion
        fill_w = int(slider_rect.width * value)
        fill_rect = pygame.Rect(slider_rect.x, slider_rect.y,
                                fill_w, slider_rect.height)
        fill_color = COLORS['yellow']
        pygame.draw.rect(self.screen, fill_color, fill_rect,
                         border_radius=4)

        # Thumb
        thumb_x = slider_rect.x + fill_w - 8
        thumb_rect = pygame.Rect(thumb_x, slider_rect.y - 2,
                                 16, slider_rect.height + 4)
        thumb_color = COLORS['white'] if is_slider_hover else COLORS['gray']
        pygame.draw.rect(self.screen, thumb_color, thumb_rect,
                         border_radius=4)

        # Button highlight
        if is_hover:
            pygame.draw.rect(self.screen, COLORS['yellow'], button_rect, 1,
                             border_radius=4)

    def update(self, events: list):
        """Handle pause menu events (mouse only)."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    # Slider drag
                    if self.bgm_slider_rect.collidepoint(pos):
                        self.dragging_slider = 'bgm'
                        self._update_slider_value('bgm', pos)
                    elif self.sfx_slider_rect.collidepoint(pos):
                        self.dragging_slider = 'sfx'
                        self._update_slider_value('sfx', pos)
                    # Continue button
                    elif self.continue_rect.collidepoint(pos):
                        return 'continue'
                    # Quit button
                    elif self.quit_rect.collidepoint(pos):
                        return 'quit'

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging_slider = None

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_slider:
                    self._update_slider_value(self.dragging_slider,
                                              event.pos)

        return None

    def _update_slider_value(self, setting_key, pos):
        """Update slider value from mouse position."""
        if setting_key == 'bgm':
            rect = self.bgm_slider_rect
        else:
            rect = self.sfx_slider_rect

        # Clamp to slider bounds
        x = max(rect.x, min(pos[0], rect.x + rect.width))
        value = (x - rect.x) / rect.width
        value = max(0.0, min(1.0, value))

        if setting_key == 'bgm':
            self.bgm_volume = value
        else:
            self.sfx_volume = value

        self._save_setting(f'{setting_key}_volume', value)

    @property
    def bgm_volume(self):
        return self._bgm_volume

    @bgm_volume.setter
    def bgm_volume(self, value):
        self._bgm_volume = value

    @property
    def sfx_volume(self):
        return self._sfx_volume

    @sfx_volume.setter
    def sfx_volume(self, value):
        self._sfx_volume = value
