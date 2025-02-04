

from scripts.Settings import Settings, static_settings


#----------------------------------------------------------------------------------------------------
# Scene Manager Class

class SceneManager:
    def __init__(self):
        self.scenes: dict = {}
        self.current_scenes: list = []


    #--------------------------------------------------
    # Getter

    def getScene(self, name: str) -> type:
        return self.scenes[name]
    

    def getCurrentScenes(self) -> list:
        return self.current_scenes


    #--------------------------------------------------
    # Setter

    def addScene(self, scene_name: str, scene: type) -> None:
        self.scenes[scene_name] = scene


    def addCurrentScene(self, scene_name: str) -> None:
        self.current_scenes.append(scene_name)


    def removeCurrentScene(self, scene_name: str) -> None:
        self.current_scenes.remove(scene_name)

    
    def removeScene(self, scene_name: str) -> None:
        self.scenes.pop(scene_name)



#----------------------------------------------------------------------------------------------------
# Public static variable

static_scene_manager = SceneManager()