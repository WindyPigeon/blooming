"""
Blooming - A 2D Point-and-Click Psychological Horror Game
Group 24 - CT029-3-2-Imaging and Special Effects
"""

import pygame
import sys
import os
import math
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image, ImageDraw, ImageFont

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'green': (0, 128, 0),
    'dark_green': (0, 64, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'pink': (255, 192, 203),
    'brown': (139, 69, 19)
}

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, 'data', 'images')


def load_image(path: str):
    full = os.path.join(IMAGE_DIR, path)
    if os.path.exists(full):
        try:
            return pygame.image.load(full).convert_alpha()
        except Exception:
            return None
    return None


def make_font(size: int):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def render_text(font, text: str, color: Tuple[int, int, int]):
    mask = font.getmask(text)
    size = mask.size
    if size[0] == 0 or size[1] == 0:
        s = pygame.Surface((1, 1), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        return s
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, fill=(*color, 255), font=font)
    mode = img.mode
    raw = img.tobytes()
    return pygame.image.frombytes(raw, size, mode)


def text_size(font, text: str):
    mask = font.getmask(text)
    return mask.size


class ParticleSystem:
    def __init__(self):
        self.particles: List[Dict[str, Any]] = []
    
    def add_pollen(self, x: int, y: int, count: int = 5):
        for _ in range(count):
            angle = pygame.time.get_ticks() % 360
            speed = 0.5 + (pygame.time.get_ticks() % 2) * 0.2
            self.particles.append({
                'x': x, 'y': y,
                'vx': speed * math.cos(math.radians(angle)),
                'vy': -speed * math.sin(math.radians(angle)),
                'size': 2 + (pygame.time.get_ticks() % 3),
                'alpha': 255,
                'color': (255, 255, 200),
                'type': 'pollen'
            })
    
    def add_spore(self, x: int, y: int, count: int = 10):
        for _ in range(count):
            angle = pygame.time.get_ticks() % 360
            speed = 1 + (pygame.time.get_ticks() % 3)
            self.particles.append({
                'x': x, 'y': y,
                'vx': speed * math.cos(math.radians(angle)),
                'vy': speed * math.sin(math.radians(angle)),
                'size': 3 + (pygame.time.get_ticks() % 4),
                'alpha': 255,
                'color': (200, 255, 200),
                'type': 'spore'
            })
    
    def add_glow(self, x: int, y: int, radius: int = 50):
        self.particles.append({
            'x': x, 'y': y,
            'radius': radius,
            'max_radius': radius + 20,
            'pulse': 0,
            'color': (255, 255, 200),
            'type': 'glow'
        })
    
    def update(self, dt: float):
        for p in self.particles[:]:
            if p['type'] in ('pollen', 'spore'):
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['alpha'] -= 2 if p['type'] == 'spore' else 1
                if p['alpha'] <= 0:
                    self.particles.remove(p)
            elif p['type'] == 'glow':
                p['pulse'] += 0.1
                p['alpha'] = int(128 + 127 * math.sin(p['pulse']))
    
    def draw(self, screen: pygame.Surface):
        for p in self.particles:
            if p['type'] in ('pollen', 'spore'):
                s = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
                s.fill((*p['color'][:3], p['alpha']))
                screen.blit(s, (p['x'], p['y']))
            elif p['type'] == 'glow':
                s = pygame.Surface((p['radius'] * 2, p['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'][:3], p['alpha']),
                                 (p['radius'], p['radius']), p['radius'])
                screen.blit(s, (p['x'] - p['radius'], p['y'] - p['radius']))


class ScreenShake:
    def __init__(self):
        self.intensity = 0
        self.duration = 0
        self.offset_x = 0
        self.offset_y = 0
    
    def shake(self, intensity: int = 10, duration: int = 30):
        self.intensity = intensity
        self.duration = duration
    
    def update(self):
        if self.duration > 0:
            self.duration -= 1
            self.offset_x = (pygame.time.get_ticks() % (self.intensity * 2)) - self.intensity
            self.offset_y = (pygame.time.get_ticks() % (self.intensity * 2)) - self.intensity
        else:
            self.offset_x = 0
            self.offset_y = 0


