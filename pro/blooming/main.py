"""Blooming - A 2D Point-and-Click Psychological Horror Game
Group 24 - CT029-3-2-Imaging and Special Effects

Entry point that wires together all scene modules and game systems.
"""

import pygame
import sys
import os

# Set base paths before importing other modules
_blooming_dir = os.path.dirname(__file__)
_assets_dir = os.path.join(_blooming_dir, 'assets', 'images')

from blooming.utils import set_base_dir, set_image_dir
set_base_dir(_blooming_dir)
set_image_dir(_assets_dir)

from blooming.utils.utils import render_text, make_font
from blooming.utils import COLORS
from blooming.utils.dialogue import DialogueSystem
from blooming.utils.inventory import Inventory
from blooming.utils.journal import Journal
from blooming.utils.sanity import SanitySystem
from blooming.scenes import (
    Scene1_Arrival,
    Scene2_Orientation,
    Scene3_Greenhouse,
    Scene4_Care,
    Scene5_Horror,
    Scene5_Ending,
)
from blooming.scenes.chapter_select import ChapterSelect
from blooming.scenes.title_screen import TitleScreen

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60


class Game:
    """Main game class that wires all systems together."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Blooming")
        self.clock = pygame.time.Clock()
        self.running = True

        # Core systems
        self.inventory = Inventory()
        self.dialogue = DialogueSystem(self.screen)
        self.journal = Journal()
        self.sanity = SanitySystem()

        # Game state
        self.flags = {}
        self.chapter_select = ChapterSelect(self.screen)
        self.title_screen = TitleScreen(self.screen)
        self.show_title = True

        # Initialize journal entries
        self.journal.add_entry('s1_card', 'Access Card',
                               'Received from Dr. Mara Vale.\n'
                               'Grants Level 1 access to greenhouse and office.')
        self.journal.add_entry('s2_rules', 'Greenhouse Rules',
                               '1. Do not remove anything without authorization.\n'
                               '2. Do not move any specimen unless told.')
        self.journal.add_entry('s3_x17', 'Specimen X-17',
                               'Unknown species.\nRecovered from undocumented forest.\n'
                               'Requires 500 ml filtered water daily.')

        # Build scene chain
        self.scenes = {
            'arrival': Scene1_Arrival(self),
            'orientation': Scene2_Orientation(self),
            'greenhouse': Scene3_Greenhouse(self),
            'care': Scene4_Care(self),
            'horror': None,  # created lazily
            'ending': None,  # created lazily
        }

        self.current_scene = self.scenes['arrival']
        self.journal.unlock_entry('s1_card')
        self._font20 = make_font(20)

    def _ensure_horror_scene(self):
        """Create horror scene on first transition."""
        if self.scenes['horror'] is None:
            self.scenes['horror'] = Scene5_Horror(self)
        if self.scenes['ending'] is None:
            self.scenes['ending'] = Scene5_Ending(self)

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            events = pygame.event.get()

            # Title screen mode
            if self.show_title:
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False

                choice = self.title_screen.update(events)
                self.title_screen.draw()
                pygame.display.flip()

                if choice == 'quit':
                    self.running = False
                elif choice == 'start':
                    self.show_title = False
                    self.show_chapter_select = True
                continue

            # Chapter select mode
            if self.show_chapter_select:
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

                choice = self.chapter_select.update(events)
                self.chapter_select.draw()
                pygame.display.flip()

                if choice == 'quit':
                    self.running = False
                elif choice:
                    self._start_chapter(choice)
                continue

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_j:
                        self.journal.active = not self.journal.active

            # Update
            self.dialogue.update(events)
            self.sanity.update()

            # Handle scene transitions
            prev_scene = self.current_scene
            self.current_scene.update(events)

            # Check if scene changed
            if self.current_scene is not prev_scene:
                scene_name = None
                for name, scene in self.scenes.items():
                    if scene is self.current_scene:
                        scene_name = name
                        break
                if scene_name == 'orientation':
                    self._ensure_horror_scene()
                elif scene_name == 'greenhouse':
                    self._ensure_horror_scene()
                elif scene_name == 'care':
                    self._ensure_horror_scene()

            # Sanity check
            if self.sanity.is_critical() and not isinstance(
                    self.current_scene, (Scene5_Horror, Scene5_Ending)):
                self._ensure_horror_scene()
                self.current_scene = self.scenes['horror']
                self.current_scene.phase = 2

            # Draw
            self.current_scene.draw(self.screen)
            self.dialogue.draw()
            self.inventory.draw(self.screen)
            self.journal.draw(self.screen)
            self.sanity.draw(self.screen)

            # Bottom hints
            hint1 = render_text(self._font20,
                                "Click hotspots to interact",
                                COLORS['white'])
            hint2 = render_text(self._font20,
                                "ESC to quit, J for journal",
                                COLORS['gray'])
            self.screen.blit(hint1, (20, SCREEN_HEIGHT - 30))
            self.screen.blit(hint2, (20, SCREEN_HEIGHT - 5))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _start_chapter(self, chapter_key: str):
        """Start a specific chapter."""
        self.show_chapter_select = False
        self.current_scene = self.scenes[chapter_key]
        self.journal.active = False

        # Reset scene state for re-entry
        if chapter_key == 'arrival':
            self.current_scene = Scene1_Arrival(self)
        elif chapter_key == 'orientation':
            self.current_scene = Scene2_Orientation(self)
        elif chapter_key == 'greenhouse':
            self.current_scene = Scene3_Greenhouse(self)
        elif chapter_key == 'care':
            self.current_scene = Scene4_Care(self)
            self._ensure_horror_scene()
        elif chapter_key == 'horror':
            self._ensure_horror_scene()
            self.scenes['horror'].phase = 0
            self.scenes['horror'].timer = 0
            self.scenes['horror'].response_given = False
            self.scenes['horror'].whisper_counter = 0
            self.current_scene = self.scenes['horror']


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
