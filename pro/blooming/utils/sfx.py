"""SFX Manager - loads and plays sound effects from data/sounds/."""

import os
import pygame


class SFXManager:
    """Loads OGG/WAV files from data/sounds/ and plays them with volume control."""

    def __init__(self, sound_dir=None, volume=0.7):
        self.sounds = {}
        self.volume = volume
        self.enabled = False
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
        except pygame.error:
            return
        self.enabled = True
        if sound_dir is None:
            sound_dir = os.path.join(
                os.path.dirname(__file__), '..', 'data', 'sounds'
            )
        self.sound_dir = os.path.abspath(sound_dir)
        self._load_all()

    def _load_all(self):
        """Load all .ogg and .wav files from the sound directory."""
        if not os.path.isdir(self.sound_dir):
            return
        for name in os.listdir(self.sound_dir):
            if not (name.endswith('.ogg') or name.endswith('.wav')):
                continue
            key = os.path.splitext(name)[0]
            path = os.path.join(self.sound_dir, name)
            try:
                self.sounds[key] = pygame.mixer.Sound(path)
            except pygame.error:
                self.sounds[key] = None

    def set_volume(self, vol):
        """Set default volume for all sounds (0.0 - 1.0)."""
        self.volume = max(0.0, min(1.0, vol))

    def play(self, name):
        """Play a sound by filename stem (no extension).

        E.g. play('birds') loads birds.ogg or birds.wav.
        Returns the channel if played, else None.
        """
        if not self.enabled:
            return None
        sound = self.sounds.get(name)
        if sound is None:
            return None
        try:
            ch = sound.play()
            if ch:
                ch.set_volume(self.volume)
            return ch
        except pygame.error:
            return None

    def preload(self, names):
        """Ensure sounds are loaded (no-op here since all load at init)."""
        pass