class DialogueSystem:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = make_font(32)
        self.text_font = make_font(24)
        self.current_dialogue: Optional[Dict] = None
        self.choices: List[str] = []
        self.choice_callback = None
        self.box_rect = pygame.Rect(50, 500, SCREEN_WIDTH - 100, 200)
    
    def show_dialogue(self, text: str, speaker: str = "Elias",
                     choices: List[str] = None, callback=None):
        self.current_dialogue = {
            'text': text,
            'speaker': speaker,
            'lines': self.wrap_text(text, 550)
        }
        self.choices = choices or []
        self.choice_callback = callback
    
    def wrap_text(self, text: str, max_width: int) -> List[str]:
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
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_dialogue and self.choice_callback:
                    pos = pygame.mouse.get_pos()
                    for i, choice in enumerate(self.choices):
                        y_pos = 620 + i * 40
                        if 150 <= pos[0] <= SCREEN_WIDTH - 150 and y_pos <= pos[1] <= y_pos + 30:
                            self.choice_callback(choice)
                            self.current_dialogue = None
                            self.choices = []
    
    def draw(self):
        if not self.current_dialogue:
            return
        pygame.draw.rect(self.screen, COLORS['black'], self.box_rect)
        pygame.draw.rect(self.screen, COLORS['white'], self.box_rect, 2)
        
        speaker_surf = render_text(self.font, self.current_dialogue['speaker'], COLORS['yellow'])
        self.screen.blit(speaker_surf, (self.box_rect.x + 10, self.box_rect.y + 10))
        
        y_off = self.box_rect.y + 50
        for line in self.current_dialogue['lines']:
            text_surf = render_text(self.text_font, line, COLORS['white'])
            self.screen.blit(text_surf, (self.box_rect.x + 10, y_off))
            y_off += 30
        
        y_off = self.box_rect.y + 100
        for choice in self.choices:
            choice_rect = pygame.Rect(150, y_off, SCREEN_WIDTH - 300, 30)
            pygame.draw.rect(self.screen, COLORS['gray'], choice_rect)
            choice_surf = render_text(self.text_font, choice, COLORS['white'])
            self.screen.blit(choice_surf, (choice_rect.x + 10, choice_rect.y + 5))
            y_off += 40


class Inventory:
    def __init__(self):
        self.items: Dict[str, Dict[str, Any]] = {}
        self.selected: Optional[str] = None
        self.item_font = make_font(16)
    
    def add_item(self, item_id: str, name: str, description: str = ""):
        self.items[item_id] = {'name': name, 'description': description, 'used': False}
    
    def select(self, item_id: str) -> bool:
        if item_id in self.items:
            self.selected = item_id
            return True
        return False
    
    def has_item(self, item_id: str) -> bool:
        return item_id in self.items
    
    def draw(self, screen: pygame.Surface):
        if not self.items:
            return
        inv_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(screen, COLORS['black'], inv_rect)
        pygame.draw.rect(screen, COLORS['white'], inv_rect, 2)
        
        x_off = 20
        for item_id, item_data in self.items.items():
            item_rect = pygame.Rect(x_off, SCREEN_HEIGHT - 60, 60, 60)
            if self.selected == item_id:
                pygame.draw.rect(screen, COLORS['yellow'], item_rect, 3)
            pygame.draw.rect(screen, COLORS['gray'], item_rect)
            pygame.draw.rect(screen, COLORS['white'], item_rect, 1)
            name_surf = render_text(self.item_font, item_data['name'], COLORS['white'])
            screen.blit(name_surf, (x_off, SCREEN_HEIGHT - 85))
            x_off += 80


class Journal:
    def __init__(self):
        self.entries: Dict[str, Dict[str, str]] = {}
        self.active = False
        self.title_font = make_font(28)
        self.content_font = make_font(20)
    
    def add_entry(self, entry_id: str, title: str, content: str):
        self.entries[entry_id] = {'title': title, 'content': content, 'unlocked': False}
    
    def unlock_entry(self, entry_id: str):
        if entry_id in self.entries:
            self.entries[entry_id]['unlocked'] = True
    
    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        pygame.draw.rect(screen, COLORS['black'], rect)
        pygame.draw.rect(screen, COLORS['white'], rect, 3)
        y_off = rect.y + 20
        for eid, edata in self.entries.items():
            if edata['unlocked']:
                title_surf = render_text(self.title_font, edata['title'], COLORS['yellow'])
                screen.blit(title_surf, (rect.x + 20, y_off))
                y_off += 35
                for line in edata['content'].split('\n'):
                    s = render_text(self.content_font, line, COLORS['white'])
                    screen.blit(s, (rect.x + 30, y_off))
                    y_off += 25
                y_off += 30


