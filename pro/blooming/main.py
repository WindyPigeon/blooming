"""
Blooming - A 2D Point-and-Click Psychological Horror Game
Group 24 - CT029-3-2-Imaging and Special Effects

This module contains all the game logic and systems.
"""

import pygame
import sys
import os
import math
from typing import Dict, List, Optional, Tuple, Any

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
IMAGE_DIR = os.path.join(BASE_DIR, '..', '..', '..', 'dev', 'concepts')

class ParticleSystem:
    def __init__(self):
        self.particles: List[Dict[str, Any]] = []
    
    def add_pollen(self, x: int, y: int, count: int = 5):
        for _ in range(count):
            angle = pygame.time.get_ticks() % 360
            speed = 0.5 + (pygame.time.get_ticks() % 2) * 0.2
            self.particles.append({
                'x': x,
                'y': y,
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
                'x': x,
                'y': y,
                'vx': speed * math.cos(math.radians(angle)),
                'vy': speed * math.sin(math.radians(angle)),
                'size': 3 + (pygame.time.get_ticks() % 4),
                'alpha': 255,
                'color': (200, 255, 200),
                'type': 'spore'
            })
    
    def add_glow(self, x: int, y: int, radius: int = 50):
        self.particles.append({
            'x': x,
            'y': y,
            'radius': radius,
            'max_radius': radius + 20,
            'pulse': 0,
            'color': (255, 255, 200),
            'type': 'glow'
        })
    
    def update(self, dt: float):
        for particle in self.particles[:]:
            if particle['type'] == 'pollen':
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['alpha'] -= 1
                if particle['alpha'] <= 0:
                    self.particles.remove(particle)
            
            elif particle['type'] == 'spore':
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['alpha'] -= 2
                if particle['alpha'] <= 0:
                    self.particles.remove(particle)
            
            elif particle['type'] == 'glow':
                particle['pulse'] += 0.1
                particle['alpha'] = int(128 + 127 * math.sin(particle['pulse']))
    
    def draw(self, screen: pygame.Surface):
        for particle in self.particles:
            if particle['type'] in ['pollen', 'spore']:
                s = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
                s.fill((*particle['color'][:3], particle['alpha']))
                screen.blit(s, (particle['x'], particle['y']))
            elif particle['type'] == 'glow':
                s = pygame.Surface((particle['radius'] * 2, particle['radius'] * 2), pygame.SRCALPHA)
                color_with_alpha = (*particle['color'][:3], particle['alpha'])
                pygame.draw.circle(s, color_with_alpha, (particle['radius'], particle['radius']), particle['radius'])
                screen.blit(s, (particle['x'] - particle['radius'], particle['y'] - particle['radius']))


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
    
    def apply(self, screen: pygame.Surface) -> pygame.Surface:
        if self.intensity > 0:
            shifted = screen.copy()
            screen.blit(shifted, (self.offset_x, self.offset_y))
        return screen


class DialogueSystem:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)
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
            if self.text_font.size(test_line)[0] <= max_width:
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
                    mouse_pos = pygame.mouse.get_pos()
                    for i, choice in enumerate(self.choices):
                        y_pos = 620 + i * 40
                        if 150 <= mouse_pos[0] <= SCREEN_WIDTH - 150 and y_pos <= mouse_pos[1] <= y_pos + 30:
                            self.choice_callback(choice)
                            self.current_dialogue = None
                            self.choices = []
    
    def draw(self):
        if not self.current_dialogue:
            return
        
        pygame.draw.rect(self.screen, COLORS['black'], self.box_rect)
        pygame.draw.rect(self.screen, COLORS['white'], self.box_rect, 2)
        
        speaker_text = self.font.render(self.current_dialogue['speaker'], True, COLORS['yellow'])
        self.screen.blit(speaker_text, (self.box_rect.x + 10, self.box_rect.y + 10))
        
        y_offset = self.box_rect.y + 50
        for line in self.current_dialogue['lines']:
            text_surface = self.text_font.render(line, True, COLORS['white'])
            self.screen.blit(text_surface, (self.box_rect.x + 10, y_offset))
            y_offset += 30
        
        y_offset = self.box_rect.y + 100
        for choice in self.choices:
            choice_rect = pygame.Rect(150, y_offset, SCREEN_WIDTH - 300, 30)
            pygame.draw.rect(self.screen, COLORS['gray'], choice_rect)
            choice_text = self.text_font.render(choice, True, COLORS['white'])
            self.screen.blit(choice_text, (choice_rect.x + 10, choice_rect.y + 5))
            y_offset += 40


