import random
import enum
import math
import pygame
from config import (
    SCREEN_WIDTH, POWERUP_SPAWN_INTERVAL, POWERUP_DURATION,
    ORANGE, PURPLE, GREEN, WHITE,
)


class PowerUpType(enum.Enum):
    SLOW = "slow"
    NUKE = "nuke"
    LIFE = "life"


POWERUP_COLORS = {
    PowerUpType.SLOW: (80, 220, 220),
    PowerUpType.NUKE: (255, 100, 40),
    PowerUpType.LIFE: (220, 40, 60),
}

POWERUP_LABELS = {
    PowerUpType.SLOW: "SLOW",
    PowerUpType.NUKE: "NUKE",
    PowerUpType.LIFE: "+1 UP",
}


class PowerUp:
    def __init__(self, x, ptype):
        self.x = x
        self.y = 0.0
        self.ptype = ptype
        self.speed = 0.8
        self.alive = True
        self.collected = False
        self.pulse = 0.0

    def update(self, dt):
        self.y += self.speed * dt * 60
        self.pulse += dt * 4.0
        if self.y >= 670:
            self.alive = False

    def draw(self, surface, font_small):
        scale = 1.0 + 0.15 * math.sin(self.pulse)
        size = int(28 * scale)
        color = POWERUP_COLORS.get(self.ptype, (255, 255, 255))
        rect = pygame.Rect(self.x - size, int(self.y) - size, size * 2, size * 2)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=8)
        label = font_small.render("?", True, (0, 0, 0))
        lx = self.x - label.get_width() // 2
        ly = int(self.y) - label.get_height() // 2
        surface.blit(label, (lx, ly))


class PowerUpSpawner:
    def __init__(self):
        self.timer = 0.0
        self.interval = POWERUP_SPAWN_INTERVAL
        self.active_powerups = []
        self.active_effects = {}

    def update(self, dt):
        self.timer += dt

        expired = []
        for key in self.active_effects:
            self.active_effects[key] -= dt
            if self.active_effects[key] <= 0:
                expired.append(key)
        for key in expired:
            del self.active_effects[key]

        for p in self.active_powerups:
            p.update(dt)
        self.active_powerups = [p for p in self.active_powerups if p.alive]

        if self.timer >= self.interval:
            self.timer = 0.0
            ptype = random.choice(list(PowerUpType))
            x = random.randint(80, SCREEN_WIDTH - 80)
            self.active_powerups.append(PowerUp(x, ptype))

    def try_collect(self, player):
        for p in self.active_powerups:
            if p.alive and not p.collected and p.y >= 600:
                p.collected = True
                p.alive = False
                self._activate(p.ptype, player)
                return p.ptype
        return None

    def _activate(self, ptype, player):
        from config import POWERUP_DURATION
        if ptype == PowerUpType.SLOW:
            self.active_effects[PowerUpType.SLOW] = POWERUP_DURATION["slow"]
        elif ptype == PowerUpType.NUKE:
            self.active_effects[PowerUpType.NUKE] = POWERUP_DURATION["nuke"]
        elif ptype == PowerUpType.LIFE:
            player.add_life()

    def has_effect(self, ptype):
        return ptype in self.active_effects

    def slow_factor(self):
        if self.has_effect(PowerUpType.SLOW):
            return 0.4
        return 1.0

    def draw(self, surface, font_small):
        for p in self.active_powerups:
            if p.alive:
                p.draw(surface, font_small)
