"""Shared helper utilities for the blooming game."""

import pygame
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List


# Path to DejaVu Sans font on the system
_DEJA_VU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_image(path: str):
    """Load an image from the assets/images directory.

    Uses PIL to load the image as RGBA, then converts to pygame Surface
    via frombuffer. This avoids pygame.image.load() returning 24-bit
    surfaces that convert_alpha() fails on in pygame 2.6.1 + Python 3.14.

    Args:
        path: Relative path within blooming/assets/images/

    Returns:
        pygame Surface or None if file not found
    """
    from blooming.utils import IMAGE_DIR
    if IMAGE_DIR is None:
        return None
    full = os.path.join(IMAGE_DIR, path)
    if not os.path.exists(full):
        return None
    try:
        pil_img = Image.open(full).convert('RGBA')
        data = pil_img.tobytes("raw", "RGBA")
        surf = pygame.image.frombuffer(data, pil_img.size, "RGBA")
        return surf.convert_alpha()
    except Exception:
        return None


def make_font(size: int) -> ImageFont.FreeTypeFont:
    """Create a font by size, falling back to default."""
    try:
        return ImageFont.truetype(_DEJA_VU, size)
    except Exception:
        return ImageFont.load_default()


def render_text(font, text: str, color: Tuple[int, int, int]):
    """Render text to a pygame Surface using PIL.

    Args:
        font: PIL ImageFont object
        text: Text string to render
        color: (R, G, B) tuple

    Returns:
        pygame Surface with the rendered text
    """
    bbox = font.getbbox(text)
    x0, y0, x1, y1 = bbox
    width = x1 - x0
    height = y1 - y0
    if width <= 0 or height <= 0:
        s = pygame.Surface((1, 1), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        return s
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((-x0, -y0), text, fill=(*color, 255), font=font)
    mode = img.mode
    raw = img.tobytes()
    return pygame.image.frombytes(raw, (width, height), mode)


def text_size(font, text: str) -> Tuple[int, int]:
    """Get the pixel size of rendered text."""
    bbox = font.getbbox(text)
    x0, y0, x1, y1 = bbox
    return (x1 - x0, y1 - y0)


def scale_image_keep_ratio(surface, max_w: int, max_h: int):
    """Scale surface to fit within (max_w, max_h) while preserving aspect ratio.

    Returns:
        (scaled_surface, center_x, center_y) where (center_x, center_y)
        is the position to blit for centering within the bounding box.
    """
    orig_w, orig_h = surface.get_size()
    scale_x = max_w / orig_w
    scale_y = max_h / orig_h
    scale = min(scale_x, scale_y)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    scaled = pygame.transform.smoothscale(surface, (new_w, new_h))
    # Center offset within the max bounding box
    cx = (max_w - new_w) // 2
    cy = (max_h - new_h) // 2
    return scaled, cx, cy


def draw_rounded_rect(surface, color, rect, radius=8):
    """Draw a filled rectangle with rounded corners."""
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    w = max(w, radius * 2)
    h = max(h, radius * 2)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    corners = [
        (radius, radius, radius, radius),
        (w - radius, radius, radius, radius),
        (w - radius, h - radius, radius, radius),
        (radius, h - radius, radius, radius),
    ]
    pygame.draw.ellipse(s, color,
                        pygame.Rect(0, 0, radius * 2, radius * 2))
    pygame.draw.ellipse(s, color,
                        pygame.Rect(w - radius * 2, 0, radius * 2, radius * 2))
    pygame.draw.ellipse(s, color,
                        pygame.Rect(w - radius * 2, h - radius * 2,
                                    radius * 2, radius * 2))
    pygame.draw.ellipse(s, color,
                        pygame.Rect(0, h - radius * 2, radius * 2, radius * 2))
    pygame.draw.rect(s, color,
                     pygame.Rect(radius, 0, w - radius * 2, h))
    pygame.draw.rect(s, color,
                     pygame.Rect(0, radius, w, h - radius * 2))
    surface.blit(s, (x, y))