class Inventory:
    def __init__(self):
        self.items: Dict[str, Dict[str, Any]] = {}
        self.selected: Optional[str] = None
    
    def add_item(self, item_id: str, name: str, description: str = "", used: bool = False):
        self.items[item_id] = {
            'name': name,
            'description': description,
            'used': used
        }
    
    def select(self, item_id: str) -> bool:
        if item_id in self.items:
            self.selected = item_id
            return True
        return False
    
    def use_item(self, item_id: str) -> bool:
        if item_id in self.items:
            self.items[item_id]['used'] = True
            return True
        return False
    
    def has_item(self, item_id: str) -> bool:
        return item_id in self.items
    
    def draw(self, screen: pygame.Surface):
        if not self.items:
            return
        
        inventory_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(screen, COLORS['black'], inventory_rect)
        pygame.draw.rect(screen, COLORS['white'], inventory_rect, 2)
        
        x_offset = 20
        for item_id, item_data in self.items.items():
            item_rect = pygame.Rect(x_offset, SCREEN_HEIGHT - 60, 60, 60)
            
            if self.selected == item_id:
                pygame.draw.rect(screen, COLORS['yellow'], item_rect, 3)
            
            pygame.draw.rect(screen, COLORS['gray'], item_rect)
            pygame.draw.rect(screen, COLORS['white'], item_rect, 1)
            
            name_text = pygame.font.Font(None, 16).render(
                item_data['name'], True, COLORS['white'])
            screen.blit(name_text, (x_offset, SCREEN_HEIGHT - 85))
            
            x_offset += 80


class Journal:
    def __init__(self):
        self.entries: Dict[str, Dict[str, str]] = {}
        self.active = False
    
    def add_entry(self, entry_id: str, title: str, content: str):
        self.entries[entry_id] = {
            'title': title,
            'content': content,
            'unlocked': False
        }
    
    def unlock_entry(self, entry_id: str):
        if entry_id in self.entries:
            self.entries[entry_id]['unlocked'] = True
    
    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        
        journal_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        pygame.draw.rect(screen, COLORS['black'], journal_rect)
        pygame.draw.rect(screen, COLORS['white'], journal_rect, 3)
        
        y_offset = journal_rect.y + 20
        for entry_id, entry_data in self.entries.items():
            if entry_data['unlocked']:
                title_text = pygame.font.Font(None, 28).render(
                    entry_data['title'], True, COLORS['yellow'])
                screen.blit(title_text, (journal_rect.x + 20, y_offset))
                
                content_lines = entry_data['content'].split('\n')
                y_offset += 35
                for line in content_lines:
                    content_text = pygame.font.Font(None, 20).render(
                        line, True, COLORS['white'])
                    screen.blit(content_text, (journal_rect.x + 30, y_offset))
                    y_offset += 25
                
                y_offset += 30


class SanitySystem:
    def __init__(self):
        self.sanity = 100
        self.max_sanity = 100
        self.hallucination_level = 0
        self.hallucination_timer = 0
    
    def decrease_sanity(self, amount: int = 10):
        self.sanity = max(0, self.sanity - amount)
        self.hallucination_level = (100 - self.sanity) // 20
    
    def update(self):
        self.hallucination_timer += 1
    
    def is_hallucinating(self) -> bool:
        return self.sanity < 50
    
    def draw(self, screen: pygame.Surface):
        meter_rect = pygame.Rect(20, 20, 200, 20)
        pygame.draw.rect(screen, COLORS['dark_gray'], meter_rect)
        pygame.draw.rect(screen, COLORS['white'], meter_rect, 2)
        
        fill_width = int((self.sanity / self.max_sanity) * 196)
        fill_color = COLORS['green'] if self.sanity > 50 else COLORS['red']
        pygame.draw.rect(screen, fill_color, 
                        (meter_rect.x + 2, meter_rect.y + 2, fill_width, 16))
        
        text = pygame.font.Font(None, 20).render(f"Sanity: {self.sanity}%", True, COLORS['white'])
        screen.blit(text, (meter_rect.x + 220, 20))
        
        if self.is_hallucinating() and self.hallucination_timer % 120 < 60:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = int(50 + 50 * (self.hallucination_level / 3))
            overlay.fill((100, 0, 0, alpha))
            screen.blit(overlay, (0, 0))


