import pygame
from config import FONT_NAME, FONT_SIZE_SMALL, FONT_SIZE_WORD


class InputHandler:
    def __init__(self):
        self.current_input = ""
        self.target_word = None
        self.target_index = -1

    def reset(self):
        self.current_input = ""
        self.target_word = None
        self.target_index = -1

    def handle_key(self, event, falling_words, player):
        if event.key == pygame.K_BACKSPACE:
            if self.current_input:
                self.current_input = self.current_input[:-1]
                if self.target_word and self.target_index >= 0:
                    idx = len(self.current_input)
                    if idx < len(self.target_word.text):
                        self.target_word.typed_index = idx
            return None

        if event.key == pygame.K_RETURN:
            return "enter"

        if not event.unicode or not event.unicode.isalpha():
            return None

        ch = event.unicode.lower()

        if self.target_word is None or not self.target_word.alive:
            self._find_target(ch, falling_words)
            if self.target_word is None:
                player.add_keystroke(False)
                return "miss"

        if self.target_word:
            result = self.target_word.try_char(ch)
            if result == "destroyed":
                player.add_hit()
                destroyed = self.target_word
                self.reset()
                return ("destroyed", destroyed)
            elif result == "destroyed_boss":
                destroyed = self.target_word
                self.reset()
                return ("destroyed_boss", destroyed)
            elif result == "hit":
                player.add_keystroke(True)
                self.current_input += ch
                return "hit"
            elif result == "miss_boss":
                player.add_keystroke(False)
                self.current_input = ""
                return "miss_boss"
            else:
                player.add_keystroke(False)
                return "miss"

        return None

    def _find_target(self, ch, falling_words):
        best = None
        best_y = -1
        for i, w in enumerate(falling_words):
            if w.alive and w.text.startswith(ch) and w.typed_index == 0:
                if w.y > best_y:
                    best_y = w.y
                    best = w
                    self.target_index = i
        if best:
            self.target_word = best
            self.current_input = ch
            best.typed_index = 1
        else:
            self.target_word = None

    def draw_input(self, surface, font, x, y):
        if self.current_input:
            text_surf = font.render(f"> {self.current_input}_", True, (255, 255, 255))
            surface.blit(text_surf, (x, y))
