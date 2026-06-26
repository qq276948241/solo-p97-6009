import pygame
import math
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
    DARK_BG, WHITE, GRAY, HEART_RED, GREEN, CYAN, YELLOW, ORANGE, DARK_GRAY,
)
from powerup import PowerUpType


def draw_heart(surface, x, y, size, color):
    points = []
    for i in range(360):
        t = math.radians(i)
        hx = 16 * math.sin(t) ** 3
        hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        points.append((x + hx * size / 17, y + hy * size / 17))
    if len(points) >= 3:
        pygame.draw.polygon(surface, color, points)


def draw_hud(surface, player, fonts, powerup_spawner=None):
    font_small = fonts["small"]
    font_medium = fonts["medium"]

    score_text = font_medium.render(f"SCORE: {player.score}", True, WHITE)
    surface.blit(score_text, (20, 10))

    combo_text = font_medium.render(f"COMBO: {player.combo}", True, YELLOW if player.combo >= 5 else WHITE)
    surface.blit(combo_text, (SCREEN_WIDTH // 2 - combo_text.get_width() // 2, 10))

    if player.multiplier > 1.0:
        mult_text = font_small.render(f"x{player.multiplier:.1f}", True, ORANGE)
        surface.blit(mult_text, (SCREEN_WIDTH // 2 + combo_text.get_width() // 2 + 10, 18))

    for i in range(player.lives):
        draw_heart(surface, SCREEN_WIDTH - 50 - i * 45, 30, 16, HEART_RED)

    if powerup_spawner:
        effects = []
        if powerup_spawner.has_effect(PowerUpType.SLOW):
            remaining = powerup_spawner.active_effects.get(PowerUpType.SLOW, 0)
            effects.append(f"SLOW {remaining:.1f}s")
        if effects:
            eff_surf = font_small.render("  ".join(effects), True, CYAN)
            surface.blit(eff_surf, (20, 50))


def draw_bottom_bar(surface, input_handler, fonts):
    font = fonts["small"]
    bar_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
    pygame.draw.rect(surface, (25, 25, 40), bar_rect)
    pygame.draw.line(surface, GRAY, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 1)
    input_handler.draw_input(surface, font, 20, SCREEN_HEIGHT - 40)


def draw_menu(surface, fonts, selected):
    font_large = fonts["large"]
    font_medium = fonts["medium"]

    title = font_large.render("KEYBOARD FIGHTER", True, CYAN)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

    subtitle = fonts["small"].render("-- Type to Destroy --", True, GRAY)
    surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))

    options = ["START", "SETTINGS", "LEADERBOARD"]
    for i, opt in enumerate(options):
        color = YELLOW if i == selected else WHITE
        text = font_medium.render(opt, True, color)
        y = 300 + i * 70
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))

    hint = fonts["small"].render("UP/DOWN to select, ENTER to confirm", True, GRAY)
    surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60))


def draw_settings(surface, fonts, bgm_on, sfx_on, selected):
    font_medium = fonts["medium"]
    font_small = fonts["small"]

    title = font_medium.render("SETTINGS", True, WHITE)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

    bgm_label = f"BGM: {'ON' if bgm_on else 'OFF'}"
    sfx_label = f"SFX: {'ON' if sfx_on else 'OFF'}"

    items = [bgm_label, sfx_label, "BACK"]
    for i, item in enumerate(items):
        color = YELLOW if i == selected else WHITE
        text = font_medium.render(item, True, color)
        y = 250 + i * 70
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))

    hint = font_small.render("LEFT/RIGHT to toggle, ENTER to confirm", True, GRAY)
    surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60))


def draw_leaderboard(surface, fonts, scores):
    font_medium = fonts["medium"]
    font_small = fonts["small"]

    title = font_medium.render("LEADERBOARD", True, WHITE)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

    if not scores:
        no_data = font_small.render("No scores yet. Play a game!", True, GRAY)
        surface.blit(no_data, (SCREEN_WIDTH // 2 - no_data.get_width() // 2, 200))
    else:
        header = font_small.render("RANK   SCORE   ACC%   COMBO   DATE", True, GRAY)
        surface.blit(header, (SCREEN_WIDTH // 2 - header.get_width() // 2, 130))
        for i, s in enumerate(scores[:10]):
            line = f" {i+1:2d}.    {s['score']:5d}   {s['accuracy']:5.1f}   {s['max_combo']:3d}     {s['date']}"
            color = YELLOW if i == 0 else WHITE
            text = font_small.render(line, True, color)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 170 + i * 36))

    hint = font_small.render("Press ESC or ENTER to go back", True, GRAY)
    surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60))


def draw_game_over(surface, fonts, player):
    font_large = fonts["large"]
    font_medium = fonts["medium"]
    font_small = fonts["small"]

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    go_text = font_large.render("GAME OVER", True, (230, 60, 60))
    surface.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, 140))

    score_text = font_medium.render(f"Score: {player.score}", True, WHITE)
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 260))

    acc_text = font_medium.render(f"Accuracy: {player.accuracy:.1f}%", True, WHITE)
    surface.blit(acc_text, (SCREEN_WIDTH // 2 - acc_text.get_width() // 2, 320))

    combo_text = font_medium.render(f"Max Combo: {player.max_combo}", True, YELLOW)
    surface.blit(combo_text, (SCREEN_WIDTH // 2 - combo_text.get_width() // 2, 380))

    hint1 = font_small.render("[R] Restart    [Q] Main Menu", True, GRAY)
    surface.blit(hint1, (SCREEN_WIDTH // 2 - hint1.get_width() // 2, 480))
