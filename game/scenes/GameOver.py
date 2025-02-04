import pygame

from scripts.UI import Button
from scripts.SceneManager import SceneManager, static_scene_manager
from scripts.SoundMusic import Music, static_music
from scripts.Settings import Settings, static_settings
from scripts.Text import Text


class GameOver:
    def __init__(self, screen) -> None:
        self.settings: Settings = static_settings
        self.scene_manager: SceneManager = static_scene_manager
        self.screen: pygame.surface.Surface = screen
        self.buttons: list = [
            Button(pygame.display.Info().current_w // 2 - 100, 400, 200, 100, text = "Back to Menu", on_click=self.backToMenu)
        ]
        self.game_over = Text(None, 100, "Game Over")
        self.score = Text(None, 60, f"Score: {str(self.settings.score)}")
        self.music: Music = static_music
        self.music.play(self.settings.getAssetsPath() + "audio/music/Winning Sound Effect.mp3")


    def physicsUpdate(self, physics_delta_time: float) -> list:
        pass


    def update(self, draw_delta_time: float) -> None:
        self.screen.blit(self.game_over.getText(), (self.screen.get_width() // 2 - self.game_over.getText().get_width() // 2, 100))
        self.screen.blit(self.score.getText(), (self.screen.get_width() // 2 - self.score.getText().get_width() // 2, 200))
        for button in self.buttons:
            button.onClick()
            button.draw(self.screen)


    def backToMenu(self):
        self.music.play(self.settings.getAssetsPath() + "audio/music/time_for_adventure.mp3")
        self.scene_manager.addCurrentScene("MainScene")
        self.scene_manager.removeCurrentScene("GameOver")