class Scene:
    def __init__(self, game: 'Game'):
        self.game = game
        self.font = pygame.font.Font(None, 32)
        self.hotspots: Dict[str, Dict[str, Any]] = {}
        self.active = True
        self.particle_system = ParticleSystem()
    
    def update(self, events: List[pygame.event.Event]):
        pass
    
    def draw(self, screen: pygame.Surface):
        pass
    
    def add_hotspot(self, name: str, rect: pygame.Rect, description: str = ""):
        self.hotspots[name] = {
            'rect': rect,
            'description': description,
            'active': True
        }
    
    def handle_hotspot_click(self, pos: Tuple[int, int]) -> Optional[str]:
        if not self.active:
            return None
        
        for name, hotspot in self.hotspots.items():
            if hotspot['active'] and hotspot['rect'].collidepoint(pos):
                return name
        return None
    
    def update_particles(self):
        self.particle_system.update(0.016)


def load_image(path: str) -> Optional[pygame.Surface]:
    full_path = os.path.join(IMAGE_DIR, path)
    if os.path.exists(full_path):
        return pygame.image.load(full_path).convert_alpha()
    return None


class Scene1_Arrival(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.background_image = load_image('greenhouse/greenhouse-exterior.png')
        
        self.add_hotspot('sign', pygame.Rect(100, 100, 150, 80), "Blackwood Research Facility")
        self.add_hotspot('intercom', pygame.Rect(800, 300, 100, 100), "Security intercom")
        self.add_hotspot('door', pygame.Rect(400, 250, 224, 318), "Security door")
        self.add_hotspot('door_panel', pygame.Rect(650, 300, 50, 100), "Security panel")
        self.add_hotspot('mara', pygame.Rect(500, 300, 100, 200), "Dr. Mara Vale")
        
        self.door_locked = True
        self.access_card_found = False
        self.access_card_selected = False
        self.entered = False
    
    def draw(self, screen: pygame.Surface):
        if self.entered:
            return
        
        if self.background_image:
            screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        else:
            screen.fill(COLORS['dark_gray'])
        
        instructions = [
            "Click hotspots to interact",
            "Talk to Mara to get access card"
        ]
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 24).render(instruction, True, COLORS['white'])
            screen.blit(text, (20, SCREEN_HEIGHT - 40 + i * 25))
    
    def update(self, events: List[pygame.event.Event]):
        if self.entered:
            return
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                hotspot_name = self.handle_hotspot_click(event.pos)
                
                if hotspot_name == 'door':
                    if self.door_locked and not self.access_card_found:
                        self.game.dialogue.show_dialogue(
                            "The door is locked. I need my access card.",
                            "Elias"
                        )
                
                elif hotspot_name == 'door_panel' and self.door_locked:
                    if not self.access_card_selected:
                        self.game.dialogue.show_dialogue(
                            "Access denied. Please use your access card.",
                            "Intercom"
                        )
                    elif self.access_card_selected:
                        self.door_locked = False
                        self.access_card_selected = False
                        self.game.dialogue.show_dialogue(
                            "Access granted.",
                            "Intercom",
                            ["Enter facility"],
                            lambda choice: self.enter_facility()
                        )
                
                elif hotspot_name == 'intercom':
                    self.game.dialogue.show_dialogue(
                        "Security intercom is active.",
                        "Elias",
                        ["Try to open door"],
                        lambda choice: self.game.dialogue.show_dialogue(
                            "Access denied. Please use your access card.",
                            "Intercom"
                        )
                    )
                
                elif hotspot_name == 'mara':
                    if not self.access_card_found:
                        self.game.dialogue.show_dialogue(
                            "Mara holds out an access card.",
                            "Mara",
                            ["Take the card"],
                            lambda choice: self.take_card()
                        )
                
                elif hotspot_name == 'sign':
                    self.game.dialogue.show_dialogue(
                        "Blackwood Research Facility.\nA long way from the university greenhouse.",
                        "Elias"
                    )
    
    def take_card(self):
        self.game.inventory.add_item('access_card', 'Level 1 Access Card', 'Grants access to greenhouse')
        self.access_card_found = True
        self.game.dialogue.show_dialogue(
            "I received my access card.",
            "Elias",
            ["Select access card"],
            lambda choice: self.select_card()
        )
    
    def select_card(self):
        if self.game.inventory.select('access_card'):
            self.access_card_selected = True
            self.game.dialogue.show_dialogue(
                "Access card selected. Use it on the security panel.",
                "Elias"
            )
    
    def enter_facility(self):
        self.entered = True
        self.game.current_scene = Scene2_Orientation(self.game)


