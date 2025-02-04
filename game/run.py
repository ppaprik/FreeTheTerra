import pygame
import threading
import time
import multiprocessing
import os

from scripts.Settings import Settings, static_settings
from scripts.SceneManager import SceneManager, static_scene_manager
from scripts.EventListener import event_listener
from scenes.Options import Options, static_options

from scripts.Text import Text

from scenes.MainScene import MainScene
from scenes.FPSmonitor import FPSmonitor


#----------------------------------------------------------------------------------------------------
# Game class (whoile game starts here)

class Game():
    def __init__(self):
        pygame.init()

        self.settings: Settings = static_settings
        self.settings.setSceenSize((1000, 600))
        self.settings.setRunPath(os.path.dirname(os.path.abspath(__file__)) + "\\")
        self.on_start()

        if self.settings.isFullscreen():
            self.screen: pygame.surface.Surface = pygame.display.set_mode(self.settings.fullscreenSize(), pygame.FULLSCREEN)
        else:
            self.screen: pygame.surface.Surface = pygame.display.set_mode(self.settings.getSceenSize())

        pygame.display.set_icon(pygame.image.load(self.settings.getWindowsCaptionImg()))
        pygame.display.set_caption(self.settings.getWindowCaption())
        self.clock = pygame.time.Clock()

        self.scene_manager: SceneManager = static_scene_manager
        self.scene_manager.addScene("MainScene", MainScene(self.screen))
        self.scene_manager.addScene("FPSmonitor", FPSmonitor(self.screen))
        self.scene_manager.addScene("Options", Options(self.screen))

        self.scene_manager.addCurrentScene("MainScene")


    #--------------------------------------------------
    # Start of Program

    def start(self):
        # self.physics_thread = threading.Thread(target=self.physics_update).start()
        self.draw_update()


    #--------------------------------------------------
    # Draw Update

    def draw_update(self):
        delta_time: float = 0
        draw_delta_time: float = 0
        required_draw_delta_time : float = round((1 / 60), 4)

        while self.settings.getRunning():
            current_time: float = time.time()
            event_listener.update()
            draw_delta_time += delta_time

            if draw_delta_time >= required_draw_delta_time:
                self.screen.fill(self.settings.getColor("BLACK"))

                for scene in self.scene_manager.getCurrentScenes():
                    self.scene_manager.getScene(scene).update(draw_delta_time)

                pygame.display.flip()

                draw_delta_time = 0

            delta_time = round((time.time() - current_time), 4)


    #--------------------------------------------------
    # Physics Update

    def physics_update(self):
        delta_time: float = 0
        physics_delta_time: float = 0
        required_physics_delta_time : float = round((1 / 200), 4)

        while self.settings.getRunning():
            current_time: float = time.time()
            physics_delta_time += delta_time

            if physics_delta_time >= required_physics_delta_time:
                for scene in self.scene_manager.getCurrentScenes():
                    self.scene_manager.getScene(scene).physicsUpdate(physics_delta_time)

                physics_delta_time = 0

            delta_time = round((time.time() - current_time), 4)


    def on_start(self):
        try:
            with open(self.settings.getRunPath() + "setting.txt", "r") as file:
                array: list = file.readlines()
                self.settings.setMusicVolume(float(array[0].strip()))
                self.settings.setSoundVolume(float(array[1].strip()))
                self.settings.setFullscreen(bool(int(array[2].strip())))
                self.settings.best_score = int(array[3].strip())
        except Exception as error:
            print(f"<< Failed: to load settings. Error: {error}")



#----------------------------------------------------------------------------------------------------
# EXECUTE

if __name__ == "__main__":
    game = Game()
    game.start()