from config import INITIAL_LIVES, MAX_LIVES, BASE_SCORE, COMBO_MULTIPLIER_STEP, COMBO_THRESHOLD


class PlayerState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.lives = INITIAL_LIVES
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.words_destroyed = 0
        self.words_missed = 0
        self.miss_streak = 0

    @property
    def multiplier(self):
        tier = self.combo // COMBO_THRESHOLD
        return 1.0 + tier * COMBO_MULTIPLIER_STEP

    @property
    def accuracy(self):
        if self.total_keystrokes == 0:
            return 100.0
        return (self.correct_keystrokes / self.total_keystrokes) * 100.0

    def add_hit(self):
        self.combo += 1
        self.correct_keystrokes += 1
        self.total_keystrokes += 1
        self.miss_streak = 0
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        earned = int(BASE_SCORE * self.multiplier)
        self.score += earned
        self.words_destroyed += 1

    def add_miss(self):
        self.combo = 0
        self.miss_streak += 1
        self.total_keystrokes += 1

    def lose_life(self):
        self.lives -= 1
        self.combo = 0
        self.words_missed += 1
        if self.lives < 0:
            self.lives = 0

    def add_life(self):
        if self.lives < MAX_LIVES:
            self.lives += 1

    def is_dead(self):
        return self.lives <= 0

    def add_keystroke(self, correct):
        self.total_keystrokes += 1
        if correct:
            self.correct_keystrokes += 1