class Scene2_Orientation(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.background_image = load_image('greenhouse/greenhouse-exterior.png')
        
        self.add_hotspot('restricted_lab', pygame.Rect(100, 200, 150, 300), "Restricted Laboratory")
        self.add_hotspot('staff_office', pygame.Rect(350, 200, 150, 300), "Staff Office")
        self.add_hotspot('storage', pygame.Rect(600, 200, 150, 300), "Storage")
        self.add_hotspot('greenhouse_door', pygame.Rect(850, 200, 150, 300), "Greenhouse")
        self.add_hotspot('mara', pygame.Rect(500, 350, 100, 150), "Dr. Mara Vale")
        
        self.mara_leaving = False
        self.greenhouse_open = False
    
    def draw(self, screen: pygame.Surface):
        if self.background_image:
            screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        else:
            screen.fill(COLORS['dark_gray'])
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                hotspot_name = self.handle_hotspot_click(event.pos)
                
                if hotspot_name == 'restricted_lab':
                    self.game.dialogue.show_dialogue(
                        "Restricted Laboratory. I need higher clearance.",
                        "Elias"
                    )
                
                elif hotspot_name == 'mara' and not self.mara_leaving:
                    self.game.dialogue.show_dialogue(
                        "Before we go inside, one rule. Don't remove anything from the greenhouse without authorization.",
                        "Mara",
                        ["Understood"],
                        lambda choice: self.follow_mara()
                    )
                
                elif hotspot_name == 'greenhouse_door' and not self.mara_leaving:
                    self.mara_leaving = True
                    self.greenhouse_open = True
                    self.game.dialogue.show_dialogue(
                        "Mara scans her card and opens the greenhouse door.",
                        "Mara",
                        ["Enter greenhouse"],
                        lambda choice: self.enter_greenhouse()
                    )
    
    def follow_mara(self):
        self.game.dialogue.show_dialogue(
            "Come on.",
            "Mara"
        )
    
    def enter_greenhouse(self):
        self.game.current_scene = Scene3_Greenhouse(self.game)


class Scene3_Greenhouse(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.background_image = load_image('greenhouse/greenhouse-interior.png')
        self.flower_image = load_image('flower/flower.png')
        self.heart_image = load_image('heart.png')
        
        self.add_hotspot('watering_can', pygame.Rect(100, 400, 80, 80), "Watering can")
        self.add_hotspot('sink', pygame.Rect(250, 400, 80, 80), "Filtered water sink")
        self.add_hotspot('clipboard', pygame.Rect(400, 400, 80, 80), "Care instructions")
        self.add_hotspot('thermometer', pygame.Rect(550, 400, 60, 120), "Greenhouse thermometer")
        self.add_hotspot('cabinet', pygame.Rect(700, 400, 80, 80), "Storage cabinet")
        self.add_hotspot('journal', pygame.Rect(850, 400, 80, 80), "Old research journal")
        self.add_hotspot('x17', pygame.Rect(450, 250, 120, 120), "Specimen X-17")
        self.add_hotspot('mara', pygame.Rect(500, 350, 100, 150), "Dr. Mara Vale")
        
        self.watering_can_held = False
        self.watering_can_filled = False
        self.water_amount = 0
        self.x17_interacted = False
        self.journal_locked = True
        self.watering_can_selected = False
    
    def draw(self, screen: pygame.Surface):
        if self.background_image:
            screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        
        if self.flower_image and self.x17_interacted:
            screen.blit(pygame.transform.scale(self.flower_image, (120, 120)), (450, 250))
        
        if self.heart_image and self.game.flags.get('X17_GLOW', False):
            screen.blit(pygame.transform.scale(self.heart_image, (60, 60)), (480, 310))
        
        if not self.x17_interacted and self.heart_image:
            screen.blit(pygame.transform.scale(self.heart_image, (120, 120)), (450, 250))
        
        self.update_particles()
        self.particle_system.draw(screen)
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                hotspot_name = self.handle_hotspot_click(event.pos)
                
                if hotspot_name == 'watering_can' and not self.watering_can_held:
                    self.watering_can_held = True
                    self.game.inventory.add_item('empty_watering_can', 'Empty Watering Can', 'Can be filled at the sink')
                
                elif hotspot_name == 'watering_can' and self.watering_can_held and not self.watering_can_filled:
                    self.game.dialogue.show_dialogue(
                        "The watering can is empty.",
                        "Elias",
                        ["Fill with filtered water"],
                        lambda choice: self.fill_watering_can()
                    )
                
                elif hotspot_name == 'watering_can' and self.watering_can_held and self.watering_can_filled:
                    self.game.dialogue.show_dialogue(
                        "Watering can filled with 500ml.",
                        "Elias",
                        ["Select watering can"],
                        lambda choice: self.select_watering_can()
                    )
                
                elif hotspot_name == 'sink':
                    self.game.dialogue.show_dialogue(
                        "Filtered water system. Perfect for specimen care.",
                        "Elias"
                    )
                
                elif hotspot_name == 'clipboard':
                    self.game.dialogue.show_dialogue(
                        "SPECIMEN X-17\n\nDAILY CARE PROCEDURE\n1. Confirm greenhouse temperature: 23-25 degrees Celsius.\n2. Inspect specimen for physical abnormalities.\n3. Provide 500 ml filtered water.\n4. Record unusual reactions.\n5. Do not relocate the specimen.",
                        "Care Instructions"
                    )
                
                elif hotspot_name == 'thermometer':
                    self.game.dialogue.show_dialogue(
                        "Greenhouse temperature: 24 degrees Celsius. Optimal range.",
                        "Elias"
                    )
                
                elif hotspot_name == 'cabinet':
                    self.game.dialogue.show_dialogue(
                        "Storage cabinet. Contains general supplies.",
                        "Elias"
                    )
                
                elif hotspot_name == 'journal' and self.journal_locked:
                    self.game.dialogue.show_dialogue(
                        "An old research journal. Dr. Vale says to leave it.",
                        "Elias"
                    )
                
                elif hotspot_name == 'journal' and not self.journal_locked:
                    self.game.dialogue.show_dialogue(
                        "Old research notes from X-17.",
                        "Elias"
                    )
                
                elif hotspot_name == 'mara':
                    self.game.dialogue.show_dialogue(
                        "Come here. There's something you need to see.",
                        "Mara"
                    )
                
                elif hotspot_name == 'x17' and not self.x17_interacted:
                    self.game.dialogue.show_dialogue(
                        "Specimen X-17. A rare, mysterious flower.",
                        "Elias",
                        ["Inspect X-17"],
                        lambda choice: self.inspect_x17()
                    )
                
                elif hotspot_name == 'x17' and self.x17_interacted:
                    self.game.dialogue.show_dialogue(
                        "X-17 is waiting.",
                        "Elias"
                    )
    
    def fill_watering_can(self):
        self.watering_can_filled = True
        self.water_amount = 500
        self.game.inventory.items['empty_watering_can']['name'] = 'Watering Can (500ml)'
        self.game.dialogue.show_dialogue(
            "Filled with 500ml of filtered water.",
            "Elias"
        )
    
    def select_watering_can(self):
        if self.watering_can_filled:
            if self.game.inventory.select('empty_watering_can'):
                self.watering_can_selected = True
                self.game.dialogue.show_dialogue(
                    "Watering can with 500ml selected. Use on X-17.",
                    "Elias"
                )
    
    def inspect_x17(self):
        self.x17_interacted = True
        self.game.dialogue.show_dialogue(
            "This is why you're here.",
            "Mara",
            ["It looks dangerous.", "It's beautiful.", "It looks unusual."],
            lambda choice: self.x17_inspection_choice(choice)
        )
    
    def x17_inspection_choice(self, choice: str):
        if choice == "It looks dangerous.":
            self.game.flags['FIRST_IMPRESSION'] = 'DANGEROUS'
            self.game.dialogue.show_dialogue(
                "I expected something more dangerous.",
                "Elias",
                ["Dr. Vale response"],
                lambda _: self.game.dialogue.show_dialogue(
                    "Appearances are unreliable.",
                    "Mara"
                )
            )
        elif choice == "It's beautiful.":
            self.game.flags['FIRST_IMPRESSION'] = 'BEAUTIFUL'
            self.game.dialogue.show_dialogue(
                "It's beautiful.",
                "Elias",
                ["Dr. Vale response"],
                lambda _: self.game.dialogue.show_dialogue(
                    "Careful with that word.",
                    "Mara"
                )
            )
        elif choice == "It looks unusual.":
            self.game.flags['FIRST_IMPRESSION'] = 'UNUSUAL'
            self.game.dialogue.show_dialogue(
                "It looks unusual.",
                "Elias",
                ["Dr. Vale response"],
                lambda _: self.game.dialogue.show_dialogue(
                    "Give it time.",
                    "Mara"
                )
            )
        
        self.game.dialogue.show_dialogue(
            "Before you do anything... Inspect it. What are you looking for?",
            "Mara"
        )
    
    def water_x17(self):
        if not self.watering_can_filled:
            self.game.dialogue.show_dialogue(
                "I need to fill the watering can first.",
                "Elias"
            )
            return
        
        self.game.dialogue.show_dialogue(
            "I watered X-17. Nothing happened immediately.",
            "Elias"
        )
        self.watering_can_filled = False
        self.game.inventory.items['empty_watering_can']['name'] = 'Empty Watering Can'
        self.game.flags['X17_WATERED'] = True
        self.game.journal.unlock_entry('entry2')
    
    def complete_observation(self):
        self.game.flags['OBSERVATION_COMPLETE'] = True
        self.game.current_scene = Scene4_Blooming(self.game)


class Scene4_Blooming(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.phase = 0
        self.timer = 0
        self.whisper_counter = 0
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.glow_effect = False
        self.whispers_triggered = False
        self.background_image = load_image('greenhouse/greenhouse-interior.png')
        self.flower_image = load_image('flower/flower.png')
        self.heart_image = load_image('heart.png')
    
    def draw(self, screen: pygame.Surface):
        if self.background_image:
            screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        
        if self.phase >= 1 and self.flower_image:
            pulse = 100 + 50 * math.sin(self.timer * 0.1)
            glow_color = (255, 255, int(pulse))
            flower_scaled = pygame.transform.scale(self.flower_image, (150, 150))
            
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*glow_color, 100), (100, 100), 100)
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - 100, 200))
            screen.blit(flower_scaled, (SCREEN_WIDTH // 2 - 75, 200))
            
            self.particle_system.add_pollen(SCREEN_WIDTH // 2, 300, 3)
        
        if self.phase >= 2 and self.heart_image:
            heart_scaled = pygame.transform.scale(self.heart_image, (80, 80))
            screen.blit(heart_scaled, (SCREEN_WIDTH // 2 - 40, 310))
        
        self.particle_system.update(0.016)
        self.particle_system.draw(screen)
        
        self.screen_shake.update()
        
        if self.phase == 0:
            text = self.font.render("I'm alone now...", True, COLORS['white'])
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, 200))
        
        elif self.phase == 1:
            text = self.font.render("The flower... it's glowing!", True, COLORS['white'])
            screen.blit(text, (SCREEN_WIDTH // 2 - 150, 200))
        
        elif self.phase == 2:
            text = self.font.render("Whispers... I hear whispers!", True, COLORS['red'])
            screen.blit(text, (SCREEN_WIDTH // 2 - 180, 200))
        
        elif self.phase >= 3:
            text = self.font.render("ELIAS...", True, COLORS['red'])
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, 200))
    
    def update(self, events: List[pygame.event.Event]):
        self.timer += 1
        
        if self.phase == 0 and self.timer > 120:
            self.phase = 1
            self.glow_effect = True
            self.game.flags['X17_GLOW'] = True
            self.game.dialogue.show_dialogue(
                "The flower is glowing...",
                "Elias"
            )
        
        elif self.phase == 1 and self.timer > 180:
            self.phase = 2
            self.whisper_counter = 0
            self.whispers_triggered = True
        
        elif self.phase == 2 and self.timer % 60 == 0 and self.whisper_counter < 3:
            self.whisper_counter += 1
            self.game.sanity.decrease_sanity(15)
            whisper_texts = [
                "Don't leave me...",
                "I need you...",
                "Elias..."
            ]
            self.game.dialogue.show_dialogue(
                whisper_texts[self.whisper_counter - 1],
                "Unknown",
                ["Look at the flower"],
                lambda choice: None
            )
        
        if self.phase >= 2 and self.whispers_triggered:
            self.whispers_triggered = False
            self.game.dialogue.show_dialogue(
                "Don't go...",
                "Unknown",
                ["Look at X-17", "Try to leave", "Intercom"],
                lambda choice: self.handle_horror_response(choice)
            )
        
        if self.phase >= 3:
            self.screen_shake.shake(20, 60)
            if self.timer > 300:
                self.game.current_scene = Scene5_Ending(self.game)
        
        if self.phase >= 1:
            self.particle_system.add_spore(SCREEN_WIDTH // 2, 300, 2)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.phase >= 2:
                    hotspot_name = self.handle_hotspot_click(event.pos)
                    if hotspot_name == 'x17':
                        self.game.dialogue.show_dialogue(
                            "The glow pulses once. Silence.",
                            "Elias"
                        )
    
    def handle_horror_response(self, choice: str):
        if choice == "Look at the flower":
            self.game.flags['FIRST_HORROR_RESPONSE'] = 'FLOWER'
            self.game.dialogue.show_dialogue(
                "I'm talking to a plant.",
                "Elias"
            )
        elif choice == "Try to leave":
            self.game.flags['FIRST_HORROR_RESPONSE'] = 'ESCAPE'
            self.game.dialogue.show_dialogue(
                "Don't go...",
                "Unknown"
            )
            self.game.sanity.decrease_sanity(20)
        elif choice == "Intercom":
            self.game.flags['FIRST_HORROR_RESPONSE'] = 'INTERCOM'
            self.game.dialogue.show_dialogue(
                "I'm here.",
                "Mara (through intercom)"
            )
        
        self.phase = 3


class Scene5_Ending(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.timer = 0
        self.background_image = load_image('greenhouse/greenhouse-exterior.png')
    
    def draw(self, screen: pygame.Surface):
        if self.background_image:
            screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        
        if self.timer < 100:
            text = self.font.render("The Blooming...", True, COLORS['red'])
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        elif self.timer < 200:
            text = self.font.render("END OF DAY 1", True, COLORS['white'])
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        else:
            text1 = self.font.render("GAME OVER", True, COLORS['red'])
            text2 = self.font.render("Press ESC to exit", True, COLORS['white'])
            screen.blit(text1, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
            screen.blit(text2, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30))
    
    def update(self, events: List[pygame.event.Event]):
        self.timer += 1
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.running = False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Blooming")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.inventory = Inventory()
        self.dialogue = DialogueSystem(self.screen)
        self.journal = Journal()
        self.sanity = SanitySystem()
        self.screen_shake = ScreenShake()
        self.flags: Dict[str, Any] = {}
        
        self.journal.add_entry('entry1', 'First Day Notes', 
                              'I arrived at Blackwood Research Facility today.\n'
                              'Dr. Mara Vale gave me my access card.\n'
                              'She warned me not to move any specimens.')
        
        self.journal.add_entry('entry2', 'X-17 Observation',
                              'Specimen X-17 is a mysterious flower.\n'
                              'It appeared pale and closed initially.\n'
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
                        self.show_inventory()
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
        self.current_scene.update_particles()
        
        if self.sanity.sanity <= 0:
            self.current_scene = self.scenes['blooming']
    
    def draw(self):
        self.current_scene.draw(self.screen)
        self.dialogue.draw()
        self.inventory.draw(self.screen)
        self.journal.draw(self.screen)
        self.sanity.draw(self.screen)
        
        instructions = [
            "Click hotspots to interact",
            "Press 'I' for inventory, 'J' for journal, 'ESC' to quit"
        ]
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 20).render(instruction, True, COLORS['white'])
            self.screen.blit(text, (20, SCREEN_HEIGHT - 30 + i * 25))
    
    def show_inventory(self):
        pass


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
