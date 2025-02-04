import pygame

from scripts.SoundMusic import Music
from scripts.Settings import Settings, static_settings
from scripts.SceneManager import SceneManager, static_scene_manager
from scripts.SoundMusic import static_music
from scripts.UI import Button, Slider


#----------------------------------------------------------------------------------------------------
# Options scene

class Options:
    def __init__(self, screen):
        self.screen: pygame.surface.Surface = screen
        self.scene_manager: SceneManager = static_scene_manager
        self.music = static_music
        self.settings: Settings = static_settings
        self.buttons: list = [
            # Button(pygame.display.Info().current_w // 2 - 100, 100, 200, 100, text = "Fullscreen", on_click=self.set_fullscreen),
            Button(pygame.display.Info().current_w // 2 - 100 - 25, 400, 100, 50, text = "Cancel", on_click=self.cancel_settings),
            Button(pygame.display.Info().current_w // 2 - 100 + 125, 400, 100, 50, text = "Apply", on_click=self.apply_settings),
        ]
        self.sliders: list = [
            Slider(pygame.display.Info().current_w // 2 - 200, 250, 400, 20, on_drag=self.changeMusicVolume),
            Slider(pygame.display.Info().current_w // 2 - 200, 300, 400, 20, on_drag=self.changeSoundVolume)
        ]
        self.sliders[0].setInitialVolume(self.settings.getMusicVolume())
        self.sliders[1].setInitialVolume(self.settings.getSoundVolume())

        if self.settings.isFullscreen():
            self.buttons[0].setButtonColor(self.settings.getColor("GREEN"))

    
    def changeMusicVolume(self, volume_level: float):
        self.settings.setMusicVolume(volume_level)
        self.music.changeMusicVolume()


    def changeSoundVolume(self, volume_level: float):
        self.settings.setSoundVolume(volume_level)

    
    def physicsUpdate(self, physics_delta_time: float):
        pass


    def update(self, draw_delta_time: float):
        for button in self.buttons:
            pos = [0, 0]
            pos[0] = (self.screen.get_size()[0] // 2) - (button.getSize()[0] // 2)
            button.updatePos(pos)
            self.buttons[0].updatePos((((self.screen.get_size()[0] // 2) - (self.buttons[0].getSize()[0] // 2) - 75), 0))
            self.buttons[1].updatePos((((self.screen.get_size()[0] // 2) - (self.buttons[1].getSize()[0] // 2) + 75), 0))
            button.onClick()
            button.draw(self.screen)

        for slider in self.sliders:
            slider.updatePos((((self.screen.get_size()[0] // 2) - (slider.getSize()[0] // 2)), 0))
            slider.onDrag()
            slider.draw(self.screen)


    #--------------------------------------------------
    # Events

    def set_fullscreen(self):
        if self.settings.isFullscreen():
            self.settings.setFullscreen(False)
            self.buttons[0].setButtonColor(self.settings.getColor("WHITE"))
        else:
            self.settings.setFullscreen(True)
            self.buttons[0].setButtonColor(self.settings.getColor("GREEN"))


    def cancel_settings(self):
        self.scene_manager.removeCurrentScene("Options")
        self.scene_manager.addCurrentScene(self.settings.getPreviousScene())


    def apply_settings(self):
        if self.settings.isFullscreen():
            self.screen = pygame.display.set_mode(self.settings.fullscreenSize(), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.settings.getSceenSize(), pygame.RESIZABLE)

        self.settings.updated = False

        with open(self.settings.getRunPath() + "setting.txt", "w") as file:
            array = [
                str(self.settings.getMusicVolume()) + "\n",
                str(self.settings.getSoundVolume()) + "\n",
                str(int(self.settings.isFullscreen()))
            ]
            print(self.settings.isFullscreen())
            file.writelines(array)



static_options = Options