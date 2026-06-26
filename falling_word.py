import pygame
from config import FONT_SIZE_WORD, FONT_NAME, SCREEN_HEIGHT, DARK_BG


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
