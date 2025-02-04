import pygame
import pygame.surface

from scripts.UI import Button
from scripts.Settings import Settings, static_settings
from scripts.SceneManager import SceneManager, static_scene_manager
from scenes.GameScene import GameScene
from scenes.Pause import Pause
from scripts.SoundMusic import Music, static_music
from scripts.Text import Text


#----------------------------------------------------------------------------------------------------
# Main Scene (here is everything that will be on the main screen)

class MainScene():
    def __init__(self, screen) -> None:
        self.settings: Settings = static_settings
        self.scene_manager: SceneManager = static_scene_manager
        self.screen: pygame.surface.Surface = screen
        self.buttons: list = [
            Button(pygame.display.Info().current_w // 2 - 100, 100, 200, 100, text = "Start", on_click=self.start_game),
            Button(pygame.display.Info().current_w // 2 - 100, 250, 200, 100, text = "Options", on_click=self.options),
            Button(pygame.display.Info().current_w // 2 - 100, 400, 200, 100, text = "Quit", on_click=self.quit_game)
        ]
        self.music: Music = static_music
        self.music.play(self.settings.getAssetsPath() + "audio/music/time_for_adventure.mp3")
        self.best_score = Text(None, 40, f"Best Score: {str(self.settings.best_score)}")


    #--------------------------------------------------
    # Update

    def physicsUpdate(self, physics_delta_time: float) -> None:
        pass


    def update(self, draw_delta_time: float) -> None:
        temporal_offset = 50
        offset = (self.screen.get_size()[1] // len(self.buttons))
        for index, button in enumerate(self.buttons):
            pos = [0, 0]
            pos[0] = (self.screen.get_size()[0] // 2) - (button.getSize()[0] // 2)
            pos[1] = temporal_offset if index == 0 else index * offset + temporal_offset
            button.updatePos(pos)
            button.onClick()
            button.draw(self.screen)

        self.best_score.setText(f"Best Score: {str(self.settings.best_score)}")
        self.screen.blit(self.best_score.getText(), (self.screen.get_width() - self.best_score.getText().get_width() // 2 - 180, 300))

    #--------------------------------------------------
    # Events

    def start_game(self):
        # Switch to the GameScene
        self.scene_manager.addScene("GameScene", GameScene(self.screen))
        self.scene_manager.addScene("Pause", Pause(self.screen))
        self.scene_manager.removeCurrentScene("MainScene")
        self.scene_manager.addCurrentScene("GameScene")
        


    def options(self):
        self.scene_manager.removeCurrentScene("MainScene")
        self.scene_manager.addCurrentScene("Options")
        self.settings.setPreviousScene("MainScene")


    def quit_game(self):
        self.settings.setRunning(False)