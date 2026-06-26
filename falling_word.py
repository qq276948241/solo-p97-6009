import pygame
from config import FONT_SIZE_WORD, FONT_NAME, SCREEN_HEIGHT, DARK_BG, PURPLE, WHITE


class FallingWord:
    def __init__(self, text, x, color, speed):
        self.text = text
        self.x = x
        self.y = 0.0
        self.color = color
        self.speed = speed
        self.typed_index = 0
        self.alive = True
        self.highlight_color = (255, 255, 255)
        self._render_cache = {}
        self.is_boss = False

    def update(self, dt, slow_factor=1.0):
        self.y += self.speed * dt * 60 * slow_factor

    def is_off_screen(self):
        return self.y >= SCREEN_HEIGHT - 30

    def try_char(self, ch):
        if self.typed_index < len(self.text):
            if self.text[self.typed_index] == ch:
                self.typed_index += 1
                if self.typed_index >= len(self.text):
                    self.alive = False
                    return "destroyed"
                return "hit"
            else:
                return "miss"
        return "miss"

    def get_typed_text(self):
        return self.text[:self.typed_index]

    def get_remaining_text(self):
        return self.text[self.typed_index:]

    def draw(self, surface, font):
        typed = self.get_typed_text()
        remaining = self.get_remaining_text()

        typed_surf = font.render(typed, True, self.highlight_color)
        remaining_surf = font.render(remaining, True, self.color)

        total_width = typed_surf.get_width() + remaining_surf.get_width()
        draw_x = self.x - total_width // 2
        draw_y = int(self.y)

        surface.blit(typed_surf, (draw_x, draw_y))
        surface.blit(remaining_surf, (draw_x + typed_surf.get_width(), draw_y))


class BossWord(FallingWord):
    def __init__(self, text, x, color, speed):
        super().__init__(text, x, color, speed)
        self.is_boss = True
        self.hit_count = 0
        self.highlight_color = (255, 255, 255)
        self.flash_timer = 0.0
        self.pulse_timer = 0.0

    def try_char(self, ch):
        if self.typed_index < len(self.text):
            if self.text[self.typed_index] == ch:
                self.typed_index += 1
                self.hit_count = self.typed_index
                if self.typed_index >= len(self.text):
                    self.alive = False
                    return "destroyed_boss"
                return "hit"
            else:
                self.typed_index = 0
                self.hit_count = 0
                self.flash_timer = 0.15
                return "miss_boss"
        return "miss"

    def update(self, dt, slow_factor=1.0):
        super().update(dt, slow_factor)
        if self.flash_timer > 0:
            self.flash_timer -= dt
        self.pulse_timer += dt * 3.0

    def draw(self, surface, font):
        import math
        typed = self.get_typed_text()
        remaining = self.get_remaining_text()

        scale = 1.0 + 0.05 * math.sin(self.pulse_timer)
        large_size = int(FONT_SIZE_WORD + 6)
        boss_font = pygame.font.Font(FONT_NAME, large_size)

        if self.flash_timer > 0:
            display_color = (255, 100, 100)
        else:
            display_color = self.color

        typed_surf = boss_font.render(typed, True, self.highlight_color)
        remaining_surf = boss_font.render(remaining, True, display_color)

        total_width = typed_surf.get_width() + remaining_surf.get_width()
        draw_x = self.x - total_width // 2
        draw_y = int(self.y)

        glow_surf = pygame.Surface((total_width + 20, boss_font.get_height() + 16), pygame.SRCALPHA)
        glow_surf.fill((160, 60, 220, 60))
        surface.blit(glow_surf, (draw_x - 10, draw_y - 8))

        pygame.draw.rect(
            surface,
            (160, 60, 220),
            pygame.Rect(draw_x - 10, draw_y - 8, total_width + 20, boss_font.get_height() + 16),
            width=2, border_radius=6,
        )

        surface.blit(typed_surf, (draw_x, draw_y))
        surface.blit(remaining_surf, (draw_x + typed_surf.get_width(), draw_y))

        total = len(self.text)
        if total > 0:
            ratio = self.typed_index / total
            bar_w = total_width
            bar_y = draw_y - 14
            pygame.draw.rect(
                surface, (60, 60, 80),
                pygame.Rect(draw_x, bar_y, bar_w, 4),
            )
            pygame.draw.rect(
                surface, self.color,
                pygame.Rect(draw_x, bar_y, int(bar_w * ratio), 4),
            )
