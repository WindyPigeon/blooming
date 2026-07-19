"""Chapter 3 - Greenhouse Exploration (Member B)

Player explores the greenhouse, finds the watering can,
reads care instructions, and meets Specimen X-17.
Includes the observation tutorial (inspect petals, stem, soil).
"""

import math
import random
import pygame
from blooming.utils.utils import render_text, make_font, load_image, scale_image_keep_ratio
from blooming.utils import COLORS
from blooming.utils.particles import ParticleSystem

try:
    import numpy as np
except Exception:
    np = None


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
        self.clipboard_rect = pygame.Rect(640, 420, 80, 80)
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
        self.clipboard_read_post_dialogue = False
        self.entered = False
        self.phase = 'greenhouse_intro'
        self._pending_chapter3 = False
        self._pending_watering = False
        self._pending_water_x17 = False
        self.particles = ParticleSystem()

        # Dialogue queue for non-choice dialogues
        self.dialogue_queue = []
        self.dialogue_idx = 0
        self.dialogue_playing = False
        self.pending_transition = False
        self.waiting_for_choice = False
        self.pending_obs_instruction = False
        self.just_started_dialogue = False

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
        self._inspection_options_shown = False
        self.show_first_impression_choice = False
        self.show_inspection_options = False
        self.observation_instruction_shown = False
        self.show_observation_instruction = False
        self.show_first_impression_choice_done = False

        # Care sheet display
        self.showing_care_sheet = False

        # Screen flicker effect (uses the shared vfx/screen-flicker.png)
        self.flicker_img = load_image('vfx/screen-flicker.png')
        self.flicker_active = False
        self.flicker_next_at = 0
        self.flicker_end_at = 0

        # Moving shadow shapes drifting across the greenhouse glass/floor
        self.shadow_time = 0.0
        self.shadows = [
            {'x': -160, 'y': 90, 'w': 130, 'h': 340, 'speed': 14, 'alpha': 40},
            {'x': 1180, 'y': 40, 'w': 90, 'h': 260, 'speed': -10, 'alpha': 30},
            {'x': 500, 'y': 60, 'w': 160, 'h': 200, 'speed': 6, 'alpha': 22},
        ]

        # Whisper that slowly grows louder once Elias is left alone
        self.whisper_sound = None
        self.whisper_channel = None
        self.whisper_started = False
        self.whisper_start_ticks = 0
        self.whisper_max_volume = 0.55
        self.whisper_fade_seconds = 25.0
        self._init_whisper_sound()

    def _init_whisper_sound(self):
        """Procedurally generate a soft, breathy whisper loop.

        The project ships no audio assets, so the whisper is synthesised
        from filtered noise rather than loaded from a file. Any failure
        (no audio device, no numpy, mixer unavailable) is swallowed so the
        scene works identically with sound disabled.
        """
        if np is None:
            return
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            sample_rate = 22050
            duration = 4.0
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            rng = np.random.default_rng(17)
            noise = rng.normal(0, 1, t.shape[0])
            # Crude low-pass (moving average) so it reads as "breath" not hiss
            kernel = np.ones(48) / 48.0
            filtered = np.convolve(noise, kernel, mode='same')
            # Slow breathing-rhythm amplitude envelope
            envelope = 0.4 + 0.6 * (0.5 + 0.5 * np.sin(2 * math.pi * 0.25 * t))
            waveform = filtered * envelope
            peak = np.max(np.abs(waveform))
            if peak > 0:
                waveform = waveform / peak
            pcm = (waveform * 32767 * 0.8).astype(np.int16)
            stereo = np.ascontiguousarray(np.column_stack((pcm, pcm)))
            self.whisper_sound = pygame.sndarray.make_sound(stereo)
        except Exception:
            self.whisper_sound = None

    def _start_whisper(self):
        """Begin the whisper loop, silent at first, growing louder over time."""
        if self.whisper_started or self.whisper_sound is None:
            return
        self.whisper_started = True
        try:
            self.whisper_channel = self.whisper_sound.play(loops=-1)
            if self.whisper_channel:
                self.whisper_channel.set_volume(0.0)
            self.whisper_start_ticks = pygame.time.get_ticks()
        except Exception:
            self.whisper_channel = None

    def _stop_whisper(self, fade_ms=800):
        """Fade the whisper out (used when leaving the scene)."""
        if self.whisper_channel:
            try:
                self.whisper_channel.fadeout(fade_ms)
            except Exception:
                pass
            self.whisper_channel = None

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

        # Moving shadows drifting across the glass and floor
        self._draw_moving_shadows(screen)

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

        # Screen flicker (uses vfx/screen-flicker.png), on top of everything
        if self.flicker_active:
            if self.flicker_img:
                flicker_scaled, ffx, ffy = scale_image_keep_ratio(
                    self.flicker_img, 1024, 768)
                screen.blit(flicker_scaled, (ffx, ffy))
            else:
                flicker_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
                flicker_surf.fill((255, 255, 255, 35))
                screen.blit(flicker_surf, (0, 0))

        # Objective hint after intro
        if self.intro_dialogue_done and self.phase == 'explore' and not self.game.flags.get('objective_hint_shown', False):
            obj_surf = render_text(make_font(28), "EXPLORE THE GREENHOUSE", COLORS['yellow'])
            screen.blit(obj_surf, (1024 // 2 - obj_surf.get_width() // 2, 50))
            hint_surf = render_text(make_font(18), "Click on objects to interact", COLORS['white'])
            screen.blit(hint_surf, (1024 // 2 - hint_surf.get_width() // 2, 90))
            self.game.flags['objective_hint_shown'] = True

    def _draw_moving_shadows(self, screen):
        """Draw soft, slowly drifting shadow silhouettes across the scene."""
        for shadow in self.shadows:
            sway = math.sin(self.shadow_time * 0.5 + shadow['x'] * 0.01) * 10
            shadow_surf = pygame.Surface((shadow['w'], shadow['h']), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surf, (0, 0, 0, shadow['alpha']),
                                (0, 0, shadow['w'], shadow['h']))
            screen.blit(shadow_surf, (shadow['x'] + sway, shadow['y']))

    def _draw_observation(self, screen):
        """Draw observation mode UI."""
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 60))
        screen.blit(overlay, (0, 0))

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
        if self.dialogue_idx < len(self.game.dialogue._dialogue_queue):
            item = self.game.dialogue._dialogue_queue[self.dialogue_idx]
            if isinstance(item, dict):
                text, speaker = item['text'], item['speaker']
                choices = item.get('choices')
                callback = item.get('callback')
                self.game.dialogue.current_dialogue = {
                    'text': text,
                    'speaker': speaker,
                    'lines': self.game.dialogue._wrap_text(text, 550),
                }
                self.game.dialogue.choices = choices or []
                self.game.dialogue.choice_callback = callback
                self.game.dialogue.typewriter_text = text
                if choices:
                    self.waiting_for_choice = True
                else:
                    self.waiting_for_choice = False
            else:
                text, speaker = item
                self.game.dialogue.current_dialogue = {
                    'text': text,
                    'speaker': speaker,
                    'lines': self.game.dialogue._wrap_text(text, 550),
                }
                self.game.dialogue.choices = []
                self.game.dialogue.choice_callback = None
                self.game.dialogue.typewriter_text = text
                self.waiting_for_choice = False
            self.game.dialogue.typewriter_index = 0
            self.game.dialogue.typewriter_active = False
            self.game.dialogue.typewriter_delay = len(self.game.dialogue.typewriter_text) * self.game.dialogue.typewriter_speed
            self.dialogue_idx += 1
        else:
            # Check state flags BEFORE clearing the queue/dialogue
            if self.pending_obs_instruction:
                self.pending_obs_instruction = False
                if not self.observation_instruction_shown:
                    self._show_observation_instruction()
                    return
                # Observation instruction already shown - transition to inspection options
                if self.first_impression is None:
                    self.show_first_impression_choice = True
                    self.just_started_dialogue = True
                    return
                self.show_inspection_options = True
                self.show_first_impression_choice = False  # Clear to prevent re-trigger
                self.just_started_dialogue = True
                return
            if self.show_observation_instruction:
                self.show_observation_instruction = False
                self.pending_obs_instruction = True
                self.game.dialogue.current_dialogue = None
                return
            if self.show_first_impression_choice:
                self.show_first_impression_choice = False
                if self.first_impression is None:
                    self._show_first_impression_choice()
                else:
                    self.just_started_dialogue = True
                return
            if self._pending_chapter3:
                self._pending_chapter3 = False
                self.game.dialogue.current_dialogue = None
                self.game.dialogue.choices = []
                self.game.dialogue.choice_callback = None
                self._transition_to_scene4()
                return
            if self._pending_watering:
                self._pending_watering = False
                self.phase = 'watering'
                self.game.dialogue.current_dialogue = None
                self.game.dialogue.choices = []
                self.game.dialogue.choice_callback = None
                self._start_watering()
                return
            if self._pending_water_x17:
                self._pending_water_x17 = False
                self.game.dialogue.current_dialogue = None
                self.game.dialogue.choices = []
                self.game.dialogue.choice_callback = None
                self._show_water_x17_prompt()
                return
            # Check state flags that should run AFTER queue exhaustion
            if self.show_first_impression_choice:
                if self.first_impression is None:
                    self.show_first_impression_choice = False
                    self._show_first_impression_choice()
                    return
                else:
                    # Player already made choice - clear flag to prevent infinite loop
                    self.show_first_impression_choice = False
                    if not self.show_inspection_options:
                        self.show_inspection_options = True
                return
            if self.show_observation_instruction:
                self.show_observation_instruction = False
                self.pending_obs_instruction = True
                return
            # Now safe to clear
            self.dialogue_playing = False
            self.game.dialogue.current_dialogue = None
            self.game.dialogue.clear()
            self.dialogue_queue = []
            self.dialogue_idx = 0
            self.waiting_for_choice = False

    def _queue_dialogue(self, text, speaker, choices=None, callback=None):
        """Queue a dialogue line for sequential display."""
        if choices is not None:
            self.dialogue_queue.append({
                'text': text,
                'speaker': speaker,
                'choices': choices,
                'callback': callback,
            })
        else:
            self.dialogue_queue.append((text, speaker))

    def _display_queued(self):
        """Display the dialogue at dialogue_idx (updates display state only)."""
        if not self.dialogue_queue or self.dialogue_idx >= len(self.dialogue_queue):
            return
        item = self.dialogue_queue[self.dialogue_idx]
        self.waiting_for_choice = False
        if isinstance(item, dict):
            text, speaker = item['text'], item['speaker']
            choices = item.get('choices', [])
            self.game.dialogue.current_dialogue = {
                'text': text,
                'speaker': speaker,
                'lines': self.game.dialogue._wrap_text(text, 550),
            }
            self.game.dialogue.choices = choices
            self.game.dialogue.choice_callback = item.get('callback')
            self.game.dialogue.typewriter_text = text
            if choices:
                self.waiting_for_choice = True
        else:
            text, speaker = item
            self.game.dialogue.current_dialogue = {
                'text': text,
                'speaker': speaker,
                'lines': self.game.dialogue._wrap_text(text, 550),
            }
            self.game.dialogue.choices = []
            self.game.dialogue.choice_callback = None
            self.game.dialogue.typewriter_text = text
        self.game.dialogue.typewriter_index = 0
        self.game.dialogue.typewriter_active = False
        self.game.dialogue.typewriter_delay = len(self.game.dialogue.typewriter_text) * self.game.dialogue.typewriter_speed

    def _start_queued_dialogue(self):
        """Sync greenhouse queue to dialogue system and display current item."""
        self.game.dialogue._dialogue_queue = []
        for item in self.dialogue_queue:
            if isinstance(item, dict):
                self.game.dialogue._dialogue_queue.append(item)
            else:
                text, speaker = item
                self.game.dialogue._dialogue_queue.append({
                    'text': text,
                    'speaker': speaker,
                    'choices': [],
                    'callback': None,
                    'auto_advance': False,
                })
        self.game.dialogue._queue_index = self.dialogue_idx
        self._display_queued()
        self.just_started_dialogue = True

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

        alone = self.game.flags.get('mara_left', False)

        # Moving shadows drifting across the glass/floor - subtle while
        # Mara is around, more pronounced once Elias is left alone
        self.shadow_time += 0.016
        for shadow in self.shadows:
            shadow['x'] += shadow['speed'] * (1.6 if alone else 1.0) * 0.016 * 60
            if shadow['speed'] > 0 and shadow['x'] > 1024 + shadow['w']:
                shadow['x'] = -shadow['w']
            elif shadow['speed'] < 0 and shadow['x'] < -shadow['w']:
                shadow['x'] = 1024 + shadow['w']

        # Screen flicker - starts only once Elias is alone in the greenhouse
        if alone:
            now = pygame.time.get_ticks()
            if not self.flicker_active and now >= self.flicker_next_at:
                self.flicker_active = True
                self.flicker_end_at = now + random.randint(100, 240)
            elif self.flicker_active and now >= self.flicker_end_at:
                self.flicker_active = False
                self.flicker_next_at = now + random.randint(2500, 6000)
        else:
            self.flicker_active = False

        # Whisper slowly grows louder the longer Elias is alone
        if self.whisper_started and self.whisper_channel:
            elapsed = (pygame.time.get_ticks() - self.whisper_start_ticks) / 1000.0
            volume = min(1.0, elapsed / self.whisper_fade_seconds) * self.whisper_max_volume
            try:
                self.whisper_channel.set_volume(volume)
            except Exception:
                pass

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

                # Close care sheet
                if self.showing_care_sheet:
                    self.showing_care_sheet = False
                    if not self.clipboard_read_post_dialogue:
                        self._clipboard_after_care_sheet()
                        self.clipboard_read_post_dialogue = True
                    continue

                # Observation mode
                if self.observation_active:
                    choice_clicked = False
                    has_choice_dialogue = (self.game.dialogue.current_dialogue 
                                           and self.game.dialogue.choices)
                    # Check dialogue choice clicks first
                    if has_choice_dialogue:
                        text_y = self.game.dialogue.box_rect.y + 50
                        for line in self.game.dialogue._wrap_text(
                                self.game.dialogue.typewriter_text if self.game.dialogue.typewriter_active
                                else self.game.dialogue.current_dialogue['text'], 550):
                            text_y += 30
                        choice_y = text_y + 5
                        for i, choice in enumerate(self.game.dialogue.choices):
                            y_pos = choice_y + i * 28
                            if (150 <= pos[0] <= 1024 - 150
                                    and y_pos <= pos[1] <= y_pos + 22):
                                self.game.dialogue.choice_callback(choice)
                                choice_clicked = True
                    if choice_clicked:
                        continue
                    # Check pending transitions before skipping hotspot checks
                    if self.show_inspection_options:
                        print(f"[PENDING insp] pending={getattr(self, '_pending_inspect_choice', None)}")
                        self.show_inspection_options = False
                        if getattr(self, '_pending_inspect_choice', None):
                            choice = self._pending_inspect_choice
                            self._pending_inspect_choice = None
                            self.observation_active = True
                            if choice == "Inspect petals":
                                self._inspect_petals()
                            elif choice == "Inspect stem":
                                self._inspect_stem()
                            elif choice == "Inspect soil":
                                self._inspect_soil()
                        else:
                            self._inspection_options_shown = False
                            self.observation_active = True
                            self._observe_x17()
                            self._inspection_options_shown = True
                        continue
                    # Skip hotspot checks when a choice dialogue is active
                    if has_choice_dialogue:
                        continue
                    # Advance non-choice queued dialogues (e.g. soil chain)
                    if self.dialogue_playing and self.game.dialogue.current_dialogue:
                        self._advance_dialogue()
                        continue
                    # When no dialogue to advance but in observation mode, check X-17 for inspection options
                    if self.phase == 'explore' and not self.x17_interacted:
                        if self.x17_rect.collidepoint(pos):
                            self._first_meet_x17()
                            continue
                    if self.phase == 'explore' and self.x17_interacted and not self.x17_watered:
                        if self.x17_rect.collidepoint(pos) and not self.waiting_for_choice and self.observation_active:
                            self._observe_x17()
                            continue
                    continue

                # Handle choice click for non-observation dialogues
                if self.waiting_for_choice and self.game.dialogue.choices and self.game.dialogue.current_dialogue:
                    if self.game.dialogue.choice_callback:
                        pos = pygame.mouse.get_pos()
                        text_y = self.game.dialogue.box_rect.y + 50
                        for line in self.game.dialogue._wrap_text(
                                self.game.dialogue.typewriter_text if self.game.dialogue.typewriter_active
                                else self.game.dialogue.current_dialogue['text'], 550):
                            text_y += 30
                        choice_y = text_y + 5
                        for i, choice in enumerate(self.game.dialogue.choices):
                            y_pos = choice_y + i * 28
                            if (150 <= pos[0] <= 1024 - 150
                                    and y_pos <= pos[1] <= y_pos + 22):
                                self.game.dialogue.choice_callback(choice)
                                self.waiting_for_choice = False
                                continue
                        # Click was in dialogue area but not on a choice — advance
                        self.waiting_for_choice = False
                        if self.game.dialogue.current_dialogue:
                            self._advance_dialogue()
                            continue

                # Advance non-observation queued dialogues
                if self.dialogue_playing and self.game.dialogue.current_dialogue and not self.waiting_for_choice:
                    if not self.just_started_dialogue:
                        self._advance_dialogue()
                        if self.pending_obs_instruction:
                            self.pending_obs_instruction = False
                            self._show_observation_instruction()
                            continue
                    self.just_started_dialogue = False
                    continue

                # Handle pending transitions after dialogue queue exhausted
                if not self.game.dialogue.current_dialogue:
                    if self._pending_chapter3:
                        self._pending_chapter3 = False
                        self.game.dialogue.current_dialogue = None
                        self.game.dialogue.choices = []
                        self.game.dialogue.choice_callback = None
                        self._transition_to_scene4()
                        continue
                    if self._pending_watering:
                        self._pending_watering = False
                        self.game.dialogue.current_dialogue = None
                        self.game.dialogue.choices = []
                        self.game.dialogue.choice_callback = None
                        self.phase = 'watering'
                        self._start_watering()
                        continue
                    if self._pending_water_x17:
                        self._pending_water_x17 = False
                        self.game.dialogue.current_dialogue = None
                        self.game.dialogue.choices = []
                        self.game.dialogue.choice_callback = None
                        self._show_water_x17_prompt()
                        continue
                    if self.show_observation_instruction:
                        self.show_observation_instruction = False
                        if not self.observation_instruction_shown:
                            self.pending_obs_instruction = True
                        continue
                    if self.pending_obs_instruction:
                        self.pending_obs_instruction = False
                        if not self.observation_instruction_shown:
                            self._show_observation_instruction()
                        continue
                    if self.show_first_impression_choice:
                        if self.first_impression is None:
                            self.show_first_impression_choice = False
                            self._show_first_impression_choice()
                            continue
                        else:
                            self.show_first_impression_choice = False
                            if not self.show_inspection_options and not self.observation_instruction_shown:
                                self.show_inspection_options = True
                            continue
                    if self.observation_instruction_shown:
                        self.observation_instruction_shown = False
                        self.observation_active = True
                        continue
                    if self.dialogue_playing:
                        self.dialogue_playing = False
                        self.game.dialogue._dialogue_queue = []
                        self.game.dialogue._queue_index = 0
                    if self.observation_active and not self.x17_watered:
                        self.show_inspection_options = True
                        self._inspection_options_shown = False

                # Watering can
                if self.watering_can_rect.collidepoint(pos) and not self.waiting_for_choice:
                    if not self.watering_can_held:
                        self._pickup_watering_can()
                    elif not self.watering_can_filled:
                        self._watering_can_after_pickup()

                # Sink
                elif self.sink_rect.collidepoint(pos):
                    if self.watering_can_held and not self.watering_can_filled:
                        self._try_fill_water()
                    elif self.watering_can_held and self.watering_can_filled:
                        self.game.dialogue.show_dialogue(
                            "Already filled with 500 ml.",
                            "Elias")
                    else:
                        self.dialogue_queue = []
                        self._queue_dialogue("Filtered water system?", "Elias")
                        self._queue_dialogue("Yes.", "Mara")
                        self._queue_dialogue(
                            "Specimens in this section don't receive water "
                            "directly from the main supply.", "Mara")
                        self._queue_dialogue("Why?", "Elias")
                        self._queue_dialogue("Because contamination ruins research.", "Mara")
                        self._queue_dialogue("And careers.", "Mara")
                        self.dialogue_playing = True
                        self.dialogue_idx = 0
                        self._start_queued_dialogue()

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
                            "Elias")

                # Thermometer
                elif self.thermometer_rect.collidepoint(pos):
                    self.game.dialogue.show_dialogue(
                        "Greenhouse thermometer: 24 degrees Celsius.\n"
                        "Within the required range.",
                        "Elias")

                # Cabinet
                elif self.cabinet_rect.collidepoint(pos):
                    self.game.dialogue.show_dialogue(
                        "Storage cabinet. Contains general supplies "
                        "and extra pots.",
                        "Elias")

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
                                "Elias")
                        elif not self.watering_can_held:
                            self.game.dialogue.show_dialogue(
                                "I need to select the watering can first.",
                                "Elias")

    def _pickup_watering_can(self):
        """Pick up the watering can with dialogue sequence."""
        self.watering_can_held = True
        self.game.inventory.add_item('watering_can', 'Empty Watering Can', image_path='props/watering-can.png')
        self.dialogue_queue = []
        self._queue_dialogue("Standard watering can.", "Elias")
        self._queue_dialogue("Take it.", "Mara")
        self._queue_dialogue("Now?", "Elias")
        self._queue_dialogue("Unless you're planning to carry water in your hands.", "Mara")
        self.game.journal.add_objective('obj_water_x17', 'Prepare 500 ml Water', 'Fill watering can at the sink')
        self._start_queued_dialogue()

    def _watering_can_after_pickup(self):
        """Dialogue after player has the watering can in hand."""
        self.dialogue_queue = []
        self._queue_dialogue("Good.", "Mara")
        self._queue_dialogue("You know how to pick things up.", "Mara")
        self._queue_dialogue("I did graduate from university.", "Elias")
        self._queue_dialogue("We'll see how useful that was.", "Mara")
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()

    def _clipboard_after_care_sheet(self):
        """Dialogue after reading the care sheet for the first time."""
        self.dialogue_queue = []
        self._queue_dialogue("Five hundred milliliters.", "Elias")
        self._queue_dialogue("Good.", "Mara")
        self._queue_dialogue("Now you know why we write things down.", "Mara")
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()

    def _first_meet_x17(self):
        """First interaction with X-17 - dialogue and observation."""
        self.x17_interacted = True
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
        self.game.journal.add_objective('obj_inspect_x17',
                                        'Inspect X-17',
                                        'Examine petals, stem, and soil')
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()
        self.show_first_impression_choice = True

    def _observe_x17(self):
        """Second X-17 interaction - observation mode."""
        if self.observation_active and getattr(self, '_inspection_options_shown', False):
            self.observation_active = False
            self.dialogue_playing = False
            self.dialogue_queue = []
            return
        self.observation_active = True
        self.dialogue_queue = []
        self._queue_dialogue(
            "Inspect X-17 for changes.\nCheck petals, stem, and soil.",
            "Mara",
            ["Inspect petals", "Inspect stem", "Inspect soil", "Back"],
            lambda c: self._observe_choice(c))
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self._display_queued()
        self.just_started_dialogue = True
        self._inspection_options_shown = True

    def _observe_choice(self, choice: str):
        """Handle observation mode choices."""
        if choice == "Back":
            self.observation_active = False
            self.dialogue_playing = False
            self.dialogue_queue = []
            self._inspection_options_shown = False
        elif choice in ("Inspect petals", "Inspect stem", "Inspect soil"):
            self._pending_inspect_choice = choice
            self.show_inspection_options = True

    def _show_first_impression_choice(self):
        """Show first impression dialogue choice (before player picks one)."""
        if self.first_impression is not None:
            # Already made a choice - don't call this again
            self.show_first_impression_choice = False
            if self.observation_instruction_shown:
                self.show_inspection_options = True
            return
        
        self.dialogue_queue = []
        self._queue_dialogue(
            "What do you think?",
            "Mara",
            ["It looks dangerous.", "It's beautiful.", "It looks unusual."],
            lambda c: self._first_impression_callback(c))
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self._display_queued()
        self.just_started_dialogue = True

    def _show_observation_instruction(self):
        """Show observation instruction after first impression choice."""
        print(f"[_show_observation_instruction] obs_instr_shown={self.observation_instruction_shown}, pending={self.pending_obs_instruction}")
        if self.observation_instruction_shown:
            print(f"  RETURNED (already shown)")
            return
        self.observation_instruction_shown = True
        self.show_observation_instruction = False
        self.dialogue_queue = []
        self._queue_dialogue("Before you do anything...", "Mara")
        self._queue_dialogue("Inspect it.", "Mara")
        self._queue_dialogue("What am I looking for?", "Elias")
        self._queue_dialogue("You tell me.", "Mara")
        self.game.journal.add_objective('obj_inspect_x17',
                                        'Inspect X-17',
                                        'Examine petals, stem, and soil')
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()
        self.just_started_dialogue = True

    def _first_impression_callback(self, choice: str):
        """Handle first impression dialogue choice."""
        self.dialogue_queue = []
        if choice == "It looks dangerous.":
            self._queue_dialogue("I expected something more dangerous.", "Elias")
            self._queue_dialogue("Appearances are unreliable.", "Mara")
            self.first_impression = "dangerous"
            self.game.flags['first_impression'] = 'dangerous'
        elif choice == "It's beautiful.":
            self._queue_dialogue("It's beautiful.", "Elias")
            self._queue_dialogue("Careful with that word.", "Mara")
            self.first_impression = "beautiful"
            self.game.flags['first_impression'] = 'beautiful'
        elif choice == "It looks unusual.":
            self._queue_dialogue("It looks unusual.", "Elias")
            self._queue_dialogue("Give it time.", "Mara")
            self.first_impression = "unusual"
            self.game.flags['first_impression'] = 'unusual'
        
        self.show_observation_instruction = True
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()

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
        self.dialogue_playing = True
        self.dialogue_idx = 0
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
        self._pending_chapter3 = True
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
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()
        self._start_whisper()
        self._start_queued_dialogue()

    def _transition_to_scene4(self):
        """Transition to Chapter 3 after Mara leaves."""
        self._stop_whisper()
        from blooming.scenes.chapter3_care import Chapter3_Care
        self.game.current_scene = Chapter3_Care(self.game)

    def _inspect_petals(self):
        """Inspect X-17 petals."""
        self.observed_petals = True
        self.dialogue_queue = []
        self._queue_dialogue("Closed petals.", "Elias")
        self._queue_dialogue("Pale coloration.", "Elias")
        self._queue_dialogue("No visible physical damage.", "Elias")
        self._queue_dialogue("They were open three days ago.", "Mara")
        self._queue_dialogue("They won't open again until you water it.", "Mara")
        self._start_queued_dialogue()
        self.show_inspection_options = True

    def _inspect_stem(self):
        """Inspect X-17 stem."""
        self.observed_stem = True
        self.dialogue_queue = []
        self._queue_dialogue("Stem is upright.", "Elias")
        self._queue_dialogue("No visible lesions.", "Elias")
        self._queue_dialogue("And?", "Mara")
        self._queue_dialogue("Slight discoloration near the base.", "Elias")
        self._queue_dialogue("Purple.", "Mara")
        self._queue_dialogue("That's the same shade as the soil.", "Mara")
        self._queue_dialogue("It draws color from whatever touches it.", "Mara")
        self._start_queued_dialogue()
        self.show_inspection_options = True

    def _inspect_soil(self):
        """Inspect X-17 soil - triggers watering choice."""
        self.observed_soil = True
        self.dialogue_queue = []
        self._queue_dialogue("The soil is dry.", "Elias")
        self._queue_dialogue("Which means?", "Mara",
                             ["Water it.", "Change the soil.", "Move it into sunlight."],
                             lambda c: self._soil_choice(c))
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self._start_queued_dialogue()
        self.just_started_dialogue = True

    def _soil_choice(self, choice: str):
        """Handle soil inspection choice."""
        if choice == "Water it.":
            self.dialogue_queue = []
            self._queue_dialogue("Water it.", "Elias")
            self._queue_dialogue("Exactly.", "Mara")
            self.game.journal.complete_objective('obj_inspect_x17')
            # Close the observation overlay and move into the watering phase
            self.observation_active = False
            self._pending_watering = True
            self.dialogue_playing = True
            self.dialogue_idx = 0
            self._start_queued_dialogue()
        elif choice == "Change the soil.":
            self.dialogue_queue = []
            self._queue_dialogue("Change the soil?", "Elias")
            self._queue_dialogue("No.", "Mara")
            self._queue_dialogue("Start with the obvious problem.", "Mara")
            self._queue_dialogue("The soil is dry.", "Mara")
            self._queue_dialogue(
                "Water it.",
                "Mara",
                ["Water it."],
                lambda c: self._soil_choice("Water it."))
            self.dialogue_playing = True
            self.dialogue_idx = 0
            self._start_queued_dialogue()
        else:
            self.dialogue_queue = []
            self._queue_dialogue("What was the rule outside?", "Mara")
            self._queue_dialogue("Don't move the specimens.", "Elias")
            self._queue_dialogue("Good.", "Mara")
            self._queue_dialogue("So don't.", "Mara")
            self._queue_dialogue(
                "Water it.",
                "Mara",
                ["Water it."],
                lambda c: self._soil_choice("Water it."))
            self.dialogue_playing = True
            self.dialogue_idx = 0
            self._start_queued_dialogue()

    def _start_watering(self):
        """Begin the watering puzzle."""
        self.game.journal.add_objective('obj_water_x17',
                                        'Prepare 500 ml Water',
                                        'Fill watering can at the sink')
        self.dialogue_queue = []
        self._queue_dialogue(
            "You already found the watering can.\nWhere would you fill it?",
            "Mara")
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()

    def _show_water_x17_prompt(self):
        """Prompt player to water X-17 after selecting correct amount."""
        self.dialogue_queue = []
        self._queue_dialogue("Now go on.", "Mara")
        self._queue_dialogue("Water the plant.", "Mara")
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()

    def _try_fill_water(self):
        """Attempt to fill the watering can."""
        if not self.clipboard_read:
            self.dialogue_queue = []
            self._queue_dialogue("How much water?", "Elias")
            self._queue_dialogue("Check the care sheet.", "Mara")
            self._queue_dialogue("You could just tell me.", "Elias")
            self._queue_dialogue("I could.", "Mara")
            self._queue_dialogue("But you'll remember more if you look it up yourself.", "Mara")
            self.dialogue_playing = True
            self.dialogue_idx = 0
            self._start_queued_dialogue()
            return

        self.game.dialogue.show_dialogue(
            "How much water?",
            "Elias",
            ["250 ml", "500 ml", "750 ml"],
            lambda c: self._water_quantity(c))

    def _water_quantity(self, quantity: str):
        """Handle water quantity selection."""
        if quantity == "250 ml":
            self.dialogue_queue = []
            self._queue_dialogue("Two hundred and fifty.", "Elias")
            self._queue_dialogue("Read the care sheet again.", "Mara")
            self.game.inventory.items['watering_can']['name'] = 'Empty Watering Can'
            self.watering_can_filled = False
            self.dialogue_playing = True
            self.dialogue_idx = 0
            self._start_queued_dialogue()
        elif quantity == "500 ml":
            self.watering_can_filled = True
            self.game.inventory.items['watering_can']['name'] = 'Can (500 ml)'
            self._pending_water_x17 = True
            self.dialogue_queue = []
            self._queue_dialogue("Five hundred milliliters.", "Elias")
            self._queue_dialogue("Good.", "Mara")
            self.game.journal.update_objective('obj_water_x17',
                                               'Water X-17 with 500 ml',
                                               'Use watering can on X-17')
            self.game.journal.add_objective('obj_water_x17_done',
                                             'Water X-17',
                                             'Apply 500 ml to the specimen')
            self.dialogue_playing = True
            self.dialogue_idx = 0
            self._start_queued_dialogue()
        else:
            self.dialogue_queue = []
            self._queue_dialogue("Seven hundred and fifty.", "Elias")
            self._queue_dialogue("You're caring for it, Elias.", "Mara")
            self._queue_dialogue("Not drowning it.", "Mara")
            self.game.inventory.items['watering_can']['name'] = 'Empty Watering Can'
            self.watering_can_filled = False
            self.dialogue_playing = True
            self.dialogue_idx = 0
            self._start_queued_dialogue()

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
        self.dialogue_playing = True
        self.dialogue_idx = 0
        self._start_queued_dialogue()