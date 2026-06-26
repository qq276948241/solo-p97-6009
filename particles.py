import random
import math
import pygame


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(80, 300)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.3, 1.0)
        self.max_life = self.life
        self.size = random.uniform(2, 5)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt
        self.vx *= 0.98
        self.life -= dt

    def is_dead(self):
        return self.life <= 0

    def draw(self, surface):
        alpha = max(0, self.life / self.max_life)
        size = max(1, int(self.size * alpha))
        r = min(255, int(self.color[0] * alpha + 255 * (1 - alpha)))
        g = min(255, int(self.color[1] * alpha))
        b = min(255, int(self.color[2] * alpha))
        pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), size)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=20):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def emit_nuke(self, screen_width, screen_height):
        for _ in range(150):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            color = random.choice([(255, 100, 40), (255, 200, 40), (255, 60, 20)])
            self.particles.append(Particle(x, y, color))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if not p.is_dead()]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
