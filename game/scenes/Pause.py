import pygame

from scripts.UI import Button
from scripts.SceneManager import SceneManager, static_scene_manager
from scripts.Settings import Settings, static_settings
from scripts.SoundMusic import Music, static_music


#----------------------------------------------------------------------------------------------------
# Pause scene

class Pause():
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.screen: pygame.surface.Surface = screen
        self.scene_manager: SceneManager = static_scene_manager
        self.settings = static_settings

        self.buttons: list = [
            Button(pygame.display.Info().current_w // 2 - 100, 50, 180, 80, text = "Unpause", on_click=self.unpause),
            Button(pygame.display.Info().current_w // 2 - 100, 150, 180, 80, text = "Options", on_click=self.options),
            # Button(pygame.display.Info().current_w // 2 - 100, 250, 180, 80, text = "Save"),
            Button(pygame.display.Info().current_w // 2 - 100, 350, 180, 80, text = "Exit", on_click=self.quit)
        ]


    def physicsUpdate(self, physics_delta_time: float):
        pass


    def update(self, draw_delta_time: float):
        background = pygame.Surface(self.screen.get_size())
        background.fill((255, 255, 255))
        background.set_alpha(64)  # 100% opacity = 255
        self.screen.blit(background, (0, 0))

        temporal_offset = 30
        offset = (self.screen.get_size()[1] // len(self.buttons))
        for index, button in enumerate(self.buttons):
            pos = [0, 0]
            pos[0] = (self.screen.get_size()[0] // 2) - (button.getSize()[0] // 2)
            pos[1] = temporal_offset if index == 0 else index * offset + temporal_offset
            button.updatePos(pos)
            button.onClick()
            button.draw(self.screen)
        

    #--------------------------------------------------
    # Events

    def unpause(self):
        self.scene_manager.removeCurrentScene("Pause")


    def options(self):
        self.scene_manager.removeCurrentScene("Pause")
        self.scene_manager.addCurrentScene("Options")
        self.settings.setPreviousScene("Pause")


    def quit(self):
        self.scene_manager.removeCurrentScene("Pause")
        self.scene_manager.removeCurrentScene("GameScene")
        self.scene_manager.removeScene("GameScene")
        self.scene_manager.removeScene("Pause")
        static_music.stop()

        self.scene_manager.addCurrentScene("MainScene")
        