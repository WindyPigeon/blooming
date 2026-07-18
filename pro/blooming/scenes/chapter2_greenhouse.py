"""Chapter 3 - Greenhouse Exploration (Member B)

Player explores the greenhouse, finds the watering can,
reads care instructions, and meets Specimen X-17.
Includes the observation tutorial (inspect petals, stem, soil).
"""

import math
import pygame
from blooming.utils.utils import render_text, make_font, load_image, scale_image_keep_ratio
from blooming.utils import COLORS
from blooming.utils.particles import ParticleSystem


class Chapter2_Greenhouse:
    """Chapter 2: Greenhouse exploration and X-17 introduction."""

    def __init__(self, game):
        self.game = game
        self.font = make_font(32)
        self.small_font = make_font(24)
        self.small_font2 = make_font(18)

        # Hotspot rects
        self.watering_can_rect = pygame.Rect(100, 400, 80, 80)
        self.sink_rect = pygame.Rect(250, 400, 80, 80)
        self.clipboard_rect = pygame.Rect(400, 400, 80, 80)
        self.thermometer_rect = pygame.Rect(900, 100, 60, 120)
        self.cabinet_rect = pygame.Rect(800, 400, 80, 80)
        self.journal_rect = pygame.Rect(700, 400, 80, 80)
        self.x17_rect = pygame.Rect(450, 250, 120, 120)
        self.mara_rect = pygame.Rect(162, 30, 700, 708)

        # Greenhouse intro state
        self.intro_dialogue_done = False
        self.intro_lines = [
            ("Go ahead.", "Mara"),
            ("Go ahead with what?", "Elias"),
            ("Look around.", "Mara"),
            ("If you're going to work here,\nlearn where everything is.", "Mara"),
        ]
        self.intro_idx = 0
        self.mara_arrived_table = False

        # Mara fade-out state
        self.mara_fading = False
        self.mara_fade_timer = 0.0
        self.mara_fade_duration = 2.0

        # State
        self.watering_can_held = False
        self.watering_can_filled = False
        self.x17_interacted = False
        self.x17_watered = False
        self.mara_left = False
        self.clipboard_read = False
        self.journal_closed = False
        self.entered = False
        self.phase = 'greenhouse_intro'
        self.particles = ParticleSystem()

        # Dialogue queue for non-choice dialogues
        self.dialogue_queue = []
        self.dialogue_idx = 0
        self.dialogue_playing = False
        self.pending_transition = False

        # Images
        self.interior_img = load_image('backgrounds/greenhouse-interior.png')
        self.flower_img = load_image('props/flower.png')
        self.watering_can_img = load_image('props/watering-can.png')
        self.sink_img = load_image('props/sink.png')
        self.clipboard_img = load_image('props/clipboard.png')
        self.cabinet_img = load_image('props/storage-cabinet.png')
        self.thermometer_img = load_image('props/thermometer.png')
        self.journal_img = load_image('props/old-journal.png')
        self.mara_img = load_image('char/mara-vale.png')
        self.specimen_table_img = load_image('props/specimen-table.png')

        # Observation state
        self.observation_active = False
        self.observed_petals = False
        self.observed_stem = False
        self.observed_soil = False
        self.first_impression = None

        # Care sheet display
        self.showing_care_sheet = False

    @property
    def active(self):
        return self.phase != 'entered'

    def draw(self, screen):
        """Draw the greenhouse scene."""
        if self.phase == 'entered':
            return

        # Background
        if self.interior_img:
            bg_scaled, bx, by = scale_image_keep_ratio(self.interior_img, 1024, 768)
            screen.blit(bg_scaled, (bx, by))
        else:
            screen.fill((30, 60, 30))
            # Glass ceiling lines
            for x in range(0, 1024, 100):
                pygame.draw.line(screen, (80, 100, 80),
                                 (x, 0), (x, 250), 2)
            # Arc of ceiling
            pygame.draw.arc(screen, (80, 100, 80),
                            (0, 100, 1024, 300),
                            3.14, 0, 10)

        # Rows of plants (background)
        for i in range(0, 1024, 150):
            pygame.draw.rect(screen, (20, 80, 20), (i, 350, 60, 100))
            pygame.draw.rect(screen, (40, 120, 40),
                             (i + 10, 340, 40, 20))

        # Watering can
        if not self.watering_can_held:
            if self.watering_can_img:
                scaled, sx, sy = scale_image_keep_ratio(self.watering_can_img, 80, 80)
                screen.blit(scaled, (self.watering_can_rect.x + sx,
                                     self.watering_can_rect.y + sy))
            else:
                pygame.draw.rect(screen, COLORS['orange'],
                                 self.watering_can_rect)
                pygame.draw.rect(screen, COLORS['white'],
                                 self.watering_can_rect, 1)

        # Sink
        if self.sink_img:
            scaled, sx, sy = scale_image_keep_ratio(self.sink_img, 80, 80)
            screen.blit(scaled, (self.sink_rect.x + sx, self.sink_rect.y + sy))
        else:
            pygame.draw.rect(screen, COLORS['blue'], self.sink_rect)
            pygame.draw.rect(screen, COLORS['white'], self.sink_rect, 1)

        # Clipboard
        if self.clipboard_img:
            scaled, sx, sy = scale_image_keep_ratio(self.clipboard_img, 80, 80)
            screen.blit(scaled, (self.clipboard_rect.x + sx,
                                 self.clipboard_rect.y + sy))
        else:
            pygame.draw.rect(screen, COLORS['yellow'], self.clipboard_rect)
            pygame.draw.rect(screen, COLORS['white'],
                             self.clipboard_rect, 1)

        # Thermometer
        if self.thermometer_img:
            scaled, sx, sy = scale_image_keep_ratio(self.thermometer_img, 60, 120)
            screen.blit(scaled, (self.thermometer_rect.x + sx,
                                 self.thermometer_rect.y + sy))
        else:
            pygame.draw.rect(screen, COLORS['gray'], self.thermometer_rect)
            pygame.draw.rect(screen, COLORS['white'],
                             self.thermometer_rect, 1)
            temp_surf = render_text(make_font(12), "24°C",
                                    COLORS['red'])
            screen.blit(temp_surf, (910, 160))

        # Cabinet
        if self.cabinet_img:
            scaled, sx, sy = scale_image_keep_ratio(self.cabinet_img, 80, 80)
            screen.blit(scaled, (self.cabinet_rect.x + sx,
                                 self.cabinet_rect.y + sy))
        else:
            pygame.draw.rect(screen, COLORS['dark_gray'], self.cabinet_rect)
            pygame.draw.rect(screen, COLORS['white'],
                             self.cabinet_rect, 1)

        # Journal
        if not self.journal_closed and self.journal_img:
            scaled, sx, sy = scale_image_keep_ratio(self.journal_img, 80, 80)
            screen.blit(scaled, (self.journal_rect.x + sx,
                                 self.journal_rect.y + sy))
        elif not self.journal_closed:
            pygame.draw.rect(screen, COLORS['brown'], self.journal_rect)
            pygame.draw.rect(screen, COLORS['white'],
                             self.journal_rect, 1)

        # Central specimen table
        table_rect = pygame.Rect(400, 370, 220, 130)
        if self.specimen_table_img:
            table_scaled, tx, ty = scale_image_keep_ratio(
                self.specimen_table_img, table_rect.width, table_rect.height)
            screen.blit(table_scaled, (table_rect.x + tx, table_rect.y + ty))
        else:
            pygame.draw.rect(screen, (100, 80, 60), table_rect)
            pygame.draw.rect(screen, (130, 110, 80),
                             pygame.Rect(405, 375, 210, 120))

        # X-17 flower
        if self.flower_img:
            flower_scaled, fx, fy = scale_image_keep_ratio(self.flower_img, 120, 120)
            screen.blit(flower_scaled, (460 + fx, 260 + fy))
        else:
            pygame.draw.rect(screen, COLORS['pink'], (460, 260, 120, 120))

        # X-17 glow after watering
        if self.x17_watered:
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pulse = 100 + 50 * math.sin(pygame.time.get_ticks() * 0.003)
            pygame.draw.circle(glow_surf,
                               (255, 255, 200, int(pulse)),
                               (100, 100), 100)
            screen.blit(glow_surf, (410, 210))

        # Label
        label_surf = render_text(make_font(14), "SPECIMEN X-17",
                                 COLORS['white'])
        screen.blit(label_surf, (465, 380))

        # Mara (with fade-out)
        if not self.mara_left:
            if self.mara_fading:
                alpha = int(255 * (1 - self.mara_fade_timer / self.mara_fade_duration))
                alpha = max(0, alpha)
                if alpha > 0 and self.mara_img:
                    mara_scaled, mfx, mfy = scale_image_keep_ratio(self.mara_img, 700, 700)
                    mara_alpha_surf = pygame.Surface(mara_scaled.get_size(), pygame.SRCALPHA)
                    mara_alpha_surf.blit(mara_scaled, (0, 0))
                    mara_alpha_surf.set_alpha(alpha)
                    screen.blit(mara_alpha_surf, (162 + mfx, mfy))
                    mara_lbl = render_text(make_font(14), "Mara",
                                            COLORS['white'])
                    screen.blit(mara_lbl, (262, 600))
                elif alpha > 0:
                    mara_surf = pygame.Surface((80, 180), pygame.SRCALPHA)
                    mara_surf.set_alpha(alpha)
                    pygame.draw.circle(mara_surf, COLORS['blue'], (40, 60), 30)
                    pygame.draw.rect(mara_surf, COLORS['blue'],
                                     pygame.Rect(10, 80, 60, 100))
                    screen.blit(mara_surf, (162, 300))
                    mara_lbl = render_text(make_font(14), "Mara",
                                            COLORS['white'])
                    screen.blit(mara_lbl, (262, 490))
            else:
                if self.mara_img:
                    mara_scaled, mfx, mfy = scale_image_keep_ratio(self.mara_img, 700, 700)
                    screen.blit(mara_scaled, (162 + mfx, mfy))
                    mara_lbl = render_text(make_font(14), "Mara",
                                            COLORS['white'])
                    screen.blit(mara_lbl, (262, 600))
                else:
                    mara_surf = pygame.Surface((80, 180), pygame.SRCALPHA)
                    pygame.draw.circle(mara_surf, COLORS['blue'], (40, 60), 30)
                    pygame.draw.rect(mara_surf, COLORS['blue'],
                                     pygame.Rect(10, 80, 60, 100))
                    screen.blit(mara_surf, (162, 300))
                    mara_lbl = render_text(make_font(14), "Mara",
                                            COLORS['white'])
                    screen.blit(mara_lbl, (262, 490))

        # Observation overlay
        if self.observation_active:
            self._draw_observation(screen)

        # Care sheet overlay
        if self.showing_care_sheet:
            self._draw_care_sheet(screen)

        # Particles
        self.particles.update(0.016)
        self.particles.draw(screen)

        # Objective hint after intro
        if self.intro_dialogue_done and self.phase == 'explore' and not self.game.flags.get('objective_hint_shown', False):
            obj_surf = render_text(make_font(28), "EXPLORE THE GREENHOUSE", COLORS['yellow'])
            screen.blit(obj_surf, (1024 // 2 - obj_surf.get_width() // 2, 50))
            hint_surf = render_text(make_font(18), "Click on objects to interact", COLORS['white'])
            screen.blit(hint_surf, (1024 // 2 - hint_surf.get_width() // 2, 90))
            self.game.flags['objective_hint_shown'] = True

    def _draw_observation(self, screen):
        """Draw observation mode UI."""
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # Hotspots for inspection
        inspection_points = [
            (460, 260, "PETALS"),
            (510, 310, "STEM"),
            (510, 380, "SOIL"),
        ]
        for px, py, label in inspection_points:
            rect = pygame.Rect(px, py, 80, 40)
            pygame.draw.rect(screen, COLORS['yellow'], rect)
            pygame.draw.rect(screen, COLORS['white'], rect, 1)
            lbl = render_text(make_font(12), label, COLORS['black'])
            screen.blit(lbl, (px + 5, py + 10))

    def _draw_care_sheet(self, screen):
        """Draw the X-17 care instructions document."""
        rect = pygame.Rect(250, 100, 524, 500)
        pygame.draw.rect(screen, COLORS['white'], rect)
        pygame.draw.rect(screen, COLORS['black'], rect, 3)

        y_off = 130
        title = render_text(make_font(28), "SPECIMEN X-17",
                            COLORS['black'])
        screen.blit(title, (rect.x + 20, y_off))
        y_off += 40
        subtitle = render_text(make_font(24), "DAILY CARE PROCEDURE",
                               COLORS['gray'])
        screen.blit(subtitle, (rect.x + 20, y_off))
        y_off += 50

        lines = [
            "1. Confirm greenhouse temperature: 23-25°C",
            "2. Inspect specimen for physical abnormalities",
            "3. Provide 500 ml filtered water",
            "4. Record unusual reactions",
            "5. Do not relocate the specimen",
        ]
        for line in lines:
            s = render_text(make_font(20), line, COLORS['black'])
            screen.blit(s, (rect.x + 30, y_off))
            y_off += 30

        close_hint = render_text(make_font(16), "[Click anywhere to close]",
                                 COLORS['gray'])
        screen.blit(close_hint, (rect.x + 20, rect.y + rect.height - 40))

    def _advance_dialogue(self):
        """Advance to the next queued dialogue line."""
        if self.dialogue_idx < len(self.dialogue_queue):
            text, speaker = self.dialogue_queue[self.dialogue_idx]
            self.game.dialogue.clear()
            self.game.dialogue.show_dialogue(text, speaker)
            self.dialogue_idx += 1
        else:
            self.dialogue_playing = False
            self.game.dialogue.clear()
            if self.pending_transition:
                self.pending_transition = False
                self._transition_to_scene4()

    def _queue_dialogue(self, text, speaker):
        """Queue a dialogue line for sequential display."""
        self.dialogue_queue.append((text, speaker))

    def _start_queued_dialogue(self):
        """Start showing queued dialogues."""
        if not self.dialogue_playing and self.dialogue_queue:
            self.dialogue_playing = True
            self.dialogue_idx = 0
            text, speaker = self.dialogue_queue[0]
            self.game.dialogue.clear()
            self.game.dialogue.show_dialogue(text, speaker)

    def update(self, events: list):
        """Handle greenhouse interactions."""
        if self.phase == 'entered':
            return

        # Intro dialogue auto-play
        if self.phase == 'greenhouse_intro' and not self.intro_dialogue_done:
            if self.intro_idx >= len(self.intro_lines):
                # All intro lines shown - clear dialogue and start fade
                self.intro_dialogue_done = True
                self.game.dialogue.clear()
                self.mara_fading = True
                self.mara_fade_timer = 0.0
                self.phase = 'explore'
            elif not self.game.dialogue.current_dialogue:
                text, speaker = self.intro_lines[self.intro_idx]
                self.game.dialogue.show_dialogue(text, speaker)
                self.intro_idx += 1

        # Update Mara fade-out timer
        if self.mara_fading:
            self.mara_fade_timer += 0.016
            if self.mara_fade_timer >= self.mara_fade_duration:
                self.mara_left = True
                self.mara_fading = False

        # Add ambient particles
        if len(self.particles.particles) < 10:
            self.particles.add_ambient(510, 300, 1)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # Click to advance intro dialogue (before hotspot checks)
                if self.phase == 'greenhouse_intro' and not self.intro_dialogue_done:
                    if self.game.dialogue.current_dialogue:
                        if self.intro_idx < len(self.intro_lines):
                            text, speaker = self.intro_lines[self.intro_idx]
                            self.game.dialogue.clear()
                            self.game.dialogue.show_dialogue(text, speaker)
                            self.intro_idx += 1
                        else:
                            self.intro_dialogue_done = True
                            self.mara_fading = True
                            self.mara_fade_timer = 0.0
                            self.phase = 'explore'
                        continue

                # Click to advance queued dialogue (explore phase)
                if self.dialogue_playing and self.game.dialogue.current_dialogue:
                    self._advance_dialogue()
                    continue

                # Close care sheet
                if self.showing_care_sheet:
                    self.showing_care_sheet = False
                    continue

                # Observation mode
                if self.observation_active:
                    if pygame.Rect(460, 260, 80, 40).collidepoint(pos):
                        self._inspect_petals()
                    elif pygame.Rect(510, 310, 80, 40).collidepoint(pos):
                        self._inspect_stem()
                    elif pygame.Rect(510, 380, 80, 40).collidepoint(pos):
                        self._inspect_soil()
                    continue

                # Watering can
                if self.watering_can_rect.collidepoint(pos):
                    if not self.watering_can_held:
                        self.watering_can_held = True
                        self.game.inventory.add_item('watering_can',
                                                     'Empty Watering Can')
                        self.game.dialogue.show_dialogue(
                            "Standard watering can.",
                            "Elias",
                            auto_advance=True)
                    elif not self.watering_can_filled:
                        self._try_fill_water()

                # Sink
                elif self.sink_rect.collidepoint(pos):
                    if self.watering_can_held and not self.watering_can_filled:
                        self._try_fill_water()
                    elif self.watering_can_held and self.watering_can_filled:
                        self.game.dialogue.show_dialogue(
                            "Already filled with 500 ml.",
                            "Elias",
                            auto_advance=True)
                    else:
                        self.game.dialogue.show_dialogue("Filtered water system?", "Elias", auto_advance=True)
                        self.game.dialogue.show_dialogue("Yes.", "Mara", auto_advance=True)
                        self.game.dialogue.show_dialogue(
                            "Specimens in this section don't receive water "
                            "directly from the main supply.", "Mara", auto_advance=True)
                        self.game.dialogue.show_dialogue("Why?", "Elias", auto_advance=True)
                        self.game.dialogue.show_dialogue("Because contamination ruins research.", "Mara", auto_advance=True)
                        self.game.dialogue.show_dialogue("And careers.", "Mara", auto_advance=True)

                # Clipboard
                elif self.clipboard_rect.collidepoint(pos):
                    if not self.clipboard_read:
                        self.showing_care_sheet = True
                        self.clipboard_read = True
                        self.game.journal.add_objective('obj_read_care',
                                                        'Read Care Instructions',
                                                        'Find X-17 care sheet')
                    else:
                        self.game.dialogue.show_dialogue(
                            "Daily care: 23-25°C, inspect for abnormalities, "
                            "500 ml filtered water, record reactions, "
                            "do not relocate.",
                            "Elias",
                            auto_advance=True)

                # Thermometer
                elif self.thermometer_rect.collidepoint(pos):
                    self.game.dialogue.show_dialogue(
                        "Greenhouse thermometer: 24 degrees Celsius.\n"
                        "Within the required range.",
                        "Elias",
                        auto_advance=True)

                # Cabinet
                elif self.cabinet_rect.collidepoint(pos):
                    self.game.dialogue.show_dialogue(
                        "Storage cabinet. Contains general supplies "
                        "and extra pots.",
                        "Elias",
                        auto_advance=True)

                # Journal
                elif self.journal_rect.collidepoint(pos) and not self.journal_closed:
                    self._interact_journal()

                # X-17
                elif self.x17_rect.collidepoint(pos):
                    if self.phase == 'explore':
                        if not self.x17_interacted:
                            self._first_meet_x17()
                        elif not self.x17_watered:
                            self._observe_x17()
                        else:
                            self._x17_after_water()
                    elif self.phase == 'watering':
                        if self.watering_can_held and self.watering_can_filled and '500' in self.game.inventory.items.get('watering_can', {}).get('name', ''):
                            self._water_x17_from_scene3()
                        elif self.watering_can_held and 'Empty' in self.game.inventory.items.get('watering_can', {}).get('name', ''):
                            self.game.dialogue.show_dialogue(
                                "The watering can is empty.\nI need to fill it with 500 ml "
                                "filtered water.",
                                "Elias",
                                auto_advance=True)
                        elif not self.watering_can_held:
                            self.game.dialogue.show_dialogue(
                                "I need to select the watering can first.",
                                "Elias",
                                auto_advance=True)

    def _first_meet_x17(self):
        """First interaction with X-17 - dialogue and observation."""
        self.x17_interacted = True
        self.observation_active = True
        self.dialogue_queue = []
        self._queue_dialogue("This is why you're here.", "Mara")
        self._queue_dialogue("That's it?", "Elias")
        self._queue_dialogue("Disappointed?", "Mara")
        self._queue_dialogue("A little.", "Elias")
        self._queue_dialogue("Specimen X-17.", "Mara")
        self._queue_dialogue(
            "Recovered three weeks ago from an undocumented forest region.", "Mara")
        self._queue_dialogue("Species?", "Elias")
        self._queue_dialogue("Unknown.", "Mara")
        self._queue_dialogue("Genus?", "Elias")
        self._queue_dialogue("Unknown.", "Mara")
        self._queue_dialogue("Family?", "Elias")
        self._queue_dialogue(
            "If we knew that, Elias, we wouldn't need you.", "Mara")
        self._queue_dialogue("Before you do anything...", "Mara")
        self._queue_dialogue("Inspect it.", "Mara")
        self._queue_dialogue("What am I looking for?", "Elias")
        self._queue_dialogue("You tell me.", "Mara")
        self.game.journal.add_objective('obj_inspect_x17',
                                        'Inspect X-17',
                                        'Examine petals, stem, and soil')
        self._start_queued_dialogue()

    def _observe_x17(self):
        """Second X-17 interaction - observation mode."""
        self.observation_active = True
        self.game.dialogue.show_dialogue(
            "Inspect X-17 for changes.\nCheck petals, stem, and soil.",
            "Mara",
            ["Inspect petals", "Inspect stem", "Inspect soil"],
            lambda c: None)

    def _x17_after_water(self):
        """X-17 interaction after watering."""
        self.dialogue_queue = []
        self._queue_dialogue("That's it?", "Elias")
        self._queue_dialogue("What were you expecting?", "Mara")
        self._queue_dialogue("I don't know.", "Elias")
        self._queue_dialogue("That's research.", "Mara")
        self.game.journal.add_objective('obj_wait',
                                         'Wait for reaction',
                                         'Observe X-17 for changes')
        self._start_queued_dialogue()

    def _water_x17_from_scene3(self):
        """Water X-17 from Scene 3 and trigger transition to Scene 4."""
        self.x17_watered = True
        self.watering_can_filled = False
        can = self.game.inventory.items.get('watering_can', {})
        if '500' in can.get('name', ''):
            can['name'] = 'Empty Watering Can'
        self.game.journal.complete_objective('obj_water_x17_done')
        self.game.journal.add_objective('obj_wait',
                                         'Wait for reaction',
                                         'Observe X-17 for changes')
        self.game.journal.update_objective('obj_water_x17_done',
                                            'Water X-17 with 500 ml',
                                            'Use watering can on X-17')
        self._play_transition_dialogue()

    def _play_transition_dialogue(self):
        """Play radio call and Mara leaving dialogue, then transition to Scene 4."""
        self.pending_transition = True
        self.dialogue_queue = []
        self._queue_dialogue("Slowly.", "Mara")
        self._queue_dialogue("That's it?", "Elias")
        self._queue_dialogue("What were you expecting?", "Mara")
        self._queue_dialogue("I don't know.", "Elias")
        self._queue_dialogue("That's research.", "Mara")
        self._queue_dialogue("SFX: Radio static crackles through the greenhouse.", "System")
        self._queue_dialogue("Dr. Vale.", "Radio")
        self._queue_dialogue("Report to Lab Two immediately.", "Radio")
        self._queue_dialogue("I'm coming.", "Mara")
        self._queue_dialogue("Finish the observation record.", "Mara")
        self._queue_dialogue("Then leave.", "Mara")
        self._queue_dialogue("You're leaving me here?", "Elias")
        self._queue_dialogue("It's a greenhouse, Elias.", "Mara")
        self._queue_dialogue("What could happen?", "Mara")
        self._queue_dialogue("Elias.", "Mara")
        self._queue_dialogue("Yeah?", "Elias")
        self._queue_dialogue("If you hear anything unusual--", "Mara")
        self._queue_dialogue("What?", "Elias")
        self._queue_dialogue("Nothing.", "Mara")
        self._queue_dialogue("Finish your work.", "Mara")
        self._queue_dialogue(
            "SFX: Greenhouse door closes.\nSFX: Electronic lock engages.\nThe "
            "greenhouse ambience becomes quieter.", "System")
        self.game.sanity.decrease_sanity(5)
        self.game.journal.update_objective('obj_wait',
                                             'Complete observation',
                                             'Inspect X-17 again')
        self.game.flags['x17_watered'] = True
        self.game.flags['mara_left'] = True
        self.game.journal.add_objective('obj_horror',
                                         'Inspect X-17',
                                         'Observe X-17 for supernatural changes')
        self._start_queued_dialogue()

    def _transition_to_scene4(self):
        """Transition to Chapter 3 after Mara leaves."""
        from blooming.scenes.chapter3_care import Chapter3_Care
        self.game.current_scene = Chapter3_Care(self.game)

    def _inspect_petals(self):
        """Inspect X-17 petals."""
        self.observed_petals = True
        self.game.dialogue.show_dialogue("Closed petals.", "Elias", auto_advance=True)
        self.game.dialogue.show_dialogue("Pale coloration.", "Elias", auto_advance=True)
        self.game.dialogue.show_dialogue("No visible physical damage.", "Elias", auto_advance=True)
        self.game.dialogue.show_dialogue("Good.", "Mara", auto_advance=True)
        self.game.dialogue.show_dialogue("Next.", "Mara", auto_advance=True)

    def _inspect_stem(self):
        """Inspect X-17 stem."""
        self.observed_stem = True
        self.game.dialogue.show_dialogue("Stem is upright.", "Elias", auto_advance=True)
        self.game.dialogue.show_dialogue("No visible lesions.", "Elias", auto_advance=True)
        self.game.dialogue.show_dialogue("And?", "Mara", auto_advance=True)
        self.game.dialogue.show_dialogue("Slight discoloration near the base.", "Elias", auto_advance=True)
        self.game.dialogue.show_dialogue("Good.", "Mara", auto_advance=True)
        self.game.dialogue.show_dialogue("Remember it.", "Mara", auto_advance=True)

    def _inspect_soil(self):
        """Inspect X-17 soil - triggers watering choice."""
        self.observed_soil = True
        self.game.dialogue.show_dialogue("The soil is dry.", "Elias")
        self.game.dialogue.show_dialogue(
            "Which means?",
            "Mara",
            ["Water it.", "Change the soil.", "Move it into sunlight."],
            lambda c: self._soil_choice(c))

    def _soil_choice(self, choice: str):
        """Handle soil inspection choice."""
        if choice == "Water it.":
            self.game.dialogue.show_dialogue("Water it.", "Elias", auto_advance=True)
            self.game.dialogue.show_dialogue("Exactly.", "Mara", auto_advance=True)
            self.game.journal.complete_objective('obj_inspect_x17')
        elif choice == "Change the soil.":
            self.game.dialogue.show_dialogue("Change the soil?", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("No.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("Start with the obvious problem.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("The soil is dry.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue(
                "Water it.",
                "Mara",
                ["Water it."],
                lambda c: self._soil_choice("Water it."))
        else:
            self.game.dialogue.show_dialogue("What was the rule outside?", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("Don't move the specimens.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("Good.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("So don't.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue(
                "Water it.",
                "Mara",
                ["Water it."],
                lambda c: self._soil_choice("Water it."))

    def _start_watering(self):
        """Begin the watering puzzle."""
        self.game.journal.add_objective('obj_water_x17',
                                        'Prepare 500 ml Water',
                                        'Fill watering can at the sink')
        self.game.dialogue.show_dialogue(
            "You already found the watering can.\nWhere would you fill it?",
            "Mara")

    def _try_fill_water(self):
        """Attempt to fill the watering can."""
        if not self.clipboard_read:
            self.game.dialogue.show_dialogue("How much water?", "Elias", auto_advance=True)
            self.game.dialogue.show_dialogue("Check the care sheet.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("You could just tell me.", "Elias", auto_advance=True)
            self.game.dialogue.show_dialogue("I could.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("Check the care sheet.", "Mara", auto_advance=True)
            return

        self.game.dialogue.show_dialogue(
            "How much water?",
            "Elias",
            ["250 ml", "500 ml", "750 ml"],
            lambda c: self._water_quantity(c))

    def _trigger_scene4_transition(self):
        """Transition to Chapter 3 after Mara leaves."""
        from blooming.scenes.chapter3_care import Chapter3_Care
        self.game.current_scene = Chapter3_Care(self.game)
        self.game.journal.add_objective('obj_horror',
                                         'Inspect X-17',
                                         'Observe X-17 for supernatural changes')

    def _water_quantity(self, quantity: str):
        """Handle water quantity selection."""
        if quantity == "250 ml":
            self.game.dialogue.show_dialogue("Two hundred and fifty.", "Elias", auto_advance=True)
            self.game.dialogue.show_dialogue("Read the care sheet again.", "Mara", auto_advance=True)
            self.game.inventory.items['watering_can']['name'] = 'Empty Watering Can'
            self.watering_can_filled = False
        elif quantity == "500 ml":
            self.watering_can_filled = True
            self.game.inventory.items['watering_can']['name'] = 'Can (500 ml)'
            self.game.dialogue.show_dialogue(
                "Five hundred milliliters.", "Elias", auto_advance=True)
            self.game.dialogue.show_dialogue("Good.", "Mara", auto_advance=True)
            self.game.journal.update_objective('obj_water_x17',
                                               'Water X-17 with 500 ml',
                                               'Use watering can on X-17')
            self.game.journal.add_objective('obj_water_x17_done',
                                            'Water X-17',
                                            'Apply 500 ml to the specimen')
        else:
            self.game.dialogue.show_dialogue("Seven hundred and fifty.", "Elias", auto_advance=True)
            self.game.dialogue.show_dialogue("You're caring for it, Elias.", "Mara", auto_advance=True)
            self.game.dialogue.show_dialogue("Not drowning it.", "Mara", auto_advance=True)
            self.game.inventory.items['watering_can']['name'] = 'Empty Watering Can'
            self.watering_can_filled = False

    def _interact_journal(self):
        """Interact with the old research journal."""
        self.journal_closed = True
        self.dialogue_queue = []
        self._queue_dialogue("Whose journal is this?", "Elias")
        self._queue_dialogue("Leave that.", "Mara")
        self._queue_dialogue("Why?", "Elias")
        self._queue_dialogue("Old research notes.", "Mara")
        self._queue_dialogue("From X-17?", "Elias")
        self._queue_dialogue("I said leave it.", "Mara")
        # Mara approaches
        self._queue_dialogue("Come here.", "Mara")
        self._queue_dialogue("There's something you need to see.", "Mara")
        self.game.journal.update_objective('obj_inspect_x17',
                                           'Meet Mara at the specimen table',
                                           'Inspect X-17')
        self._start_queued_dialogue()

