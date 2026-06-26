import random
from config import WORD_SPEEDS, WORD_SPAWN_INTERVAL_BASE, WORD_SPAWN_INTERVAL_MIN
from word_gen import BOSS_SPEED_MULT


class DifficultyManager:
    LEVEL_UP_INTERVAL = 15.0
    INTERVAL_DELTA = 0.15

    def __init__(self):
        self.level = 0
        self.timer = 0.0
        self._word_interval = WORD_SPAWN_INTERVAL_BASE

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.LEVEL_UP_INTERVAL:
            self.timer = 0.0
            self.level += 1
            self._word_interval = max(
                WORD_SPAWN_INTERVAL_MIN,
                self._word_interval - self.INTERVAL_DELTA,
            )
            return True
        return False

    def word_spawn_interval(self):
        return self._word_interval

    def word_speed_range(self):
        if self.level < 2:
            return WORD_SPEEDS["easy"]
        elif self.level < 4:
            return WORD_SPEEDS["medium"]
        elif self.level < 6:
            lo = WORD_SPEEDS["medium"][0]
            hi = WORD_SPEEDS["hard"][1]
            return (lo, hi)
        else:
            return WORD_SPEEDS["hard"]

    def pick_word_speed(self):
        lo, hi = self.word_speed_range()
        return random.uniform(lo, hi)

    def pick_boss_speed(self):
        if self.level < 2:
            base = 0.7
        elif self.level < 4:
            base = 1.1
        elif self.level < 6:
            base = 1.4
        else:
            base = 1.7
        return base * BOSS_SPEED_MULT

    def word_pool_key(self):
        if self.level < 2:
            return "easy"
        elif self.level < 4:
            return "medium_easy"
        elif self.level < 6:
            return "hard_medium"
        else:
            return "hard"

    def reset(self):
        self.level = 0
        self.timer = 0.0
        self._word_interval = WORD_SPAWN_INTERVAL_BASE
