"""Scene 4 - Plant Care & Watering X-17 (Member C)

The watering puzzle, Mara's radio call, Mara leaving,
and the transition to supernatural events.
Player waters X-17 with correct 500ml amount.
"""

import math
import pygame
from blooming.utils.utils import render_text, make_font, load_image, scale_image_keep_ratio
from blooming.utils import COLORS
from blooming.utils.particles import ParticleSystem


class Chapter3_Care:
    """Chapter 3: Plant care and watering X-17."""

    def __init__(self, game):
        self.game = game
        self.font = make_font(32)
        self.small_font = make_font(24)
        self.small_font2 = make_font(18)

        # Hotspot rects
        self.x17_rect = pygame.Rect(450, 250, 120, 120)
        self.mara_rect = pygame.Rect(162, 30, 700, 708)
        self.intercom_rect = pygame.Rect(900, 300, 100, 120)

        # State
        self.mara_left = False
        self.watering_can_filled = False
        self.x17_watered = False
        self.radio_called = False
        self.mara_paged = False
        self.x17_glowing = False
        self.entered = False

        # Images
        self.interior_img = load_image('backgrounds/greenhouse-interior.png')
        self.flower_img = load_image('props/flower.png')
        self.mara_img = load_image('char/mara-left.png')
        self.specimen_table_img = load_image('props/specimen-table.png')
        self.intercom_img = load_image('props/intercom.png')
        self.watering_can_img = load_image('props/watering-can.png')

        # Particles
        self.particles = ParticleSystem()

        # Timer for radio call
        self.elapsed_frames = 0

    @property
    def active(self):
        return not self.entered

    def draw(self, screen):
        """Draw the greenhouse care scene."""
        if self.entered:
            return

        # Background
        if self.interior_img:
            bg_scaled, bx, by = scale_image_keep_ratio(self.interior_img, 1024, 768)
            screen.blit(bg_scaled, (bx, by))
        else:
            screen.fill((30, 60, 30))
            for x in range(0, 1024, 100):
                pygame.draw.line(screen, (80, 100, 80),
                                 (x, 0), (x, 250), 2)

        # Rows of plants
        for i in range(0, 1024, 150):
            pygame.draw.rect(screen, (20, 80, 20), (i, 350, 60, 100))
            pygame.draw.rect(screen, (40, 120, 40),
                             (i + 10, 340, 40, 20))

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

        # X-17
        if self.flower_img:
            flower_scaled, fx, fy = scale_image_keep_ratio(self.flower_img, 120, 120)
            screen.blit(flower_scaled, (460 + fx, 260 + fy))
        else:
            pygame.draw.rect(screen, COLORS['pink'], (460, 260, 120, 120))

        # Glow effect after watering
        if self.x17_watered:
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pulse = 100 + 50 * math.sin(pygame.time.get_ticks() * 0.003)
            glow_surf.fill((255, 255, 200, int(pulse)))
            screen.blit(glow_surf, (410, 210))

        # Label
        label_surf = render_text(make_font(14), "SPECIMEN X-17",
                                 COLORS['white'])
        screen.blit(label_surf, (465, 380))

        # Intercom
        if self.intercom_img:
            intercom_scaled, ix, iy = scale_image_keep_ratio(
                self.intercom_img, self.intercom_rect.width, self.intercom_rect.height)
            screen.blit(intercom_scaled, (self.intercom_rect.x + ix, self.intercom_rect.y + iy))
        else:
            pygame.draw.rect(screen, COLORS['gray'], self.intercom_rect)
            pygame.draw.rect(screen, COLORS['white'], self.intercom_rect, 1)
            intercom_lbl = render_text(make_font(12), "INTERCOM",
                                       COLORS['dark_gray'])
            screen.blit(intercom_lbl, (910, 350))

        # Mara
        if not self.mara_left and self.mara_img:
            mara_scaled, mfx, mfy = scale_image_keep_ratio(self.mara_img, 700, 700)
            screen.blit(mara_scaled, (162 + mfx, mfy))
            mara_lbl = render_text(make_font(14), "Mara",
                                    COLORS['white'])
            screen.blit(mara_lbl, (262, 600))
        elif not self.mara_left:
            mara_surf = pygame.Surface((80, 180), pygame.SRCALPHA)
            pygame.draw.circle(mara_surf, COLORS['blue'], (40, 60), 30)
            pygame.draw.rect(mara_surf, COLORS['blue'],
                             pygame.Rect(10, 80, 60, 100))
            screen.blit(mara_surf, (60, 300))
            mara_lbl = render_text(make_font(14), "Mara",
                                    COLORS['white'])
            screen.blit(mara_lbl, (70, 490))

        # Particles
        self.particles.update(0.016)
        self.particles.draw(screen)

        # Instructions
        hint1 = render_text(make_font(20),
                            "Water X-17 with 500 ml",
                            COLORS['white'])
        hint2 = render_text(make_font(20),
                            "Use watering can from inventory → Click X-17",
                            COLORS['gray'])
        screen.blit(hint1, (20, 720))
        screen.blit(hint2, (20, 750))

    def update(self, events: list):
        """Handle watering scene interactions."""
        if self.entered:
            return

        self.elapsed_frames += 1
        self._check_horror_transition()

        # Add ambient particles
        if len(self.particles.particles) < 10:
            self.particles.add_ambient(510, 300, 1)

        # Radio call trigger (after 5 seconds)
        x17_was_watered = self.x17_watered or self.game.flags.get('x17_watered', False)
        if x17_was_watered and not self.mara_paged and self.elapsed_frames > 300:
            self._radio_call()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # X-17
                if self.x17_rect.collidepoint(pos):
                    x17_was_watered = self.x17_watered or self.game.flags.get('x17_watered', False)
                    if not x17_was_watered:
                        self._water_x17()
                    elif not self.mara_left:
                        self.game.dialogue.show_dialogue(
                            "Nothing happens yet.\nThat's it?\nWhat were you "
                            "expecting?\nI don't know.\nThat's research.",
                            "Elias")
                    else:
                        self._x17_after_mara()

                # Intercom
                elif self.intercom_rect.collidepoint(pos):
                    if self.mara_left:
                        self._use_intercom()
                    else:
                        self.game.dialogue.show_dialogue(
                            "Intercom is active but Mara is right here.",
                            "Elias")

                # Mara
                elif self.mara_rect.collidepoint(pos):
                    if not self.mara_left:
                        self.game.dialogue.show_dialogue(
                            "Go ahead with the watering.\nI'll be back.",
                            "Mara")
                    else:
                        self.game.dialogue.show_dialogue(
                            "Mara is gone. The greenhouse feels quieter.",
                            "Elias")

    def _water_x17(self):
        """Attempt to water X-17."""
        can = self.game.inventory.get_selected_item()
        if can and '500' in can.get('name', ''):
            self.x17_watered = True
            self.game.dialogue.show_dialogue(
                "Elias carefully waters the plant.\nSlowly.\nThe watering "
                "finishes.",
                "Elias")
            self.game.journal.complete_objective('obj_water_x17_done')
            self.game.journal.add_objective('obj_wait',
                                            'Wait for reaction',
                                            'Observe X-17 for changes')
        elif can and 'Empty' in can.get('name', ''):
            self.game.dialogue.show_dialogue(
                "The watering can is empty.\nI need to fill it with 500 ml "
                "filtered water.",
                "Elias")
        else:
            self.game.dialogue.show_dialogue(
                "I need to select the watering can first.",
                "Elias")

    def _radio_call(self):
        """Trigger Mara's radio call."""
        self.mara_paged = True
        self.game.dialogue.show_dialogue(
            "SFX: Radio static crackles through the greenhouse.",
            "System")

        self.game.dialogue.show_dialogue(
            "Dr. Vale.\nReport to Lab Two immediately.\nI'm coming.",
            "Radio")

        self.game.dialogue.show_dialogue(
            "Finish the observation record.\nThen leave.\nYou're leaving me "
            "here?\nIt's a greenhouse, Elias.\nWhat could happen?",
            "Mara")

        self.game.dialogue.show_dialogue(
            "Elias.\nIf you hear anything unusual--\nNothing.\nFinish your "
            "work.",
            "Mara")

        self.mara_left = True
        self.game.dialogue.show_dialogue(
            "SFX: Greenhouse door closes.\nSFX: Electronic lock engages.\nThe "
            "greenhouse ambience becomes quieter.",
            "System")

        self.game.journal.update_objective('obj_wait',
                                           'Complete observation',
                                           'Inspect X-17 again')
        self.game.sanity.decrease_sanity(5)

    def _x17_after_mara(self):
        """X-17 interaction after Mara leaves."""
        self.game.dialogue.show_dialogue(
            "Observe X-17 for supernatural changes.",
            "Elias",
            ["Inspect petals", "Inspect stem", "Inspect root area"],
            lambda c: self._observe_choice(c))

    def _observe_choice(self, choice: str):
        """Handle observation choices after Mara leaves."""
        if choice == "Inspect petals":
            self.game.dialogue.show_dialogue(
                "No visible change in--\nThe petal moves.\nElias stops "
                "speaking.\nSilence.\n...What?",
                "Elias",
                ["Inspect again", "Ignore it"],
                lambda c: self._petal_event(c))
        elif choice == "Inspect stem":
            self.game.dialogue.show_dialogue(
                "Slight discoloration near the base.\nIt's moving.\nElias "
                "steps back.",
                "Elias",
                ["Inspect again", "Ignore it"],
                lambda c: self._petal_event(c))
        else:
            self.game.dialogue.show_dialogue(
                "The soil is damp.\nSomething is growing beneath it.\nElias "
                "feels uneasy.",
                "Elias",
                ["Inspect again", "Ignore it"],
                lambda c: self._petal_event(c))

    def _petal_event(self, choice: str):
        """Trigger the first supernatural event."""
        if choice == "Inspect again":
            self.x17_glowing = True
            self.game.dialogue.show_dialogue(
                "The camera moves closer to the flower.\nNothing happens.\n"
                "Probably water movement.",
                "Elias")
            self.game.sanity.decrease_sanity(5)
            self.game.flags['first_horror_response'] = 'investigate'
        else:
            self.game.dialogue.show_dialogue(
                "Elias moves away from the flower.\nProbably nothing.",
                "Elias")
            self.game.sanity.decrease_sanity(5)
            self.game.flags['first_horror_response'] = 'ignore'

        self._trigger_glow()

    def _use_intercom(self):
        """Use the intercom after Mara leaves."""
        self.game.dialogue.show_dialogue(
            "Dr. Vale?\nMara, are you there?\nStatic continues.\nThen a faint "
            "voice emerges.\nI'm here.\nThe intercom shuts down.\nNo.",
            "Elias")
        self.game.sanity.decrease_sanity(10)
        self.game.flags['first_horror_response'] = 'intercom'

    def _trigger_glow(self):
        """Trigger X-17 glow effect."""
        self.x17_glowing = True
        self.particles.add_pollen(510, 310, 20)
        self.game.journal.update_objective('obj_wait',
                                            'Investigate the change in X-17',
                                            'Click the glowing X-17')
        self.game.flags['first_supernatural_observed'] = True
        self._schedule_horror_transition()

    def _schedule_horror_transition(self):
        """Schedule transition to Scene 5 horror after delay."""
        if not hasattr(self, '_transition_timer'):
            self._transition_timer = 0
        self._transition_timer = 180  # 3 seconds at 60fps

    def _check_horror_transition(self):
        """Check if it's time to transition to Scene 5."""
        if hasattr(self, '_transition_timer') and self._transition_timer > 0:
            self._transition_timer -= 1
            if self._transition_timer <= 0:
                self._go_to_horror()

    def _go_to_horror(self):
        """Transition to Chapter 4 horror sequence."""
        from blooming.scenes.chapter4_horror import Chapter4_Horror
        if self.game.scenes['horror'] is None:
            self.game.scenes['horror'] = Chapter4_Horror(self.game)
        self.game.current_scene = self.game.scenes['horror']
        self.game.current_scene.phase = 1
        self.game.flags['entered_horror_scene'] = True
        self.game.sanity.decrease_sanity(10)
        self.game.journal.add_objective('obj_climax',
                                         'Survive the supernatural event',
                                         'Respond to the horror sequence')
