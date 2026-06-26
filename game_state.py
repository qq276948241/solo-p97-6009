import enum


class GameStateType(enum.Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    SETTINGS = "settings"
    LEADERBOARD = "leaderboard"


class GameStateManager:
    def __init__(self):
        self.current = GameStateType.MENU
        self.menu_selected = 0
        self.settings_selected = 0
        self.menu_options = ["START", "SETTINGS", "LEADERBOARD"]
        self.settings_options = ["BGM", "SFX", "BACK"]

    def go_to(self, state):
        self.current = state

    def handle_event(self, event):
        import pygame
        if self.current == GameStateType.MENU:
            return self._handle_menu(event)
        elif self.current == GameStateType.SETTINGS:
            return self._handle_settings(event)
        elif self.current == GameStateType.LEADERBOARD:
            return self._handle_leaderboard(event)
        return None

    def _handle_menu(self, event):
        import pygame
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                return self.menu_options[self.menu_selected]
        return None

    def _handle_settings(self, event):
        import pygame
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.settings_selected = (self.settings_selected - 1) % len(self.settings_options)
            elif event.key == pygame.K_DOWN:
                self.settings_selected = (self.settings_selected + 1) % len(self.settings_options)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                if self.settings_selected == 0:
                    return "toggle_bgm"
                elif self.settings_selected == 1:
                    return "toggle_sfx"
            elif event.key == pygame.K_RETURN:
                opt = self.settings_options[self.settings_selected]
                if opt == "BACK":
                    return "BACK"
                elif opt == "BGM":
                    return "toggle_bgm"
                elif opt == "SFX":
                    return "toggle_sfx"
            elif event.key == pygame.K_ESCAPE:
                return "BACK"
        return None

    def _handle_leaderboard(self, event):
        import pygame
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return "BACK"
        return None
