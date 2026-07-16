"""Scene 5 - Supernatural Event & Ending (Member D)

The supernatural sequence: X-17 glows, whispers,
player makes horror response choices, and the game ends.
Includes screen shake, hallucination, and title card.
"""

import math
import pygame
from blooming.utils.utils import render_text, make_font, load_image, scale_image_keep_ratio
from blooming.utils import COLORS
from blooming.utils.particles import ParticleSystem
from blooming.utils.screen_shake import ScreenShake


class Scene5_Horror:
    """Scene 5: Supernatural horror sequence and ending."""

    def __init__(self, game):
        self.game = game
        self.font = make_font(32)
        self.small_font = make_font(24)
        self.small_font2 = make_font(20)

        # State
        self.phase = 0  # 0: alone, 1: glow, 2: whispers, 3: climax, 4: title
        self.timer = 0
        self.whisper_counter = 0
        self.response_given = False

        # Images
        self.interior_img = load_image('backgrounds/greenhouse-horror.png')
        self.flower_glow_img = load_image('props/flower-glow.png')
        self.flower_img = load_image('props/flower.png')
        self.flower_closed_img = load_image('props/flower-glowing-closed.png')
        self.heart_img = load_image('ending/heart-pulse.png')
        self.root_img = load_image('ending/root.png')
        self.title_img = load_image('ending/title-card.png')
        self.vine_img = load_image('vfx/vine-overlay.png')
        self.flicker_img = load_image('vfx/screen-flicker.png')

        # Effects
        self.particles = ParticleSystem()
        self.shake = ScreenShake()

        # Flicker
        self.flicker_active = False
        self.flicker_timer = 0

    @property
    def active(self):
        return self.phase < 5

    def draw(self, screen):
        """Draw the horror sequence."""
        if self.phase >= 4:
            return

        # Shake offset
        offset_x, offset_y = self.shake.get_offset()
        screen_area = pygame.Rect(offset_x, offset_y, 1024, 768)

        # Background
        if self.interior_img:
            bg_scaled, bx, by = scale_image_keep_ratio(self.interior_img, 1024, 768)
            screen.blit(bg_scaled, (bx, by))
        else:
            # Darken background progressively
            darkness = min(200, self.phase * 40)
            screen.fill((darkness, darkness - 20, darkness))

        # Rows of plants (fading)
        plant_alpha = max(0, 255 - self.phase * 50)
        for i in range(0, 1024, 150):
            ps = pygame.Surface((60, 100), pygame.SRCALPHA)
            ps.fill((20, 80, 20, plant_alpha))
            screen.blit(ps, (i, 350))

        # Central specimen table
        table_rect = pygame.Rect(400, 370, 220, 130)
        table_surf = pygame.Surface((220, 130), pygame.SRCALPHA)
        t_alpha = max(0, 255 - self.phase * 40)
        table_surf.fill((100, 80, 60, t_alpha))
        screen.blit(table_surf, (400, 370))

        # X-17 glow effect
        if self.phase >= 3 and self.flower_closed_img:
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pulse = 150 + 80 * math.sin(self.timer * 0.15)
            glow_surf.fill((255, 200, 150, int(pulse)))
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - 100, 200))
            flower_scaled, ffx, ffy = scale_image_keep_ratio(self.flower_closed_img, 150, 150)
            screen.blit(flower_scaled, (SCREEN_WIDTH // 2 - 75 + ffx, 200 + ffy))
        elif self.phase >= 1 and self.flower_glow_img:
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pulse = 100 + 50 * math.sin(self.timer * 0.1)
            glow_surf.fill((255, 255, pulse, 100))
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - 100, 200))
            flower_scaled, ffx, ffy = scale_image_keep_ratio(self.flower_glow_img, 150, 150)
            screen.blit(flower_scaled, (SCREEN_WIDTH // 2 - 75 + ffx, 200 + ffy))
        elif self.phase >= 1 and self.flower_img:
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pulse = 100 + 50 * math.sin(self.timer * 0.1)
            glow_surf.fill((255, 255, pulse, 100))
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - 100, 200))
            flower_scaled, ffx, ffy = scale_image_keep_ratio(self.flower_img, 150, 150)
            screen.blit(flower_scaled, (SCREEN_WIDTH // 2 - 75 + ffx, 200 + ffy))
        elif self.phase >= 1:
            glow_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            pulse = 100 + 50 * math.sin(self.timer * 0.1)
            glow_surf.fill((255, 255, pulse, 100))
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - 100, 200))
            pygame.draw.rect(screen, (255, 200, 220),
                             (SCREEN_WIDTH // 2 - 60, 210, 120, 120))

        # Phase 2+: vines/roots growing
        if self.phase >= 2 and self.vine_img:
            vine_scaled, vx, vy = scale_image_keep_ratio(self.vine_img, 1024, 768)
            screen.blit(vine_scaled, (vx, vy))
        elif self.phase >= 2:
            for i in range(5):
                vine_color = (128, 0, 128)
                y1 = 500 + i * 20
                y2 = 600 + i * 20
                pygame.draw.line(screen, vine_color,
                                 (i * 200, y1), (i * 200 + 50, y2), 10)

        # Phase 3: darkness overlay
        if self.phase >= 3:
            darkness_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
            alpha = min(200, (self.timer - 300) * 2)
            darkness_surf.fill((0, 0, 0, alpha))
            screen.blit(darkness_surf, (0, 0))

        # Phase 4: title card
        if self.phase >= 4:
            if self.title_img:
                title_scaled, tx, ty = scale_image_keep_ratio(self.title_img, 1024, 768)
                screen.blit(title_scaled, (tx, ty))
            else:
                self._draw_title_card(screen)

        # Particles
        self.particles.update(0.016)
        self.particles.draw(screen)

        self.shake.update()

        # Phase text
        if self.phase == 0:
            s = render_text(self.font, "I'm alone now...", COLORS['white'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 100, 150))
        elif self.phase == 1:
            s = render_text(self.font, "The flower... it's glowing!",
                            COLORS['yellow'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 180, 150))
        elif self.phase == 2:
            s = render_text(self.font, "Whispers... I hear whispers!",
                            COLORS['red'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 200, 150))
        elif self.phase == 3:
            s = render_text(self.font, "ELIAS...", COLORS['red'])
            screen.blit(s, (SCREEN_WIDTH // 2 - 50, 150))

        # Instructions
        if self.phase < 3 and not self.response_given:
            hint = render_text(self.small_font2,
                               "Click X-17 to investigate",
                               COLORS['white'])
            screen.blit(hint, (20, 720))

    def _draw_title_card(self, screen):
        """Draw END OF DAY 1 title card."""
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        title_surf = render_text(self.font, "END OF DAY 1", COLORS['red'])
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        sub_surf = render_text(self.small_font2, "SFX: DISTANT WHISPER",
                               COLORS['gray'])
        screen.blit(sub_surf, (SCREEN_WIDTH // 2 - 150,
                               SCREEN_HEIGHT // 2 + 50))

    def update(self, events: list):
        """Update horror sequence phases."""
        self.timer += 1

        # Phase progression
        if self.phase == 0 and self.timer > 120:
            self.phase = 1
            self.particles.add_pollen(510, 300, 15)

        elif self.phase == 1 and self.timer > 240:
            self.phase = 2
            self.game.sanity.decrease_sanity(10)
            self.shake.shake(5, 30)

        elif self.phase == 2:
            # Whispers
            if self.timer % 90 == 0 and self.whisper_counter < 5:
                self.whisper_counter += 1
                self.game.sanity.decrease_sanity(10)
                self.shake.shake(10, 30)
                self.particles.add_spore(510, 300, 10)
                self.game.dialogue.show_dialogue(
                    "Elias...",
                    "???")
            if self.whisper_counter >= 5:
                self.phase = 3

        elif self.phase == 3 and self.timer > 360:
            self.phase = 4
            self.game.journal.add_objective('ending',
                                            'End of Day 1',
                                            'The greenhouse door closes behind you')
            if not hasattr(self, '_ending_timer'):
                self._ending_timer = 0
            self._ending_timer = 300  # 5 seconds before ending

        elif self.phase == 4:
            if hasattr(self, '_ending_timer'):
                self._ending_timer -= 1
                if self._ending_timer <= 0:
                    self._go_to_ending()

        # Spawn spores during horror
        if self.phase >= 1 and self.timer % 10 == 0:
            self.particles.add_spore(SCREEN_WIDTH // 2, 300, 1)

        # Flicker effect
        if self.phase >= 2 and self.timer % 60 < 30:
            self.flicker_active = True
            self.flicker_timer += 1
        else:
            self.flicker_active = False

        if self.flicker_active and self.flicker_img:
            flicker_scaled, fx, fy = scale_image_keep_ratio(self.flicker_img, 1024, 768)
            self.game.screen.blit(flicker_scaled, (fx, fy))
        elif self.flicker_active:
            flicker_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
            flicker_surf.fill((0, 0, 0, 80))
            self.game.screen.blit(flicker_surf, (0, 0))

        # Handle player response
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if self.phase < 3 and not self.response_given:
                    # Check X-17 click
                    x17_rect = pygame.Rect(450, 250, 120, 120)
                    if x17_rect.collidepoint(pos):
                        self.response_given = True
                        self._give_horror_response()

                # Intercom option
                elif self.phase < 3 and not self.response_given:
                    intercom_rect = pygame.Rect(900, 300, 100, 120)
                    if intercom_rect.collidepoint(pos):
                        self.response_given = True
                        self.game.dialogue.show_dialogue(
                            "Dr. Vale?\nMara, are you there?\nStatic... then: "
                            "I'm here.\nThe intercom shuts down.",
                            "Elias")
                        self.game.flags['first_horror_response'] = 'intercom'
                        self.game.sanity.decrease_sanity(10)

                # Exit option
                elif self.phase < 3 and not self.response_given:
                    exit_rect = pygame.Rect(100, 500, 150, 60)
                    if exit_rect.collidepoint(pos):
                        self.response_given = True
                        self.game.dialogue.show_dialogue(
                            "Elias walks toward the door.\nDon't go.\nSFX: "
                            "Electrical buzz.\nWho's there?",
                            "Elias")
                        self.game.flags['first_horror_response'] = 'escape'
                        self.game.sanity.decrease_sanity(10)

                # ESC to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.running = False

    def _give_horror_response(self):
        """Set horror response flag and advance to ending."""
        x17_rect = pygame.Rect(450, 250, 120, 120)
        if x17_rect.collidepoint(pygame.mouse.get_pos()):
            self.game.dialogue.show_dialogue(
                "I'm talking to a plant.",
                "Elias")
            self.game.flags['first_horror_response'] = 'flower'
            self.game.sanity.decrease_sanity(15)
        self.shake.shake(20, 60)
        self.particles.add_spore(510, 300, 30)
        self.phase = 3
        self.game.journal.add_objective('ending',
                                        'The Blooming',
                                        'Experience the end of Day 1')

    def _go_to_ending(self):
        """Transition to the final ending scene."""
        if self.game.scenes['ending'] is None:
            self.game.scenes['ending'] = Scene5_Ending(self.game)
        self.game.current_scene = self.game.scenes['ending']


class Scene5_Ending:
    """Final ending scene."""

    def __init__(self, game):
        self.game = game
        self.font = make_font(32)
        self.small_font = make_font(24)
        self.timer = 0
        self.root_img = load_image('ending/root.png')

    @property
    def active(self):
        return True  # Runs until ESC

    def draw(self, screen):
        """Draw the final ending."""
        if self.timer < 100:
            # The Blooming title
            title_surf = render_text(self.font, "The Blooming...",
                                     COLORS['red'])
            screen.blit(title_surf, (SCREEN_WIDTH // 2 - 120,
                                     SCREEN_HEIGHT // 2))
        elif self.timer < 200:
            # END OF DAY 1
            title_surf = render_text(self.font, "END OF DAY 1",
                                     COLORS['white'])
            screen.blit(title_surf, (SCREEN_WIDTH // 2 - 100,
                                     SCREEN_HEIGHT // 2))
        else:
            # GAME OVER
            s1 = render_text(self.font, "GAME OVER", COLORS['red'])
            s2 = render_text(self.small_font, "Press ESC to exit",
                             COLORS['white'])
            screen.blit(s1, (SCREEN_WIDTH // 2 - 100,
                             SCREEN_HEIGHT // 2 - 30))
            screen.blit(s2, (SCREEN_WIDTH // 2 - 120,
                             SCREEN_HEIGHT // 2 + 30))

    def update(self, events: list):
        """Update ending scene."""
        self.timer += 1
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False


# Constants needed for Scene5_Horror
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
