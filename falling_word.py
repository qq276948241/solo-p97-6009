import pygame
import math
from config import FONT_SIZE_WORD, FONT_NAME, SCREEN_HEIGHT


class BaseFallingWord:
    def __init__(self, text, x, color, speed):
        self.text = text
        self.x = x
        self.y = 0.0
        self.color = color
        self.speed = speed
        self.typed_index = 0
        self.alive = True
        self.highlight_color = (255, 255, 255)
        self.is_boss = False
        self._destroy_tag = "destroyed"
        self._miss_tag = "miss"

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
                    return self._destroy_tag
                return "hit"
            else:
                return self._miss_tag
        return self._miss_tag

    def get_typed_text(self):
        return self.text[:self.typed_index]

    def get_remaining_text(self):
        return self.text[self.typed_index:]

    def _pick_font(self, base_font):
        return base_font

    def _effective_color(self):
        return self.color

    def _render_text(self, typed_surf, remaining_surf, surface, draw_x, draw_y):
        surface.blit(typed_surf, (draw_x, draw_y))
        surface.blit(remaining_surf, (draw_x + typed_surf.get_width(), draw_y))

    def _draw_decorations(self, surface, draw_x, draw_y, total_width, font_height):
        pass

    def draw(self, surface, base_font):
        font = self._pick_font(base_font)
        typed = self.get_typed_text()
        remaining = self.get_remaining_text()
        display_color = self._effective_color()

        typed_surf = font.render(typed, True, self.highlight_color)
        remaining_surf = font.render(remaining, True, display_color)

        total_width = typed_surf.get_width() + remaining_surf.get_width()
        draw_x = self.x - total_width // 2
        draw_y = int(self.y)

        self._draw_decorations(surface, draw_x, draw_y, total_width, font.get_height())
        self._render_text(typed_surf, remaining_surf, surface, draw_x, draw_y)


class FallingWord(BaseFallingWord):
    def __init__(self, text, x, color, speed):
        super().__init__(text, x, color, speed)


class BossWord(BaseFallingWord):
    def __init__(self, text, x, color, speed):
        super().__init__(text, x, color, speed)
        self.is_boss = True
        self.hit_count = 0
        self.flash_timer = 0.0
        self.pulse_timer = 0.0
        self._destroy_tag = "destroyed_boss"
        self._miss_tag = "miss_boss"

    def try_char(self, ch):
        if self.typed_index < len(self.text):
            if self.text[self.typed_index] == ch:
                self.typed_index += 1
                self.hit_count = self.typed_index
                if self.typed_index >= len(self.text):
                    self.alive = False
                    return self._destroy_tag
                return "hit"
            else:
                self.typed_index = 0
                self.hit_count = 0
                self.flash_timer = 0.15
                return self._miss_tag
        return self._miss_tag

    def update(self, dt, slow_factor=1.0):
        super().update(dt, slow_factor)
        if self.flash_timer > 0:
            self.flash_timer -= dt
        self.pulse_timer += dt * 3.0

    def _pick_font(self, base_font):
        large_size = FONT_SIZE_WORD + 6
        return pygame.font.Font(FONT_NAME, large_size)

    def _effective_color(self):
        if self.flash_timer > 0:
            return (255, 100, 100)
        return self.color

    def _draw_decorations(self, surface, draw_x, draw_y, total_width, font_height):
        box_x = draw_x - 10
        box_y = draw_y - 8
        box_w = total_width + 20
        box_h = font_height + 16

        glow = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        glow.fill((160, 60, 220, 60))
        surface.blit(glow, (box_x, box_y))

        pygame.draw.rect(
            surface, (160, 60, 220),
            pygame.Rect(box_x, box_y, box_w, box_h),
            width=2, border_radius=6,
        )

        total = len(self.text)
        if total > 0:
            ratio = self.typed_index / total
            bar_y = draw_y - 14
            pygame.draw.rect(
                surface, (60, 60, 80),
                pygame.Rect(draw_x, bar_y, total_width, 4),
            )
            pygame.draw.rect(
                surface, self.color,
                pygame.Rect(draw_x, bar_y, int(total_width * ratio), 4),
            )
