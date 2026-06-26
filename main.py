import pygame
import sys
import math

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, DARK_BG, WHITE,
    FONT_NAME, FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, FONT_SIZE_WORD,
)
from game_state import GameStateType, GameStateManager
from word_gen import WordSpawner, BossSpawner, BOSS_BASE_SCORE, BOSS_MISS_LIVES
from player import PlayerState
from powerup import PowerUpSpawner, PowerUpType
from particles import ParticleSystem
from input_handler import InputHandler
from scoreboard import load_scores, save_score
from audio import AudioManager
from falling_word import BossWord
import renderer


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Keyboard Fighter - 键盘战机")
        self.clock = pygame.time.Clock()

        self.fonts = {
            "large": pygame.font.Font(FONT_NAME, FONT_SIZE_LARGE),
            "medium": pygame.font.Font(FONT_NAME, FONT_SIZE_MEDIUM),
            "small": pygame.font.Font(FONT_NAME, FONT_SIZE_SMALL),
            "word": pygame.font.Font(FONT_NAME, FONT_SIZE_WORD),
        }

        self.state_mgr = GameStateManager()
        self.player = PlayerState()
        self.spawner = WordSpawner()
        self.boss_spawner = BossSpawner()
        self.powerup_spawner = PowerUpSpawner()
        self.particles = ParticleSystem()
        self.input_handler = InputHandler()
        self.audio = AudioManager()
        self.audio.init_sounds()
        self.boss_effect = renderer.BossEffectManager()

        self.falling_words = []
        self.scores_data = load_scores()
        self.running = True

    def _reset_game(self):
        self.player.reset()
        self.spawner = WordSpawner()
        self.boss_spawner = BossSpawner()
        self.powerup_spawner = PowerUpSpawner()
        self.particles = ParticleSystem()
        self.input_handler.reset()
        self.boss_effect = renderer.BossEffectManager()
        self.falling_words = []

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            self._handle_events()

            if self.state_mgr.current == GameStateType.PLAYING:
                self._update(dt)
            elif self.state_mgr.current == GameStateType.MENU:
                self.audio.stop_bgm()

            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

            if self.state_mgr.current == GameStateType.MENU:
                result = self.state_mgr.handle_event(event)
                if result == "START":
                    self._reset_game()
                    self.state_mgr.go_to(GameStateType.PLAYING)
                    self.audio.play_bgm()
                elif result == "SETTINGS":
                    self.state_mgr.go_to(GameStateType.SETTINGS)
                elif result == "LEADERBOARD":
                    self.scores_data = load_scores()
                    self.state_mgr.go_to(GameStateType.LEADERBOARD)

            elif self.state_mgr.current == GameStateType.SETTINGS:
                result = self.state_mgr.handle_event(event)
                if result == "toggle_bgm":
                    self.audio.toggle_bgm()
                elif result == "toggle_sfx":
                    self.audio.toggle_sfx()
                elif result == "BACK":
                    self.state_mgr.go_to(GameStateType.MENU)

            elif self.state_mgr.current == GameStateType.LEADERBOARD:
                result = self.state_mgr.handle_event(event)
                if result == "BACK":
                    self.state_mgr.go_to(GameStateType.MENU)

            elif self.state_mgr.current == GameStateType.PLAYING:
                if event.key == pygame.K_ESCAPE:
                    self.state_mgr.go_to(GameStateType.MENU)
                    self.audio.stop_bgm()
                    continue

                if event.key == pygame.K_RETURN:
                    ptype = self.powerup_spawner.try_collect(self.player)
                    if ptype:
                        self.audio.play_powerup()
                        if ptype == PowerUpType.NUKE:
                            self._do_nuke()
                    continue

                key_result = self.input_handler.handle_key(
                    event, self.falling_words, self.player
                )
                if key_result:
                    if isinstance(key_result, tuple):
                        tag = key_result[0]
                        word = key_result[1]
                        if tag == "destroyed_boss":
                            reward = int(BOSS_BASE_SCORE * self.player.multiplier)
                            self.player.score += reward
                            self.player.words_destroyed += 1
                            self.player.combo += 1
                            if self.player.combo > self.player.max_combo:
                                self.player.max_combo = self.player.combo
                            self.particles.emit(word.x, int(word.y), word.color, 80)
                            self.boss_effect.trigger_boss_down()
                            self.boss_spawner.clear_active()
                            self.audio.play_boss_kill()
                        elif tag == "destroyed":
                            self.particles.emit(word.x, int(word.y), word.color, 25)
                            self.audio.play_destroy()
                    elif key_result == "hit":
                        self.audio.play_hit()
                    elif key_result == "miss" or key_result == "miss_boss":
                        self.audio.play_miss()

            elif self.state_mgr.current == GameStateType.GAME_OVER:
                if event.key == pygame.K_r:
                    self._reset_game()
                    self.state_mgr.go_to(GameStateType.PLAYING)
                    self.audio.play_bgm()
                elif event.key == pygame.K_q:
                    self.state_mgr.go_to(GameStateType.MENU)

    def _update(self, dt):
        if self.player.is_dead():
            save_score(self.player.score, self.player.accuracy, self.player.max_combo)
            self.state_mgr.go_to(GameStateType.GAME_OVER)
            self.audio.stop_bgm()
            return

        slow = self.powerup_spawner.slow_factor()

        if self.spawner.update(dt):
            word = self.spawner.generate_word(SCREEN_WIDTH)
            self.falling_words.append(word)

        if self.boss_spawner.update(dt):
            boss = self.boss_spawner.generate_boss(
                SCREEN_WIDTH, self.spawner.difficulty_level
            )
            self.falling_words.append(boss)

        self.powerup_spawner.update(dt)
        self.particles.update(dt)
        self.boss_effect.update(dt)

        for w in self.falling_words:
            w.update(dt, slow)

        alive_words = []
        for w in self.falling_words:
            if w.alive:
                if w.is_off_screen():
                    if w.is_boss:
                        for _ in range(BOSS_MISS_LIVES):
                            self.player.lose_life()
                        self.boss_spawner.clear_active()
                    else:
                        self.player.lose_life()
                    self.particles.emit(w.x, int(w.y), (200, 60, 60), 12)
                    self.input_handler.reset()
                else:
                    alive_words.append(w)
        self.falling_words = alive_words

        if self.input_handler.target_word and not self.input_handler.target_word.alive:
            self.input_handler.reset()

    def _do_nuke(self):
        for w in self.falling_words:
            self.particles.emit(w.x, int(w.y), w.color, 15)
            self.player.score += 10
            self.player.words_destroyed += 1
            if w.is_boss:
                self.boss_spawner.clear_active()
        self.falling_words.clear()
        self.input_handler.reset()
        self.particles.emit_nuke(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.audio.play_destroy()

    def _draw(self):
        self.screen.fill(DARK_BG)

        shake_ox, shake_oy = self.boss_effect.get_shake_offset()
        buf = self.screen
        apply_shake = (shake_ox != 0 or shake_oy != 0)
        if apply_shake:
            buf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            buf.fill(DARK_BG)

        if self.state_mgr.current == GameStateType.MENU:
            renderer.draw_menu(buf, self.fonts, self.state_mgr.menu_selected)

        elif self.state_mgr.current == GameStateType.SETTINGS:
            renderer.draw_settings(
                buf, self.fonts,
                self.audio.bgm_on, self.audio.sfx_on,
                self.state_mgr.settings_selected,
            )

        elif self.state_mgr.current == GameStateType.LEADERBOARD:
            renderer.draw_leaderboard(buf, self.fonts, self.scores_data)

        elif self.state_mgr.current == GameStateType.PLAYING:
            for w in self.falling_words:
                w.draw(buf, self.fonts["word"])
            self.powerup_spawner.draw(buf, self.fonts["small"])
            self.particles.draw(buf)
            self.boss_effect.draw(buf, self.fonts)
            renderer.draw_hud(buf, self.player, self.fonts, self.powerup_spawner)
            renderer.draw_bottom_bar(buf, self.input_handler, self.fonts)

        elif self.state_mgr.current == GameStateType.GAME_OVER:
            for w in self.falling_words:
                w.draw(buf, self.fonts["word"])
            renderer.draw_hud(buf, self.player, self.fonts)
            self.boss_effect.draw(buf, self.fonts)
            renderer.draw_game_over(buf, self.fonts, self.player)

        if apply_shake:
            self.screen.blit(buf, (shake_ox, shake_oy))

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
