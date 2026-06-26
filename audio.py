import pygame
import os
import math
import random
from config import ASSETS_DIR


def _generate_beep(frequency=440, duration_ms=80, volume=0.3):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n_samples * 2)
    for i in range(n_samples):
        t = i / sample_rate
        val = int(volume * 32767 * math.sin(2 * math.pi * frequency * t))
        fade = 1.0 - (i / n_samples)
        val = int(val * fade)
        val = max(-32767, min(32767, val))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    sound = pygame.mixer.Sound(buffer=bytes(buf))
    return sound


def _generate_explosion_sound(duration_ms=200, volume=0.2):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n_samples * 2)
    for i in range(n_samples):
        t = i / sample_rate
        fade = 1.0 - (i / n_samples)
        val = int(volume * 32767 * fade * random.uniform(-1, 1))
        val = max(-32767, min(32767, val))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    sound = pygame.mixer.Sound(buffer=bytes(buf))
    return sound


def _generate_powerup_sound(duration_ms=150, volume=0.25):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n_samples * 2)
    for i in range(n_samples):
        t = i / sample_rate
        freq = 600 + 400 * (i / n_samples)
        fade = 1.0 - (i / n_samples)
        val = int(volume * 32767 * fade * math.sin(2 * math.pi * freq * t))
        val = max(-32767, min(32767, val))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    sound = pygame.mixer.Sound(buffer=bytes(buf))
    return sound


def _generate_miss_sound(duration_ms=100, volume=0.15):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n_samples * 2)
    for i in range(n_samples):
        t = i / sample_rate
        freq = 200 - 100 * (i / n_samples)
        fade = 1.0 - (i / n_samples)
        val = int(volume * 32767 * fade * math.sin(2 * math.pi * freq * t))
        val = max(-32767, min(32767, val))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    sound = pygame.mixer.Sound(buffer=bytes(buf))
    return sound


def _generate_bgm():
    sample_rate = 44100
    duration = 16
    n_samples = sample_rate * duration
    buf = bytearray(n_samples * 2)
    melody = [261, 293, 329, 349, 392, 349, 329, 293,
              261, 293, 329, 349, 392, 440, 392, 349]
    note_len = sample_rate * duration // len(melody)
    for i in range(n_samples):
        note_idx = i // note_len
        if note_idx >= len(melody):
            note_idx = len(melody) - 1
        freq = melody[note_idx]
        t = i / sample_rate
        val = int(0.06 * 32767 * math.sin(2 * math.pi * freq * t))
        val += int(0.02 * 32767 * math.sin(2 * math.pi * freq * 2 * t))
        val = max(-32767, min(32767, val))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    sound = pygame.mixer.Sound(buffer=bytes(buf))
    return sound


class AudioManager:
    def __init__(self):
        self.bgm_on = True
        self.sfx_on = True
        self._bgm = None
        self._sfx_hit = None
        self._sfx_destroy = None
        self._sfx_miss = None
        self._sfx_powerup = None
        self._bgm_channel = None
        self._initialized = False

    def init_sounds(self):
        if self._initialized:
            return
        try:
            self._bgm = _generate_bgm()
            self._sfx_hit = _generate_beep(520, 60, 0.15)
            self._sfx_destroy = _generate_explosion_sound(250, 0.2)
            self._sfx_miss = _generate_miss_sound(100, 0.1)
            self._sfx_powerup = _generate_powerup_sound(180, 0.2)
            self._initialized = True
        except Exception:
            self._initialized = False

    def play_bgm(self):
        if not self.bgm_on or not self._initialized or not self._bgm:
            return
        self._bgm_channel = self._bgm.play(loops=-1)

    def stop_bgm(self):
        if self._bgm_channel:
            self._bgm.stop()

    def play_hit(self):
        if not self.sfx_on or not self._initialized:
            return
        if self._sfx_hit:
            self._sfx_hit.play()

    def play_destroy(self):
        if not self.sfx_on or not self._initialized:
            return
        if self._sfx_destroy:
            self._sfx_destroy.play()

    def play_miss(self):
        if not self.sfx_on or not self._initialized:
            return
        if self._sfx_miss:
            self._sfx_miss.play()

    def play_powerup(self):
        if not self.sfx_on or not self._initialized:
            return
        if self._sfx_powerup:
            self._sfx_powerup.play()

    def toggle_bgm(self):
        self.bgm_on = not self.bgm_on
        if self.bgm_on:
            self.play_bgm()
        else:
            self.stop_bgm()

    def toggle_sfx(self):
        self.sfx_on = not self.sfx_on
