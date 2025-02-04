import pygame

from scripts.Settings import Settings, static_settings
from scripts.SceneManager import SceneManager, static_scene_manager


#----------------------------------------------------------------------------------------------------
# EventListener for whole game

class EventListener:
    def __init__(self) -> None:
        self.settings: Settings = static_settings
        self.scene_manager: SceneManager = static_scene_manager
        self.last_key = None


    #--------------------------------------------------
    # Update

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.settings.setRunning(False)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_F3] and not self.last_key_state[pygame.K_F3]:
            if "FPSmonitor" in self.scene_manager.getCurrentScenes():
                self.scene_manager.removeCurrentScene("FPSmonitor")
                print("FPSmonitor removed")
            else:
                self.scene_manager.addCurrentScene("FPSmonitor")
                print("FPSmonitor added")

        if keys[pygame.K_ESCAPE] and not self.last_key_state[pygame.K_ESCAPE]:
            if "Pause" in self.scene_manager.getCurrentScenes():
                self.scene_manager.removeCurrentScene("Pause")
                print("Pause removed")
            else:
                self.scene_manager.addCurrentScene("Pause")
                print("Pause added")

        self.last_key_state = keys



#----------------------------------------------------------------------------------------------------
# Public static variable

event_listener = EventListener()