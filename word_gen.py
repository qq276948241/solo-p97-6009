import random
import string

WORD_POOL_EASY = [
    "cat", "dog", "run", "fly", "hit", "box", "key", "map", "sun", "top",
    "red", "cup", "fox", "gem", "ink", "jar", "log", "net", "oak", "pen",
    "rug", "sky", "van", "web", "zip", "arm", "bat", "cow", "dip", "egg",
]
WORD_POOL_MEDIUM = [
    "alpha", "brave", "cloud", "dream", "eagle", "flame", "ghost", "haven",
    "ivory", "joker", "karma", "laser", "magic", "nerve", "ocean", "pixel",
    "quest", "radar", "sigma", "torch", "ultra", "vigor", "wrath", "xenon",
    "yield", "zonal", "blaze", "crypt", "drift", "ember",
]
WORD_POOL_HARD = [
    "catalyst", "dynamite", "ecliptic", "fracture", "galactic", "hologram",
    "infinite", "jubilant", "keepsake", "labyrinth", "molecule", "nebulous",
    "obsidian", "paradigm", "quadrant", "resonant", "spectrum", "tangible",
    "umbra", "velocity", "whisper", "zenith", "crucible", "derelict",
    "euphoria", "fortress", "granite", "ignition",
]

ALL_WORDS = WORD_POOL_EASY + WORD_POOL_MEDIUM + WORD_POOL_HARD

BOSS_WORD_POOL = [
    "congratulations", "extraordinary", "magnificent", "unprecedented",
    "spectacular", "revolutionary", "extraordinarily", "magnificently",
    "philosophical", "electromagnetic", "thermodynamics", "neuropsychology",
    "photographically", "paleontologist", "circumstantial", "determination",
    "sophistication", "thunderstorm", "strawberry", "butterflies",
]

BOSS_COLOR = (160, 60, 220)
BOSS_SPAWN_INTERVAL = 60.0
BOSS_SPEED_MULT = 0.6
BOSS_BASE_SCORE = 200
BOSS_MISS_LIVES = 2


def pick_word(pool_key):
    if pool_key == "easy":
        return random.choice(WORD_POOL_EASY)
    elif pool_key == "medium_easy":
        return random.choice(random.choice([WORD_POOL_EASY, WORD_POOL_MEDIUM]))
    elif pool_key == "hard_medium":
        return random.choice(random.choice([WORD_POOL_MEDIUM, WORD_POOL_HARD]))
    else:
        return random.choice(WORD_POOL_HARD)


def pick_color():
    from config import WORD_COLORS
    return random.choice(WORD_COLORS)


def pick_boss_word():
    return random.choice(BOSS_WORD_POOL)


class WordSpawner:
    def __init__(self, difficulty_manager=None):
        self.timer = 0.0
        self.difficulty_manager = difficulty_manager
        self.difficulty_level = getattr(difficulty_manager, "level", 0)

    def bind(self, difficulty_manager):
        self.difficulty_manager = difficulty_manager
        self.difficulty_level = difficulty_manager.level

    def update(self, dt):
        if self.difficulty_manager is None:
            return False
        self.difficulty_level = self.difficulty_manager.level
        self.timer += dt
        interval = self.difficulty_manager.word_spawn_interval()
        if self.timer >= interval:
            self.timer = 0.0
            return True
        return False

    def generate_word(self, screen_width):
        from falling_word import FallingWord
        pool_key = (
            self.difficulty_manager.word_pool_key()
            if self.difficulty_manager else "easy"
        )
        word_text = pick_word(pool_key)
        color = pick_color()
        speed = (
            self.difficulty_manager.pick_word_speed()
            if self.difficulty_manager else 1.0
        )
        x = random.randint(60, screen_width - 120)
        return FallingWord(word_text, x, color, speed)


class BossSpawner:
    def __init__(self, difficulty_manager=None):
        self.timer = 0.0
        self.interval = BOSS_SPAWN_INTERVAL
        self.active_boss = None
        self.difficulty_manager = difficulty_manager

    def bind(self, difficulty_manager):
        self.difficulty_manager = difficulty_manager

    def update(self, dt):
        if self.active_boss is not None:
            return False
        self.timer += dt
        if self.timer >= self.interval:
            self.timer = 0.0
            return True
        return False

    def generate_boss(self, screen_width, difficulty_level=None):
        from falling_word import BossWord
        if difficulty_level is None and self.difficulty_manager:
            difficulty_level = self.difficulty_manager.level
        if difficulty_level is None:
            difficulty_level = 0
        speed = (
            self.difficulty_manager.pick_boss_speed()
            if self.difficulty_manager else 0.5
        )
        word_text = pick_boss_word()
        x = screen_width // 2
        boss = BossWord(word_text, x, BOSS_COLOR, speed)
        self.active_boss = boss
        return boss

    def clear_active(self):
        self.active_boss = None
