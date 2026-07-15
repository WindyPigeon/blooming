"""Journal system for tracking objectives and notes."""

import pygame
from blooming.utils.utils import render_text, make_font
from blooming.utils import COLORS


class Journal:
    """Tracks game objectives and unlocks notes."""

    def __init__(self):
        self.entries = {}
        self.active = False
        self.title_font = make_font(28)
        self.content_font = make_font(20)

    def add_entry(self, entry_id: str, title: str, content: str):
        """Add a journal entry (locked)."""
        self.entries[entry_id] = {
            'title': title,
            'content': content,
            'unlocked': False,
        }

    def unlock_entry(self, entry_id: str):
        """Unlock a journal entry."""
        if entry_id in self.entries:
            self.entries[entry_id]['unlocked'] = True

    def add_objective(self, objective_id: str, title: str, description: str):
        """Add a tracking objective."""
        if 'objectives' not in self.entries:
            self.entries['objectives'] = {
                'title': 'OBJECTIVES',
                'content': '',
                'unlocked': True,
                'is_objective_list': True,
            }
        self.entries[objective_id] = {
            'title': title,
            'content': description,
            'unlocked': True,
            'is_objective': True,
        }

    def update_objective(self, objective_id: str, new_title: str = None,
                         new_content: str = None):
        """Update an active objective."""
        if objective_id in self.entries:
            if new_title:
                self.entries[objective_id]['title'] = new_title
            if new_content:
                self.entries[objective_id]['content'] = new_content

    def complete_objective(self, objective_id: str):
        """Mark an objective as complete."""
        if objective_id in self.entries:
            current = self.entries[objective_id]['content']
            if '✅' not in current:
                self.entries[objective_id]['content'] = '✅ ' + current

    def draw(self, screen):
        """Draw journal overlay if active."""
        if not self.active:
            return

        rect = pygame.Rect(100, 100, 1024 - 200, 768 - 200)
        pygame.draw.rect(screen, COLORS['black'], rect)
        pygame.draw.rect(screen, COLORS['white'], rect, 3)

        y_off = rect.y + 20
        title_surf = render_text(self.title_font, "JOURNAL", COLORS['yellow'])
        screen.blit(title_surf, (rect.x + 20, y_off))
        y_off += 40

        for eid, edata in self.entries.items():
            if edata.get('is_objective_list'):
                continue
            if edata['unlocked']:
                icon = '✅ ' if edata.get('is_objective') else '📝 '
                title_surf = render_text(self.title_font, icon + edata['title'],
                                         COLORS['yellow'])
                screen.blit(title_surf, (rect.x + 20, y_off))
                y_off += 35
                for line in edata['content'].split('\n'):
                    s = render_text(self.content_font, '  ' + line, COLORS['white'])
                    screen.blit(s, (rect.x + 30, y_off))
                    y_off += 25
                y_off += 15

        close_surf = render_text(self.content_font, "[J to close]", COLORS['gray'])
        screen.blit(close_surf, (rect.x + 20, rect.y + rect.height - 30))

    def clear(self):
        """Clear all entries."""
        self.entries.clear()
