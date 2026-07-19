"""Inventory system with item collection and tracking."""

import os
import pygame
from blooming.utils.utils import render_text, make_font
from blooming.utils import COLORS


class Inventory:
    """Manages player inventory items."""

    def __init__(self):
        self.items = {}
        self.selected = None
        self.item_font = make_font(16)
        self._image_cache = {}

    def _get_image_path(self):
        """Get data/images directory path."""
        from blooming.utils import IMAGE_DIR
        return IMAGE_DIR

    def add_item(self, item_id: str, name: str, description: str = "",
                 image_path: str = ""):
        """Add an item to inventory."""
        if item_id not in self.items:
            self.items[item_id] = {
                'name': name,
                'description': description,
                'used': False,
                'image_path': image_path,
            }

    def _load_item_image(self, image_path):
        """Load and cache item image."""
        if not image_path or image_path in self._image_cache:
            return self._image_cache.get(image_path)
        if image_path not in self._image_cache:
            try:
                full_path = os.path.join(self._get_image_path(), image_path)
                if os.path.exists(full_path):
                    img = pygame.image.load(full_path)
                    self._image_cache[image_path] = img
                    return img
            except Exception:
                pass
        return None

    def remove_item(self, item_id: str):
        """Remove item from inventory."""
        self.items.pop(item_id, None)
        if self.selected == item_id:
            self.selected = None

    def select(self, item_id: str) -> bool:
        """Select an item from inventory."""
        if item_id in self.items:
            self.selected = item_id
            return True
        return False

    def deselect(self):
        """Clear selection."""
        self.selected = None

    def has_item(self, item_id: str) -> bool:
        """Check if player has an item."""
        return item_id in self.items

    def is_selected(self, item_id: str) -> bool:
        """Check if a specific item is selected."""
        return self.selected == item_id

    def mark_used(self, item_id: str):
        """Mark an item as used."""
        if item_id in self.items:
            self.items[item_id]['used'] = True

    def get_selected_item(self):
        """Get currently selected item data."""
        if self.selected and self.selected in self.items:
            return self.items[self.selected]
        return None

    def draw(self, screen):
        """Draw inventory bar at bottom of screen."""
        if not self.items:
            return

        inv_rect = pygame.Rect(0, 768 - 80, 1024, 80)
        pygame.draw.rect(screen, COLORS['black'], inv_rect)
        pygame.draw.rect(screen, COLORS['white'], inv_rect, 2)

        # Label
        label = render_text(self.item_font, "INVENTORY", COLORS['gray'])
        screen.blit(label, (20, 768 - 75))

        x_off = 20
        for item_id, item_data in self.items.items():
            item_img = self._load_item_image(item_data.get('image_path', ''))
            item_rect = pygame.Rect(x_off + 10, 768 - 60, 60, 60)
            if self.selected == item_id:
                pygame.draw.rect(screen, COLORS['yellow'], item_rect, 3)
            if item_img:
                img_w = min(item_rect.width, item_img.get_width())
                img_h = min(item_rect.height, item_img.get_height())
                scale = min(img_w / item_img.get_width(), img_h / item_img.get_height())
                scaled_w = int(item_img.get_width() * scale)
                scaled_h = int(item_img.get_height() * scale)
                scaled = pygame.transform.smoothscale(item_img, (scaled_w, scaled_h))
                draw_x = item_rect.x + (item_rect.width - scaled_w) // 2
                draw_y = item_rect.y + (item_rect.height - scaled_h) // 2
                screen.blit(scaled, (draw_x, draw_y))
            else:
                pygame.draw.rect(screen, COLORS['gray'], item_rect)
                pygame.draw.rect(screen, COLORS['white'], item_rect, 1)
            name_surf = render_text(self.item_font, item_data['name'], COLORS['white'])
            screen.blit(name_surf, (x_off + 10, 768 - 85))
            x_off += 80

    def clear(self):
        """Remove all items."""
        self.items.clear()
        self.selected = None
