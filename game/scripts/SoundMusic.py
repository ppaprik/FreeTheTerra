import pygame

from scripts.Settings import static_settings


#----------------------------------------------------------------------------------------------------
# Music for background

class Music:
    def __init__(self) -> None:
        self.settings = static_settings

    def play(self, path_to_music: str, loops: int = -1, volume: float = 0.2) -> None:
        pygame.mixer.music.load(path_to_music)
        pygame.mixer.music.set_volume(self.settings.getMusicVolume())
        pygame.mixer.music.play(loops=loops)
    

    def stop(self) -> None:
        pygame.mixer.music.stop()


    def pause(self) -> None:
        pygame.mixer.music.pause()


    def unpause(self) -> None:
        pygame.mixer.music.unpause()


    def changeMusicVolume(self):
        pygame.mixer.music.set_volume(self.settings.getMusicVolume())



static_music = Music()



#----------------------------------------------------------------------------------------------------
# Sound for soundeffect

class Sound:
    def __init__(self, path_to_sound: str, volume: float = 0.7) -> None:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.settings = static_settings
        shoot_sound = pygame.mixer.Sound(path_to_sound)
        shoot_sound.set_volume(self.settings.getSoundVolume())
        shoot_sound.play()