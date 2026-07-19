"""Chapter 1 - Arrival at Blackwood Research Facility (Member A)

Player arrives at the facility, meets Dr. Mara Vale,
receives an access card, and enters the building.

Matches screenplay SEQ 01 and SEQ 02 exactly.

Visual novel style:
- Background fades in
- Character fades in
- Dialogue auto-plays with typewriter effect
- Player clicks to advance through lines
"""

import pygame
import math
import random
from blooming.utils.utils import render_text, make_font, load_image, scale_image_keep_ratio
from blooming.utils import COLORS


class Chapter1_Arrival:
    """Scene 1: Arrival at facility entrance.

    Visual novel style intro:
    1. Background fades in over 1.5s
    2. Character fades in over 0.8s
    3. Dialogue auto-plays (click to skip/advance)
    """

    def __init__(self, game):
        self.game = game
        self.font = make_font(32)
        self.small_font = make_font(24)

        # Hotspot rects
        self.sign_rect = pygame.Rect(100, 100, 150, 80)
        self.intercom_rect = pygame.Rect(850, 300, 100, 100)
        self.door_rect = pygame.Rect(400, 250, 224, 318)
        self.mara_rect = pygame.Rect(162, 30, 700, 708)

        # State machine
        self.phase = 'greeting'
        self.door_locked = True
        self.sign_read = False
        self.intercom_used = False
        self.door_clicked_before_card = False

        # Images
        self.exterior_img = load_image('backgrounds/greenhouse-exterior.png')
        self.mara_img = load_image('char/mara-vale.png')
        self.door_img = load_image('props/security-door.png')
        self.sign_img = load_image('props/facility-sign.png')
        self.intercom_img = load_image('props/intercom.png')
        self.access_card_img = load_image('props/access-card.png')

        # Parallax fog layers
        self.fog_layer_offset = 0
        self.fog_layers = [
            {'speed': 0.3, 'alpha': 40, 'scale': 1.0, 'color': (180, 190, 200)},
            {'speed': 0.6, 'alpha': 60, 'scale': 0.8, 'color': (160, 175, 190)},
            {'speed': 1.0, 'alpha': 80, 'scale': 0.5, 'color': (140, 160, 185)},
        ]

        # Card holographic shimmer
        self.holo_hue = 0.0
        self.holo_speed = 0.02

        # Intercom static effect
        self.intercom_static_timer = 0
        self.intercom_static_active = False

        # Door LED scan line
        self.scan_line_y = 250
        self.scan_line_speed = 2

        # Mara breathing animation
        self.breath_phase = 0.0
        self.breath_speed = 0.03



        # Rain particles (constant angle, varied speed/spacing)
        self.raindrops = []
        self.rain_angle = 20  # degrees (wind from left)
        random.seed(42)
        for i in range(200):
            self.raindrops.append({
                'x': random.random() * 1024,
                'y': -50 - 200 * random.random(),
                'speed': 2.0 + 3.0 * random.random(),
                'length': 15 + 25 * random.random(),
                'alpha': 180 + 75 * random.random(),
                'hue': random.random(),
            })

        # Vignette parameters
        self.vignette_strength = 0.6

        # Mara position
        self.mara_x = 350
        self.mara_target_x = 500
        self.mara_animating = False

        # Fade-in system: start fully black, fade to 0 (reveal scene)
        self.fade_alpha = 255
        self.fade_target = 0
        self.fade_duration = 90
        self.fade_elapsed = 0
        self.fade_active = True
        # Character fade
        self.mara_alpha = 0  # starts invisible, fades to 255
        self.mara_alpha_target = 255
        self.mara_alpha_duration = 48
        self.mara_alpha_elapsed = 0
        self.mara_fade_active = False

        # Dialogue sequence
        self.greeting_idx = 0
        self.greeting_lines = [
            ("You must be Elias.", "Mara"),
            ("Dr. Vale?", "Elias"),
            ("Mara is fine.", "Mara"),
            ("You found the place without getting lost.\n"
             "That's already better than our last intern.", "Mara"),
            ("I'm not an intern.", "Elias"),
            ("Then you'll have even fewer excuses.", "Mara"),
        ]
        self.greeting_done = False
        self.dialogue_playing = False
        self.dialogue_line_idx = 0
        self.dialogue_lines = []

        # Card handoff animation
        self.card_overlay_active = False
        self.card_overlay_alpha = 0
        self.card_overlay_timer = 0
        self.card_overlay_duration = 90  # frames (~1.5s) fade in
        self.card_overlay_max_alpha = 230
        self.card_showing = False
        self.card_fade_out_timer = 0
        self.card_fade_out_duration = 75  # frames (~1.25s) fade out
        self.card_given_to_inventory = False

        # Card handoff lines from screenplay
        self.card_lines = [
            ("Here. Take this.", "Mara"),
            ("My access card?", "Elias"),
            ("Level One.\n"
             "Greenhouse, staff office, archive corridor.", "Mara"),
            ("And the other rooms?", "Elias"),
            ("Not your concern.", "Mara"),
            ("Select the card from your equipment.\n"
             "Then use it on the security panel\n"
             "beside the door.", "Mara"),
        ]
        self.card_idx = 0
        self.card_done = False

        # Entrance lines from screenplay
        self.entrance_lines = [
            ("There you go.\n"
             "You'll use equipment the same way.\n"
             "Choose what you need...\n"
             "then use it where it belongs.", "Mara"),
            ("After you.", "Mara"),
        ]
        self.entrance_idx = 0
        self.entrance_done = False

        # Corridor intro lines (SEQ 02)
        self.corridor_lines = [
            ("The greenhouse is at the end of the corridor.", "Mara"),
            ("My office is on the left.", "Mara"),
            ("Storage is opposite it.", "Mara"),
        ]
        self.corridor_idx = 0
        self.corridor_done = False

        # Rules lines from screenplay SEQ 02
        self.rules_lines = [
            ("Before we go inside, one rule.", "Mara"),
            ("Only one?", "Elias"),
            ("Don't remove anything from the greenhouse\n"
             "without authorization.", "Mara"),
            ("Understood.", "Elias"),
            ("And don't move any specimen unless you're told.", "Mara"),
            ("That's two rules.", "Elias"),
            ("You're observant.\nGood start.", "Mara"),
        ]
        self.rules_idx = 0
        self.rules_done = False

    def _get_holo_color(self, hue):
        """Generate holographic color from hue value."""
        r = int(128 + 127 * (0.5 + 0.5 * (3.0 * hue)))
        g = int(128 + 127 * (0.5 + 0.5 * (3.0 * hue + 1.0) % 3.0))
        b = int(128 + 127 * (0.5 + 0.5 * (3.0 * hue + 2.0) % 3.0))
        return (min(255, r), min(255, g), min(255, b))

    def _render_glowing_text(self, font, text, color, glow_color=(255, 255, 200), glow_size=3):
        """Render text with a glowing outline effect."""
        # Create glow layers
        glow_surf = pygame.Surface(font.size(text), pygame.SRCALPHA)
        for offset_x in range(-glow_size, glow_size + 1):
            for offset_y in range(-glow_size, glow_size + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                glow_surf.blit(font.render(text, True, glow_color),
                             (offset_x, offset_y))
        
        # Draw main text on top
        text_surf = font.render(text, True, color)
        glow_surf.blit(text_surf, (0, 0))
        return glow_surf

    def draw(self, screen):
        """Draw the arrival scene with fade overlay."""
        if self.phase == 'done':
            return

        # Draw scene
        if self.exterior_img:
            bg_scaled, bx, by = scale_image_keep_ratio(self.exterior_img, 1024, 768)
            screen.blit(bg_scaled, (bx, by))
        else:
            screen.fill(COLORS['dark_fog'])
            # Parallax fog layers
            for layer in self.fog_layers:
                offset = pygame.time.get_ticks() * layer['speed'] / 100
                for i in range(-1, 6):
                    fog_surf = pygame.Surface((200, 768), pygame.SRCALPHA)
                    fog_surf.fill((*layer['color'], layer['alpha']))
                    screen.blit(fog_surf,
                                (i * 200 - (offset % 200), 0))

        # Draw rain particles (before vignette so not covered)
        # Fixed trajectory: down + slight right
        for rain in self.raindrops:
            dx = math.sin(math.radians(self.rain_angle))
            dy = math.cos(math.radians(self.rain_angle))
            rain_surf = pygame.Surface((3, rain['length']), pygame.SRCALPHA)
            grey = int(200 + 55 * rain['hue'])
            rain_surf.fill((grey, grey, grey, int(rain['alpha'])))
            # Rotate drop to align with movement direction
            drop_angle = math.degrees(math.atan2(dx, dy))
            rotated = pygame.transform.rotate(rain_surf, drop_angle)
            screen.blit(rotated, (rain['x'], rain['y']))
            rain['x'] += rain['speed'] * dx
            rain['y'] += rain['speed'] * dy
            if rain['y'] > 768:
                rain['y'] = -rain['length']
                rain['x'] = random.random() * 1024

        # Draw vignette overlay
        if not self.fade_active:
            vignette = pygame.Surface((1024, 768), pygame.SRCALPHA)
            for i in range(100):
                alpha = int(self.vignette_strength * 255 * (1 - i / 100))
                color = (0, 0, 0, alpha)
                rect = pygame.Rect(i, i, 1024 - 2 * i, 768 - 2 * i)
                pygame.draw.rect(vignette, color, rect, 1)
            screen.blit(vignette, (0, 0))

        pygame.draw.rect(screen, COLORS['dark_gray'], (0, 550, 1024, 218))

        # Door
        if self.door_img:
            door_scaled, dx, dy = scale_image_keep_ratio(
                self.door_img, self.door_rect.width, self.door_rect.height)
            screen.blit(door_scaled, (self.door_rect.x + dx, self.door_rect.y + dy))
        else:
            door_color = (COLORS['red'] if self.door_locked
                          else COLORS['green'])
            pygame.draw.rect(screen, COLORS['dark_gray'], self.door_rect)
            pygame.draw.rect(screen, door_color,
                             pygame.Rect(420, 270, 184, 278))
            pygame.draw.rect(screen, COLORS['gray'], self.door_rect, 3)

        # Door indicator with scan line
        ind_x, ind_y = 630, 300
        ind_color = (COLORS['red'] if self.door_locked
                      else COLORS['green'])
        pygame.draw.circle(screen, ind_color, (ind_x, ind_y), 15)
        pygame.draw.circle(screen, COLORS['white'], (ind_x, ind_y), 15, 2)
        
        # LED scan line on door
        scan_x = self.door_rect.x + 20
        scan_y = self.scan_line_y
        if scan_y >= self.door_rect.top and scan_y <= self.door_rect.bottom:
            scan_line = pygame.Surface((180, 3), pygame.SRCALPHA)
            scan_line.fill((100, 200, 255, 150))
            screen.blit(scan_line, (scan_x, scan_y))
        
        # Update scan line position
        self.scan_line_y += self.scan_line_speed
        if self.scan_line_y > self.door_rect.bottom:
            self.scan_line_y = self.door_rect.top
        
        ind_label = "LOCKED" if self.door_locked else "OPEN"
        ind_surf = render_text(make_font(12), ind_label, COLORS['white'])
        screen.blit(ind_surf, (ind_x - 25, ind_y + 20))

        # Sign
        if self.sign_img:
            sign_scaled, sx, sy = scale_image_keep_ratio(
                self.sign_img, self.sign_rect.width, self.sign_rect.height)
            screen.blit(sign_scaled, (self.sign_rect.x + sx, self.sign_rect.y + sy))
        else:
            pygame.draw.rect(screen, COLORS['gray'], self.sign_rect)
            pygame.draw.rect(screen, COLORS['white'], self.sign_rect, 1)
            for i, t in enumerate(["BLACKWOOD", "BOTANICAL", "RESEARCH"]):
                s = render_text(self.small_font, t, COLORS['white'])
                screen.blit(s, (110, 115 + i * 28))
            sub = render_text(self.small_font,
                              "AUTHORIZED PERSONNEL ONLY", COLORS['gray'])
            screen.blit(sub, (110, 220))

        # Intercom
        if self.intercom_img:
            intercom_scaled, ix, iy = scale_image_keep_ratio(
                self.intercom_img, self.intercom_rect.width, self.intercom_rect.height)
            screen.blit(intercom_scaled, (self.intercom_rect.x + ix, self.intercom_rect.y + iy))
        else:
            pygame.draw.rect(screen, COLORS['gray'], self.intercom_rect)
            pygame.draw.rect(screen, COLORS['white'], self.intercom_rect, 1)
            spk = render_text(self.small_font, "INTERCOM", COLORS['dark_gray'])
            screen.blit(spk, (self.intercom_rect.x + 5,
                              self.intercom_rect.y + 40))

        # Mara with breathing animation and blink
        mx = int(self.mara_x)
        breath_phase = (pygame.time.get_ticks() * 0.002) % (2 * math.pi)
        breath_scale = 1.0 + 0.015 * math.sin(breath_phase)
        
        if self.mara_img:
            mara_scaled, mfx, mfy = scale_image_keep_ratio(self.mara_img, 700, 700)
            
            # Apply breathing scale
            if not self.mara_fade_active:
                scaled_w = int(700 * breath_scale)
                scaled_h = int(700 * breath_scale)
                mara_scaled = pygame.transform.scale(self.mara_img, (scaled_w, scaled_h))
            
            # Apply character fade
            if self.mara_alpha < 255:
                mara_scaled.set_alpha(self.mara_alpha)
            
            screen.blit(mara_scaled, (mx, mfy))
        else:
            mara_surf = pygame.Surface((100, 200), pygame.SRCALPHA)
            pygame.draw.circle(mara_surf, COLORS['blue'], (50, 100), 40)
            pygame.draw.circle(mara_surf, COLORS['white'], (50, 100), 40, 2)
            if self.mara_alpha < 255:
                mara_surf.set_alpha(self.mara_alpha)
            screen.blit(mara_surf, (mx, 300))
        
        mara_lbl = render_text(make_font(14), "Mara", COLORS['white'])
        screen.blit(mara_lbl, (mx + 200, 600))

        # Large centered card overlay (fade in/out handoff animation)
        if self.card_overlay_active and self.access_card_img:
            overlay_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
            overlay_surf.fill((0, 0, 0, 100))
            screen.blit(overlay_surf, (0, 0))

            # Position card at center of screen
            card_scaled, cx, cy = scale_image_keep_ratio(self.access_card_img, 300, 190)
            card_scaled.set_alpha(self.card_overlay_alpha)
            
            # Holographic shimmer effect
            holo_color = self._get_holo_color(self.holo_hue)
            holo_surf = pygame.Surface((300, 190), pygame.SRCALPHA)
            holo_surf.fill((*holo_color, int(80 + 40 * (pygame.time.get_ticks() % 100) / 100)))
            card_scaled.blit(holo_surf, (0, 0), pygame.BLEND_RGBA_ADD)
            
            screen.blit(card_scaled, (362 + cx, 289 + cy))
            self.holo_hue = (self.holo_hue + self.holo_speed) % 1.0

            label = render_text(make_font(20), "ACCESS CARD (LEVEL 1)",
                                COLORS['white'])
            screen.blit(label, (512 - 100, 230))
        
        # Update holographic hue even when card not showing
        self.holo_hue = (self.holo_hue + self.holo_speed) % 1.0



        # Fade overlay
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
            fade_surf.fill((0, 0, 0, self.fade_alpha))
            screen.blit(fade_surf, (0, 0))

    def update(self, events: list):
        """Handle scene with visual novel style flow.

        Phase flow:
        1. 'fade_in' -> background/character fade in
        2. 'greeting' -> auto-play dialogue, click to advance
        3. 'player_control' -> click hotspots
        4. 'card_given' -> click to advance through card dialogue
        5. 'door_unlocked' -> use card on door
        6. 'done' -> transition to Scene 2
        """
        if self.phase == 'done':
            return

        # Update fade: 255 → 0 (reveal scene)
        if self.fade_active:
            self.fade_elapsed += 1
            progress = self.fade_elapsed / self.fade_duration
            self.fade_alpha = int(255 * (1 - progress))
            if self.fade_elapsed >= self.fade_duration:
                self.fade_alpha = 0
                self.fade_active = False
                self.mara_fade_active = True
                self.mara_alpha_elapsed = 0

        # Update Mara fade
        if self.mara_fade_active:
            self.mara_alpha_elapsed += 1
            progress = self.mara_alpha_elapsed / self.mara_alpha_duration
            self.mara_alpha = int(self.mara_alpha_target * (1 - progress))
            if self.mara_alpha_elapsed >= self.mara_alpha_duration:
                self.mara_alpha = 255
                self.mara_fade_active = False
                # Start dialogue
                self._start_dialogue()

        # Animate Mara walking
        if self.mara_animating:
            self.mara_x += (self.mara_target_x - self.mara_x) * 0.05
            if abs(self.mara_x - self.mara_target_x) < 1:
                self.mara_animating = False
                self.mara_x = self.mara_target_x

        # Update card overlay animation
        if self.card_overlay_active and self.card_showing:
            self.card_overlay_timer += 1
            progress = self.card_overlay_timer / self.card_overlay_duration
            if progress <= 0.3:
                self.card_overlay_alpha = int(self.card_overlay_max_alpha * (progress / 0.3))
            else:
                self.card_overlay_alpha = self.card_overlay_max_alpha
            if self.card_overlay_timer >= self.card_overlay_duration:
                self.card_showing = False
                self.card_overlay_timer = 0
        elif self.card_overlay_active:
            self.card_fade_out_timer += 1
            progress = self.card_fade_out_timer / self.card_fade_out_duration
            self.card_overlay_alpha = int(self.card_overlay_max_alpha * (1 - progress))
            if self.card_fade_out_timer >= self.card_fade_out_duration:
                self.card_overlay_active = False
                self.card_overlay_alpha = 0
                self.card_fade_out_timer = 0
                if not self.card_given_to_inventory:
                    self.card_given_to_inventory = True
                    self.game.inventory.add_item('access_card', 'Access Card (Level 1)',
                                                 image_path='props/access-card.png')
        
        # Update intercom static timer
        if self.intercom_static_active:
            self.intercom_static_timer += 1

        # Process clicks
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # Still fading - no interaction
                if not self.fade_active and not self.mara_fade_active:
                    pass  # continue to dialogue/player control
                else:
                    continue

                # Dialogue playing: click to advance
                if self.dialogue_playing:
                    # If card is showing, player click to advance triggers fade-out
                    if self.card_showing:
                        self.card_showing = False
                        self.card_fade_out_timer = 0
                    self._advance_dialogue()
                    return

                # Player control: hotspots
                self._handle_player_control(pos)

    def _start_dialogue(self):
        """Start the greeting dialogue sequence."""
        self.dialogue_lines = self.greeting_lines[:]
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self._show_next_line()

    def _show_next_line(self):
        """Show the next dialogue line."""
        if self.dialogue_idx < len(self.dialogue_lines):
            text, speaker = self.dialogue_lines[self.dialogue_idx]
            self.game.dialogue.show_dialogue(text, speaker)

    def _advance_dialogue(self):
        """Advance to the next dialogue line or end dialogue."""
        if self.dialogue_idx < len(self.dialogue_lines):
            self.dialogue_idx += 1
            if self.dialogue_idx < len(self.dialogue_lines):
                text, speaker = self.dialogue_lines[self.dialogue_idx]
                self.game.dialogue.show_dialogue(text, speaker)
            else:
                # Card dialogue exhausted - start fade-out
                self.dialogue_playing = False
                self.dialogue_lines = []
                self.game.dialogue.clear()
                if self.phase == 'greeting':
                    self.phase = 'card_given'
                    self._start_card_handoff()
                elif self.phase == 'card_given':
                    self.card_done = True
        else:
            # Dialogue exhausted
            self.dialogue_playing = False
            self.dialogue_lines = []
            self.game.dialogue.clear()

    def _start_card_handoff(self):
        """Start the card handoff dialogue sequence."""
        self.dialogue_lines = self.card_lines[:]
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self.mara_animating = True
        self.mara_x = 420
        self.mara_target_x = 500
        self.card_overlay_active = True
        self.card_overlay_alpha = 0
        self.card_overlay_timer = 0
        self.card_showing = True
        self._show_next_line()

    def _handle_player_control(self, pos):
        """Handle player clicks during free exploration."""
        # Sign (optional)
        if self.sign_rect.collidepoint(pos) and not self.sign_read:
            self.sign_read = True
            self.game.dialogue.show_dialogue(
                "Blackwood Research Facility.", "Elias")

        # Intercom (optional)
        elif self.intercom_rect.collidepoint(pos) and not self.intercom_used:
            self.intercom_used = True
            self.intercom_static_active = True
            self.intercom_static_timer = 0
            self.game.dialogue.show_dialogue(
                "Security intercom.", "Elias")
        
        # Intercom static effect
        if self.intercom_static_active:
            self.intercom_static_timer += 1
            static_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            for _ in range(50):
                x = 50 * (hash(str(_ * 17)) % 100) // 100
                y = 50 * (hash(str(_ * 13)) % 100) // 100
                alpha = 100 + 100 * (hash(str(_ * 7)) % 55) // 55
                static_surf.set_at((x, y), (255, 255, 255, alpha))
            screen.blit(static_surf, (self.intercom_rect.x, self.intercom_rect.y))
            if self.intercom_static_timer > 30:
                self.intercom_static_active = False

        # Door
        elif self.door_rect.collidepoint(pos):
                    if self.phase == 'door_unlocked':
                        self._enter_facility()
                    elif self.card_done:
                        # Card received, check if player has it
                        if self.game.inventory.has_item('access_card'):
                            self.door_unlocked()
                        else:
                            self.game.dialogue.show_dialogue(
                                "Select the card from your equipment.\n"
                                "Then use it on the security panel.", "Mara")
                    else:
                        self.door_clicked_before_card = True
                        self.game.dialogue.show_dialogue(
                            "Locked.", "Elias")

        # Mara
        elif (self.mara_rect.collidepoint(pos) or
              pygame.Rect(int(self.mara_x), 300, 100, 200).collidepoint(pos)):
            if self.phase == 'card_given' and not self.card_done:
                self.phase = 'card_given'
                self._start_card_handoff()

    def door_unlocked(self):
        """Unlock the door after using the access card."""
        self.door_locked = False
        self.phase = 'door_unlocked'
        self.game.dialogue.show_dialogue(
            "There you go.\n"
            "You'll use equipment the same way.\n"
            "Choose what you need...\n"
            "then use it where it belongs.", "Mara")
        # Animate Mara walking toward door
        self.mara_animating = True
        self.mara_x = 500
        self.mara_target_x = 650

    def _enter_facility(self):
        """Transition to Scene 2. Matches screenplay SEQ 01 end."""
        self.phase = 'done'
        self.game.current_scene = Chapter1_Orientation(self.game)
        self.game.sanity.decrease_sanity(5)


class Chapter1_Orientation:
    """Scene 2: Facility corridor orientation.

    Visual novel style:
    1. Background fades in
    2. Character fades in
    3. Dialogue auto-plays (click to advance)
    """

    def __init__(self, game):
        self.game = game
        self.font = make_font(32)
        self.small_font = make_font(24)

        # Hotspot rects
        self.restricted_rect = pygame.Rect(50, 200, 200, 300)
        self.office_rect = pygame.Rect(300, 200, 200, 300)
        self.storage_rect = pygame.Rect(550, 200, 200, 300)
        self.greenhouse_rect = pygame.Rect(800, 200, 200, 300)
        self.mara_rect = pygame.Rect(650, 300, 100, 200)

        # State
        self.phase = 'corridor_intro'
        self.restricted_clicked = False
        self.office_clicked = False
        self.storage_clicked = False
        self.rules_done = False

        # Images
        self.corridor_img = load_image('backgrounds/corridor-exterior.png')
        self.mara_img = load_image('char/mara-vale.png')
        self.door_img = load_image('props/security-door.png')

        # Fade-in system: start black, fade to 0
        self.fade_alpha = 255
        self.fade_target = 0
        self.fade_duration = 90
        self.fade_elapsed = 0
        self.fade_active = True
        self.mara_alpha = 0
        self.mara_alpha_target = 255
        self.mara_alpha_duration = 48
        self.mara_alpha_elapsed = 0
        self.mara_fade_active = False

        # Dialogue
        self.dialogue_lines = []
        self.dialogue_idx = 0
        self.dialogue_playing = False

        # Corridor intro lines
        self.corridor_lines = [
            ("The greenhouse is at the end of the corridor.", "Mara"),
            ("My office is on the left.", "Mara"),
            ("Storage is opposite it.", "Mara"),
        ]
        self.corridor_idx = 0
        self.corridor_done = False

        # Rules lines
        self.rules_lines = [
            ("Before we go inside, one rule.", "Mara"),
            ("Only one?", "Elias"),
            ("Don't remove anything from the greenhouse\n"
             "without authorization.", "Mara"),
            ("Understood.", "Elias"),
            ("And don't move any specimen unless you're told.", "Mara"),
            ("That's two rules.", "Elias"),
            ("You're observant.\nGood start.", "Mara"),
        ]
        self.rules_idx = 0
        self.rules_given = False

        # Restricted lab dialogue
        self.restricted_lines = [
            ("Restricted Laboratory.", "Elias"),
            ("Not part of today's tour.", "Mara"),
            ("What's inside?", "Elias"),
            ("Projects above your clearance level.", "Mara"),
            ("Dangerous projects?", "Elias"),
            ("Expensive projects.", "Mara"),
            ("Come on.\nYour specimen is waiting.", "Mara"),
        ]
        self.restricted_idx = 0
        self.restricted_done = False

        # Greenhouse entrance dialogue
        self.greenhouse_entrance_lines = [
            ("You made good time.", "Mara"),
            ("The greenhouse is at the end of the corridor.", "Elias"),
            ("I saw it.", "Mara"),
            ("This is it.", "Mara"),
        ]
        self.greenhouse_entrance_idx = 0
        self.greenhouse_entrance_done = False
        self.greenhouse_entrance_dialogue_shown = False

        # Post-door-close dialogue
        self.post_door_lines = [
            ("Is this where I work?", "Elias"),
            ("For now.", "Mara"),
            ("So...", "Elias"),
            ("Don't touch anything until I tell you to.", "Mara"),
        ]
        self.post_door_idx = 0
        self.post_door_done = False
        self.post_door_dialogue_shown = False

        # Mara position
        self.mara_x = 650
        self.mara_target_x = 850
        self.mara_animating = False

    @property
    def active(self):
        return self.phase != 'enter_greenhouse'

    def draw(self, screen):
        """Draw the corridor scene with fade overlay."""
        if self.phase == 'enter_greenhouse':
            return

        # Background
        if self.corridor_img:
            bg_scaled, bx, by = scale_image_keep_ratio(self.corridor_img, 1024, 768)
            screen.blit(bg_scaled, (bx, by))
        else:
            screen.fill(COLORS['dark_gray'])
            pygame.draw.rect(screen, COLORS['dark_gray'],
                             (0, 150, 1024, 400))
            for x in [200, 400, 600, 800, 1000]:
                light = pygame.Surface((100, 20), pygame.SRCALPHA)
                light.fill((255, 255, 200, 30))
                screen.blit(light, (x - 50, 140))

        pygame.draw.rect(screen, COLORS['dark_gray'], (0, 550, 1024, 218))

        # Doors
        gh_open = (self.phase in ('rules_given', 'greenhouse_open'))
        rooms = [
            (self.restricted_rect, "RESTRICTED LAB", COLORS['red']),
            (self.office_rect, "STAFF OFFICE", COLORS['gray']),
            (self.storage_rect, "STORAGE", COLORS['gray']),
            (self.greenhouse_rect, "GREENHOUSE",
             COLORS['green'] if gh_open else COLORS['red']),
        ]
        for rect, label, color in rooms:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLORS['black'], rect, 3)
            lbl = render_text(self.small_font, label, COLORS['white'])
            screen.blit(lbl, (rect.x + 20, rect.y + 270))
            if color == COLORS['red']:
                ind = render_text(self.small_font, "LOCKED", COLORS['red'])
                screen.blit(ind, (rect.x + 40, rect.y + 50))

        # Mara with fade alpha
        mx = int(self.mara_x)
        if self.mara_img:
            mara_scaled, mfx, mfy = scale_image_keep_ratio(self.mara_img, 700, 700)
            if self.mara_alpha < 255:
                mara_scaled.set_alpha(self.mara_alpha)
            screen.blit(mara_scaled, (mx, mfy))
        else:
            mara_surf = pygame.Surface((100, 200), pygame.SRCALPHA)
            pygame.draw.circle(mara_surf, COLORS['blue'], (50, 100), 40)
            pygame.draw.circle(mara_surf, COLORS['white'], (50, 100), 40, 2)
            if self.mara_alpha < 255:
                mara_surf.set_alpha(self.mara_alpha)
            screen.blit(mara_surf, (mx, 300))
        mara_lbl = render_text(make_font(14), "Mara", COLORS['white'])
        screen.blit(mara_lbl, (mx + 200, 600))

        # Greenhouse glow
        if gh_open:
            glow = pygame.Surface((200, 300), pygame.SRCALPHA)
            pulse = 80 + 40 * (pygame.time.get_ticks() % 100) // 100
            glow.fill((0, 128, 0, pulse // 3))
            screen.blit(glow, (self.greenhouse_rect.x - 20,
                               self.greenhouse_rect.y - 20))

        # Hint
        hint = render_text(make_font(20),
                           "Follow Mara to the greenhouse", COLORS['white'])
        screen.blit(hint, (20, 720))

        # Fade overlay
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
            fade_surf.fill((0, 0, 0, self.fade_alpha))
            screen.blit(fade_surf, (0, 0))

    def update(self, events: list):
        """Handle corridor interactions with visual novel flow."""
        # Update fade: 255 → 0
        if self.fade_active:
            self.fade_elapsed += 1
            progress = self.fade_elapsed / self.fade_duration
            self.fade_alpha = int(255 * (1 - progress))
            if self.fade_elapsed >= self.fade_duration:
                self.fade_alpha = 0
                self.fade_active = False
                self.mara_fade_active = True
                self.mara_alpha_elapsed = 0

        if self.mara_fade_active:
            self.mara_alpha_elapsed += 1
            progress = self.mara_alpha_elapsed / self.mara_alpha_duration
            self.mara_alpha = int(self.mara_alpha_target * progress)
            if self.mara_alpha_elapsed >= self.mara_alpha_duration:
                self.mara_alpha = 255
                self.mara_fade_active = False
                self._start_dialogue()

        # Animate Mara
        if self.mara_animating:
            self.mara_x += (self.mara_target_x - self.mara_x) * 0.05
            if abs(self.mara_x - self.mara_target_x) < 1:
                self.mara_animating = False
                self.mara_x = self.mara_target_x

        # Process clicks
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if not self.fade_active and not self.mara_fade_active:
                    pass
                else:
                    continue

                # Dialogue playing: click to advance
                if self.dialogue_playing:
                    self._advance_dialogue()
                    return

                # Corridor intro
                if self.phase == 'corridor_play' and not self.corridor_done:
                    if self.corridor_idx < len(self.corridor_lines):
                        text, speaker = self.corridor_lines[self.corridor_idx]
                        self.corridor_idx += 1
                        self.game.dialogue.show_dialogue(text, speaker)
                        return
                    else:
                        self.corridor_done = True
                        self.phase = 'player_control'
                        return

                # Restricted Lab
                if (self.restricted_rect.collidepoint(pos) and
                        not self.restricted_done):
                    self.restricted_done = True
                    text, speaker = self.restricted_lines[self.restricted_idx]
                    self.game.dialogue.show_dialogue(text, speaker)
                    if self.restricted_idx < len(self.restricted_lines) - 1:
                        self.restricted_idx += 1
                    return

                # Staff Office
                elif (self.office_rect.collidepoint(pos) and
                        not self.office_clicked):
                    self.office_clicked = True
                    self.game.dialogue.show_dialogue(
                        "Staff Office. Mara's workspace.\nClosed for now.",
                        "Elias")

                # Storage
                elif (self.storage_rect.collidepoint(pos) and
                        not self.storage_clicked):
                    self.storage_clicked = True
                    self.game.dialogue.show_dialogue(
                        "Storage room. Contains general supplies.",
                        "Elias")

                # Greenhouse
                elif self.greenhouse_rect.collidepoint(pos):
                    if self.phase in ('rules_given', 'greenhouse_open'):
                        if not self.greenhouse_entrance_done:
                            self._greenhouse_entrance()
                        elif not self.post_door_dialogue_shown:
                            self._post_door_close()
                        else:
                            self._enter_greenhouse()
                    elif not self.rules_done:
                        self._give_rules()

                # Mara
                elif (self.mara_rect.collidepoint(pos) or
                      pygame.Rect(int(self.mara_x), 300, 100,
                                  200).collidepoint(pos)):
                    if self.phase not in ('rules_given', 'greenhouse_open'):
                        self._give_rules()

    def _start_dialogue(self):
        """Start dialogue sequence."""
        self.phase = 'corridor_play'
        self.dialogue_lines = self.corridor_lines[:]
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self._show_next_line()

    def _show_next_line(self):
        """Show next line."""
        if self.dialogue_idx < len(self.dialogue_lines):
            text, speaker = self.dialogue_lines[self.dialogue_idx]
            self.game.dialogue.show_dialogue(text, speaker)

    def _advance_dialogue(self):
        """Advance dialogue."""
        if self.dialogue_idx < len(self.dialogue_lines):
            self.dialogue_idx += 1
            if self.dialogue_idx < len(self.dialogue_lines):
                text, speaker = self.dialogue_lines[self.dialogue_idx]
                self.game.dialogue.show_dialogue(text, speaker)
            else:
                self.dialogue_playing = False
                self.dialogue_lines = []
                if self.phase == 'corridor_play':
                    self.corridor_done = True
                    self.phase = 'player_control'
                elif self.phase == 'greenhouse_entrance':
                    self.greenhouse_entrance_done = True
                    self.phase = 'greenhouse_open'
                elif self.phase == 'post_door_close':
                    self.post_door_dialogue_shown = True
                    self._enter_greenhouse()
        else:
            self.dialogue_playing = False
            self.dialogue_lines = []
            if self.phase == 'corridor_play':
                self.corridor_done = True
                self.phase = 'player_control'
            elif self.phase == 'greenhouse_entrance':
                self.greenhouse_entrance_done = True
                self.phase = 'greenhouse_open'
            elif self.phase == 'post_door_close':
                self.post_door_dialogue_shown = True
                self._enter_greenhouse()

    def _greenhouse_entrance(self):
        """Show greenhouse entrance dialogue sequence."""
        if self.greenhouse_entrance_dialogue_shown:
            self.phase = 'greenhouse_open'
            return
        self.greenhouse_entrance_dialogue_shown = True
        self.phase = 'greenhouse_entrance'
        self.dialogue_lines = self.greenhouse_entrance_lines[:]
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self._show_next_greenhouse_entrance_line()

    def _show_next_greenhouse_entrance_line(self):
        """Show next greenhouse entrance line."""
        if self.dialogue_idx < len(self.dialogue_lines):
            text, speaker = self.dialogue_lines[self.dialogue_idx]
            self.game.dialogue.show_dialogue(text, speaker)

    def _advance_greenhouse_entrance_dialogue(self):
        """Advance greenhouse entrance dialogue."""
        if self.dialogue_idx < len(self.dialogue_lines):
            self.dialogue_idx += 1
            if self.dialogue_idx < len(self.dialogue_lines):
                text, speaker = self.dialogue_lines[self.dialogue_idx]
                self.game.dialogue.show_dialogue(text, speaker)
            else:
                self.dialogue_playing = False
                self.dialogue_lines = []
                self.greenhouse_entrance_done = True
                self.phase = 'greenhouse_open'
        else:
            self.dialogue_playing = False
            self.dialogue_lines = []
            self.greenhouse_entrance_done = True
            self.phase = 'greenhouse_open'

    def _post_door_close(self):
        """Show dialogue after greenhouse door closes."""
        self.dialogue_lines = self.post_door_lines[:]
        self.dialogue_idx = 0
        self.dialogue_playing = True
        self.phase = 'post_door_close'
        self._show_next_post_door_line()

    def _show_next_post_door_line(self):
        """Show next post-door line."""
        if self.dialogue_idx < len(self.dialogue_lines):
            text, speaker = self.dialogue_lines[self.dialogue_idx]
            self.game.dialogue.show_dialogue(text, speaker)

    def _advance_post_door_dialogue(self):
        """Advance post-door dialogue."""
        if self.dialogue_idx < len(self.dialogue_lines):
            self.dialogue_idx += 1
            if self.dialogue_idx < len(self.dialogue_lines):
                text, speaker = self.dialogue_lines[self.dialogue_idx]
                self.game.dialogue.show_dialogue(text, speaker)
            else:
                self.dialogue_playing = False
                self.dialogue_lines = []
                self._enter_greenhouse()
        else:
            self.dialogue_playing = False
            self.dialogue_lines = []
            self._enter_greenhouse()

    def _give_rules(self):
        """Mara gives rules. Matches screenplay SEQ 02."""
        self.phase = 'rules_given'
        self.game.journal.add_objective('obj_greenhouse',
                                        'Follow Mara to Greenhouse',
                                        'Meet Mara at the greenhouse entrance')
        if not self.rules_given:
            self.dialogue_lines = self.rules_lines[:]
            self.dialogue_idx = 0
            self.dialogue_playing = True
            self._show_next_line()
            self.rules_given = True
        else:
            self.phase = 'greenhouse_open'
            self.game.dialogue.show_dialogue("After you.", "Mara")

    def _enter_greenhouse(self):
        """Transition to Scene 3 (Greenhouse)."""
        self.phase = 'enter_greenhouse'
        self.game.journal.complete_objective('obj_greenhouse')
        from blooming.scenes.chapter2_greenhouse import Chapter2_Greenhouse
        self.game.current_scene = Chapter2_Greenhouse(self.game)
