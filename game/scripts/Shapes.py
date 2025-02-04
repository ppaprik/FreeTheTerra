import pygame

from scripts.Settings import Settings, static_settings


#----------------------------------------------------------------------------------------------------
# Block class

class Block:
    def __init__(self, x, y, width, height, sprite_path):
        # 0, 0, 28, 9, "sprites/terrain/grass.png" 
        self.boundary = pygame.Rect(x, y, width, height)
        self.sprite = pygame.image.load(sprite_path)
        self.scale_factor = 2
        self.sprite = pygame.transform.scale(self.sprite, (int(width * self.scale_factor), int(height * self.scale_factor)))


class GrassBlock(Block):
    def __init__(self, x, y, width, height):
        sprite_path = static_settings.getAssetsPath() + "sprites/terrain/grass.png"
        super().__init__(x, y, width, height, sprite_path)


class DirtBlock(Block):
    def __init__(self, x, y, width, height):
        sprite_path = static_settings.getAssetsPath() + "sprites/terrain/dirt.png"
        super().__init__(x, y, width, height, sprite_path)


class StoneBlock(Block):
    def __init__(self, x, y, width, height):
        sprite_path = static_settings.getAssetsPath() + "sprites/terrain/stone.png"
        super().__init__(x, y, width, height, sprite_path)

    

#----------------------------------------------------------------------------------------------------
# Rectangle class

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height



#----------------------------------------------------------------------------------------------------
# Circle class

class Circle():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


    #--------------------------------------------------
    # Getters

    def getRadius(self) -> int:
        return self.radius