class SanitySystem:
    def __init__(self):
        self.sanity = 100
        self.max_sanity = 100
        self.hallucination_level = 0
        self.hallucination_timer = 0
        self.font = make_font(20)
    
    def decrease_sanity(self, amount: int = 10):
        self.sanity = max(0, self.sanity - amount)
        self.hallucination_level = (100 - self.sanity) // 20
    
    def update(self):
        self.hallucination_timer += 1
    
    def is_hallucinating(self) -> bool:
        return self.sanity < 50
    
    def draw(self, screen: pygame.Surface):
        rect = pygame.Rect(20, 20, 200, 20)
        pygame.draw.rect(screen, COLORS['dark_gray'], rect)
        pygame.draw.rect(screen, COLORS['white'], rect, 2)
        fill_w = int((self.sanity / self.max_sanity) * 196)
        fill_c = COLORS['green'] if self.sanity > 50 else COLORS['red']
        pygame.draw.rect(screen, fill_c, (rect.x + 2, rect.y + 2, fill_w, 16))
        text_surf = render_text(self.font, f"Sanity: {self.sanity}%", COLORS['white'])
        screen.blit(text_surf, (rect.x + 220, 20))
        
        if self.is_hallucinating() and self.hallucination_timer % 120 < 60:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = int(50 + 50 * (self.hallucination_level / 3))
            overlay.fill((100, 0, 0, alpha))
            screen.blit(overlay, (0, 0))


class Scene:
    def __init__(self, game: 'Game'):
        self.game = game
        self.font = make_font(32)
        self.hotspots: Dict[str, Dict[str, Any]] = {}
        self.active = True
    
    def update(self, events: List[pygame.event.Event]):
        pass
    
    def draw(self, screen: pygame.Surface):
        pass
    
    def add_hotspot(self, name: str, rect: pygame.Rect, description: str = ""):
        self.hotspots[name] = {'rect': rect, 'description': description, 'active': True}
    
    def handle_hotspot_click(self, pos: Tuple[int, int]) -> Optional[str]:
        if not self.active:
            return None
        for name, hotspot in self.hotspots.items():
            if hotspot['active'] and hotspot['rect'].collidepoint(pos):
                return name
        return None


