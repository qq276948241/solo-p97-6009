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


def pick_word(difficulty_level):
    if difficulty_level < 2:
        pool = WORD_POOL_EASY
    elif difficulty_level < 4:
        pool = random.choice([WORD_POOL_EASY, WORD_POOL_MEDIUM])
    elif difficulty_level < 6:
        pool = random.choice([WORD_POOL_MEDIUM, WORD_POOL_HARD])
    else:
        pool = WORD_POOL_HARD
    return random.choice(pool)


def pick_color():
    from config import WORD_COLORS
    return random.choice(WORD_COLORS)


def pick_speed(difficulty_level):
    from config import WORD_SPEEDS
    if difficulty_level < 2:
        rng = WORD_SPEEDS["easy"]
    elif difficulty_level < 4:
        rng = WORD_SPEEDS["medium"]
    elif difficulty_level < 6:
        lo = WORD_SPEEDS["medium"][0]
        hi = WORD_SPEEDS["hard"][1]
        rng = (lo, hi)
    else:
        rng = WORD_SPEEDS["hard"]
    return random.uniform(rng[0], rng[1])


class WordSpawner:
    def __init__(self):
        self.timer = 0.0
        self.interval = 1.8
        self.difficulty_level = 0
        self.diff_timer = 0.0
        self.active_words = []

    def update(self, dt):
        self.timer += dt
        self.diff_timer += dt

        if self.diff_timer >= 15.0:
            self.diff_timer = 0.0
            self.difficulty_level += 1
            self.interval = max(0.5, self.interval - 0.15)

        if self.timer >= self.interval:
            self.timer = 0.0
            return True
        return False

    def generate_word(self, screen_width):
        from falling_word import FallingWord
        word_text = pick_word(self.difficulty_level)
        color = pick_color()
        speed = pick_speed(self.difficulty_level)
        x = random.randint(60, screen_width - 120)
        return FallingWord(word_text, x, color, speed)
