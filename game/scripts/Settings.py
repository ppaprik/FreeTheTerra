import os
import tkinter as tk


#----------------------------------------------------------------------------------------------------
# Setting class (all for game)

class Settings:
    def __init__(self) -> None:
        root: tk.Tk = tk.Tk()
        self.screen_size: tuple[int, int] = (root.winfo_screenwidth(), root.winfo_screenheight())
        self.fullscreen_size: tuple[int, int] = (root.winfo_screenwidth(), root.winfo_screenheight())
        root.destroy()

        self.running: bool = True

        self.run_path: str = ""
        self.assets_path: str = self.run_path + "assets\\"
        self.sprite_path: str = self.assets_path + "sprites\\"

        self.window_caption: str = "FreeTheTerra"
        self.window_caption_img = self.sprite_path + "crown.png"

        self.color = {
            "WHITE": (255, 255, 255),
            "BLACK": (0, 0, 0),
            "RED": (255, 0, 0),
            "GREEN": (0, 255, 0),
            "BLUE": (0, 0, 255),
            "YELLOW": (255, 255, 0),
            "ORANGE": (255, 128, 0),
            "PURPLE": (128, 0, 255),
            "PINK": (255, 0, 255),
            "GRAY": (128, 128, 128),
            "DARK_GRAY": (64, 64, 64),
            "LIGHT_GRAY": (192, 192, 192),
            "SKY_BLUE": (135, 206, 235),
            "GRASS": (34, 139, 34),
            "DIRT": (139, 69, 19),
            "STONE": (128, 128, 128)
        }
        self.sound_volume: float = 0.0
        self.music_volume: float = 0.0

        self.previous_scene: str = ""
        self.fullscreen: bool = False

        self.score: int = 0
        self.best_score: int = 0

        self.updated = True

    
    def updatePath(self):
        self.assets_path: str = self.run_path + "assets\\"
        self.sprite_path: str = self.assets_path + "sprites\\"
        self.window_caption_img = self.sprite_path + "crown.png"


    #--------------------------------------------------
    # Getter

    def getSceenSize(self) -> tuple[int, int]:
        return self.screen_size
    

    def getRunning(self) -> bool:
        return self.running
    

    def getRunPath(self) -> str:
        return self.run_path
    
    
    def getAssetsPath(self) -> str:
        return self.assets_path
    
    
    def getSpritePath(self) -> str:
        return self.sprite_path
    

    def getWindowsCaptionImg(self) -> str:
        return self.window_caption_img


    def getWindowCaption(self) -> str:
        return self.window_caption
    

    def getColor(self, color_name: str) -> tuple[int, int, int]:
        return self.color[color_name]
    

    def getSoundVolume(self) -> float:
        return self.sound_volume
    

    def getMusicVolume(self) -> float:
        return self.music_volume
    

    def getPreviousScene(self) -> str:
        return self.previous_scene
    

    def isFullscreen(self) -> bool:
        return self.fullscreen
    

    def fullscreenSize(self):
        return self.fullscreen_size
    

    def getScore(self) -> int:
        return self.score
    

    #--------------------------------------------------
    # Setter

    def setFullscreen(self, fullscreen: bool) -> None:
        self.fullscreen = fullscreen


    def setPreviousScene(self, previous_scene: str) -> None:
        self.previous_scene = previous_scene


    def setWindowCaption(self, window_caption: str) -> None:
        self.window_caption = window_caption


    def setSceenSize(self, screen_size: tuple[int, int]) -> None:
        self.screen_size = screen_size


    def setRunning(self, running: bool) -> None:
        self.running = running

    
    def setSoundVolume(self, sound_volume: float) -> None:
        self.sound_volume = sound_volume


    def setMusicVolume(self, music_volume: float) -> None:
        self.music_volume = music_volume


    def setScore(self, score: int) -> None:
        self.score = score

    def setRunPath(self, run_path: str) -> None:
        self.run_path = run_path
        self.updatePath()


#----------------------------------------------------------------------------------------------------
# Global static ini for setting

static_settings: Settings = Settings()