class Scene1_Arrival(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.background_color = COLORS['dark_gray']
        self.add_hotspot('sign', pygame.Rect(100, 100, 150, 80), "Blackwood Research Facility")
        self.add_hotspot('intercom', pygame.Rect(800, 300, 100, 100), "Security intercom")
        self.add_hotspot('door', pygame.Rect(400, 250, 224, 318), "Security door")
        self.add_hotspot('mara', pygame.Rect(500, 300, 100, 200), "Dr. Mara Vale")
        self.door_locked = True
        self.access_card_found = False
        self.entered = False
    
    def draw(self, screen: pygame.Surface):
        if self.entered:
            return
        screen.fill(self.background_color)
        pygame.draw.rect(screen, COLORS['dark_green'], (300, 300, 424, 300))
        door_color = COLORS['red'] if self.door_locked else COLORS['green']
        pygame.draw.rect(screen, door_color, (400, 250, 224, 318))
        pygame.draw.rect(screen, COLORS['black'], (400, 250, 224, 318), 3)
        pygame.draw.rect(screen, COLORS['gray'], (100, 100, 150, 80))
        for i, t in enumerate(["BLACKWOOD", "RESEARCH", "FACILITY"]):
            s = render_text(self.font, t, COLORS['white'])
            screen.blit(s, (110, 115 + i * 30))
        pygame.draw.circle(screen, COLORS['gray'], (850, 350), 40)
        pygame.draw.circle(screen, COLORS['blue'], (550, 400), 40)
        for i, t in enumerate(["Click hotspots to interact", "Get access card from Mara"]):
            s = render_text(make_font(24), t, COLORS['white'])
            screen.blit(s, (20, SCREEN_HEIGHT - 40 + i * 25))
    
    def update(self, events: List[pygame.event.Event]):
        if self.entered:
            return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                h = self.handle_hotspot_click(event.pos)
                if h == 'door' and self.door_locked and not self.access_card_found:
                    self.game.dialogue.show_dialogue("The door is locked. I need my access card.", "Elias")
                elif h == 'intercom':
                    self.game.dialogue.show_dialogue("Security intercom is active.", "Elias",
                        ["Try intercom"], lambda c: self.game.dialogue.show_dialogue("Access denied.", "Intercom"))
                elif h == 'mara' and not self.access_card_found:
                    self.game.dialogue.show_dialogue("Mara holds out an access card.", "Mara",
                        ["Take the card"], lambda c: self.take_card())
    
    def take_card(self):
        self.game.inventory.add_item('access_card', 'Lvl 1 Card')
        self.access_card_found = True
        self.game.dialogue.show_dialogue("I received my access card.", "Elias",
            ["Enter facility"], lambda c: self.enter_facility())
    
    def enter_facility(self):
        self.entered = True
        self.game.current_scene = Scene2_Orientation(self.game)


class Scene2_Orientation(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.add_hotspot('restricted_lab', pygame.Rect(100, 200, 150, 300), "Restricted Laboratory")
        self.add_hotspot('greenhouse', pygame.Rect(850, 200, 150, 300), "Greenhouse")
        self.add_hotspot('mara', pygame.Rect(500, 350, 100, 150), "Dr. Mara Vale")
        self.mara_leaving = False
    
    def draw(self, screen: pygame.Surface):
        screen.fill(COLORS['dark_gray'])
        pygame.draw.rect(screen, COLORS['dark_gray'], (50, 150, SCREEN_WIDTH - 100, 400))
        pygame.draw.rect(screen, COLORS['red'], (100, 200, 150, 300))
        pygame.draw.rect(screen, COLORS['gray'], (350, 200, 150, 300))
        pygame.draw.rect(screen, COLORS['gray'], (600, 200, 150, 300))
        dc = COLORS['green'] if self.mara_leaving else COLORS['red']
        pygame.draw.rect(screen, dc, (850, 200, 150, 300))
        if not self.mara_leaving:
            pygame.draw.circle(screen, COLORS['blue'], (550, 350), 40)
        for i, l in enumerate(["RESTRICTED", "STAFF OFFICE", "STORAGE", "GREENHOUSE"]):
            s = render_text(self.font, l, COLORS['white'])
            screen.blit(s, (125 + i * 250, 525))
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                h = self.handle_hotspot_click(event.pos)
                if h == 'restricted_lab':
                    self.game.dialogue.show_dialogue("Restricted Laboratory. Need higher clearance.", "Elias")
                elif h == 'greenhouse' and not self.mara_leaving:
                    self.mara_leaving = True
                    self.game.dialogue.show_dialogue("Mara opens the greenhouse door.", "Mara",
                        ["Enter greenhouse"], lambda c: self.enter_greenhouse())
    
    def enter_greenhouse(self):
        self.game.current_scene = Scene3_Greenhouse(self.game)


class Scene3_Greenhouse(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.add_hotspot('watering_can', pygame.Rect(100, 400, 80, 80), "Watering can")
        self.add_hotspot('sink', pygame.Rect(250, 400, 80, 80), "Filtered water sink")
        self.add_hotspot('clipboard', pygame.Rect(400, 400, 80, 80), "Care instructions")
        self.add_hotspot('x17', pygame.Rect(450, 250, 120, 120), "Specimen X-17")
        self.watering_can_held = False
        self.watering_can_filled = False
        self.x17_interacted = False
        self.background_img = load_image('greenhouse/greenhouse-interior.png')
        self.flower_img = load_image('flower/flower.png')
        self.particles = ParticleSystem()
    
    def draw(self, screen: pygame.Surface):
        if self.background_img:
            screen.blit(pygame.transform.scale(self.background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        else:
            screen.fill(COLORS['dark_green'])
            pygame.draw.arc(screen, COLORS['green'], (0, 100, SCREEN_WIDTH, 300), 3.14, 0, 10)
        for i in range(0, SCREEN_WIDTH, 150):
            pygame.draw.rect(screen, COLORS['green'], (i, 250, 50, 100))
        if not self.watering_can_held:
            pygame.draw.rect(screen, COLORS['orange'], (100, 400, 80, 80))
        pygame.draw.rect(screen, COLORS['blue'], (250, 400, 80, 80))
        pygame.draw.rect(screen, COLORS['yellow'], (400, 400, 80, 80))
        if self.flower_img:
            screen.blit(pygame.transform.scale(self.flower_img, (120, 120)), (450, 250))
        else:
            pygame.draw.rect(screen, COLORS['pink'], (450, 250, 120, 120))
        if self.x17_interacted:
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pulse = 100 + 50 * math.sin(pygame.time.get_ticks() * 0.003)
            pygame.draw.circle(glow_surf, (255, 255, 200, int(pulse)), (100, 100), 100)
            screen.blit(glow_surf, (410, 210))
        self.particles.update(0.016)
        self.particles.draw(screen)
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                h = self.handle_hotspot_click(event.pos)
                if h == 'watering_can' and not self.watering_can_held:
                    self.watering_can_held = True
                    self.game.inventory.add_item('empty_can', 'Empty Can')
                elif h == 'sink' and self.watering_can_held and not self.watering_can_filled:
                    self.game.dialogue.show_dialogue("Fill the watering can?", "Elias",
                        ["500 ml"], lambda c: self.fill_can())
                elif h == 'clipboard':
                    self.game.dialogue.show_dialogue("Care sheet: 500ml filtered water daily.", "Instructions")
                elif h == 'x17':
                    self.x17_interacted = True
                    self.game.dialogue.show_dialogue("This is why you're here.", "Mara",
                        ["It looks dangerous.", "It's beautiful.", "It looks unusual."],
                        lambda c: self.x17_choice(c))
    
    def fill_can(self):
        self.watering_can_filled = True
        self.game.inventory.items['empty_can']['name'] = 'Can (500ml)'
        self.game.dialogue.show_dialogue("Filled with 500ml.", "Elias",
            ["Water X-17"], lambda c: self.water_x17())
    
    def x17_choice(self, choice: str):
        responses = {
            "It looks dangerous.": "Appearances are unreliable.",
            "It's beautiful.": "Careful with that word.",
            "It looks unusual.": "Give it time."
        }
        self.game.dialogue.show_dialogue(responses.get(choice, ""), "Mara",
            ["Inspect petals", "Inspect stem", "Inspect soil"],
            lambda c: self.inspect_part(c))
    
    def inspect_part(self, choice: str):
        results = {
            "Inspect petals": "Closed petals. Pale. No damage.",
            "Inspect stem": "Stem is upright. Slight discoloration at base.",
            "Inspect soil": "The soil is dry."
        }
        self.game.dialogue.show_dialogue(results.get(choice, ""), "Elias",
            ["Water it"], lambda c: self.water_x17())
    
    def water_x17(self):
        if not self.watering_can_filled:
            self.game.dialogue.show_dialogue("Need to fill the watering can first.", "Elias")
            return
        self.game.dialogue.show_dialogue("Watered X-17.", "Elias",
            ["Complete observation"], lambda c: self.complete_obs())
    
    def complete_obs(self):
        self.game.journal.unlock_entry('entry2')
        self.particles.add_pollen(510, 310, 20)
        self.game.current_scene = Scene4_Blooming(self.game)


class Scene4_Blooming(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.phase = 0
        self.timer = 0
        self.whisper_counter = 0
        self.particles = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.background_img = load_image('greenhouse/greenhouse-interior.png')
        self.flower_img = load_image('flower/flower.png')
        self.heart_img = load_image('heart.png')
    
    def draw(self, screen: pygame.Surface):
        if self.background_img:
            screen.blit(pygame.transform.scale(self.background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        else:
            screen.fill(COLORS['black'])
        
        if self.phase >= 1 and self.flower_img:
            pulse = 100 + 50 * math.sin(self.timer * 0.1)
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, int(pulse), 100), (100, 100), 100)
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - 100, 200))
            screen.blit(pygame.transform.scale(self.flower_img, (150, 150)),
                       (SCREEN_WIDTH // 2 - 75, 200))
        
        if self.phase >= 2:
            for i in range(5):
                pygame.draw.line(screen, COLORS['purple'],
                               (i * 200, 500), (i * 200 + 50, 600), 10)
        
        self.particles.update(0.016)
        self.particles.draw(screen)
        self.screen_shake.update()
        
        if self.phase == 0:
            s = render_text(self.font, "I'm alone now...", COLORS['white'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 100, 150))
        elif self.phase == 1:
            s = render_text(self.font, "The flower... it's glowing!", COLORS['white'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 150, 150))
        elif self.phase == 2:
            s = render_text(self.font, "Whispers... I hear whispers!", COLORS['red'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 180, 150))
        elif self.phase >= 3:
            s = render_text(self.font, "ELIAS...", COLORS['red'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 50, 150))
    
    def update(self, events: List[pygame.event.Event]):
        self.timer += 1
        if self.timer % 10 == 0:
            self.particles.add_spore(SCREEN_WIDTH // 2, 300, 1)
        
        if self.phase == 0 and self.timer > 120:
            self.phase = 1
        elif self.phase == 1 and self.timer > 180:
            self.phase = 2
            self.game.sanity.decrease_sanity(10)
        elif self.phase == 2 and self.timer % 60 == 0 and self.whisper_counter < 3:
            self.whisper_counter += 1
            self.game.sanity.decrease_sanity(15)
        elif self.phase == 2 and self.whisper_counter >= 3:
            self.phase = 3
        
        if self.phase >= 3:
            self.screen_shake.shake(20, 60)
            if self.timer > 300:
                self.game.current_scene = Scene5_Ending(self.game)


class Scene5_Ending(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.timer = 0
    
    def draw(self, screen: pygame.Surface):
        screen.fill(COLORS['black'])
        if self.timer < 100:
            s = render_text(self.font, "The Blooming...", COLORS['red'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        elif self.timer < 200:
            s = render_text(self.font, "END OF DAY 1", COLORS['white'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        else:
            s1 = render_text(self.font, "GAME OVER", COLORS['red'])
            s2 = render_text(make_font(24), "Press ESC to exit", COLORS['white'])
            screen.blit(s1, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
            screen.blit(s2, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30))
    
    def update(self, events: List[pygame.event.Event]):
        self.timer += 1
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.running = False


class Game:
    """Main game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Blooming")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.inventory = Inventory()
        self.dialogue = DialogueSystem(self.screen)
        self.journal = Journal()
        self.sanity = SanitySystem()
        self.particles = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.flags: Dict[str, Any] = {}
        
        self.journal.add_entry('entry1', 'First Day Notes',
                              'Arrived at Blackwood Research Facility.\n'
                              'Dr. Mara Vale gave me my access card.')
        
        self.journal.add_entry('entry2', 'X-17 Observation',
                              'Specimen X-17 is a mysterious flower.\n'
                              'After watering, it started glowing.')
        
        self.scenes = {
            'arrival': Scene1_Arrival(self),
            'orientation': Scene2_Orientation(self),
            'greenhouse': Scene3_Greenhouse(self),
            'blooming': Scene4_Blooming(self),
            'ending': Scene5_Ending(self)
        }
        
        self.current_scene = self.scenes['arrival']
        self.journal.unlock_entry('entry1')
        self._font20 = make_font(20)
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_i:
                        pass
                    elif event.key == pygame.K_j:
                        self.journal.active = not self.journal.active
            
            self.update(events)
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def update(self, events: List[pygame.event.Event]):
        self.current_scene.update(events)
        self.dialogue.update(events)
        self.sanity.update()
        if self.sanity.sanity <= 0:
            self.current_scene = self.scenes['blooming']
    
    def draw(self):
        self.current_scene.draw(self.screen)
        self.dialogue.draw()
        self.inventory.draw(self.screen)
        self.journal.draw(self.screen)
        self.sanity.draw(self.screen)
        for i, t in enumerate(["Click hotspots to interact", "ESC to quit, J for journal"]):
            s = render_text(self._font20, t, COLORS['white'])
            self.screen.blit(s, (20, SCREEN_HEIGHT - 30 + i * 25))


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
