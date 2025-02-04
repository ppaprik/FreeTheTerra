import pygame

from scripts.Text import Text
from scripts.Settings import Settings, static_settings
from scripts.SoundMusic import Sound


#----------------------------------------------------------------------------------------------------
# Buttons class

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, 
                button_color: tuple[int, int, int] = (255, 255, 255), 
                hover_color: tuple[int, int, int] = (192, 192, 192), 
                text: str = "SAMPLE TEXT", 
                text_color: tuple[int,int ,int] = (0, 0, 0), 
                on_click: callable = None):
        self.pos = [x, y]
        self.size = (width, height)
        self.color = button_color
        self.hover_color = hover_color
        self.text = Text(None, 30, text, True, text_color)
        self.on_click = on_click
        self.last_mouse_state = [False, False, False]
        self.settings = static_settings
        self.hover = False
        self.hover_before = False


    def updatePos(self, pos: tuple[int, int]):
        self.pos[0] = pos[0]
        # self.pos[1] = pos[1]


    def draw(self, screen):

        current_color = self.color
        if self.isHovering(pygame.mouse.get_pos()):
            current_color = self.hover_color
        pygame.draw.rect(screen, current_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        screen.blit(self.text.getText(), (self.pos[0] + (self.size[0] // 2 - self.text.getText().get_width() // 2), self.pos[1] + (self.size[1] // 2 - self.text.getText().get_height() // 2)))


    def isHovering(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]:
            self.hover = True
            self.playHoverSound()
            self.hover_before = True
            return True
        self.hover = False
        self.hover_before = False
        return False
    

    def playHoverSound(self):
        if self.hover and not self.hover_before:
            Sound(self.settings.getAssetsPath() + "audio/soundeffects/hover.mp3")


    def onClick(self):
        if self.on_click is not None:
            mouse = pygame.mouse.get_pressed()
            if mouse[0] and self.isHovering(pygame.mouse.get_pos()) and not self.last_mouse_state[0]:
                self.on_click()

            self.last_mouse_state = mouse


    def getSize(self):
        return self.size
    

    def setButtonColor(self, color: tuple[int, int, int]):
        self.color = color
    


class Slider:
    def __init__(self, x: int, y: int, width: int, height: int, 
                 slider_color: tuple[int, int, int] = (200, 200, 200), 
                 knob_color: tuple[int, int, int] = (255, 0, 0), 
                 initial_volume: float = 0.5,
                 on_drag: callable = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.slider_color = slider_color
        self.knob_color = knob_color
        self.knob_radius = height // 2
        self.volume_level = initial_volume
        self.dragging = False
        self.on_drag = on_drag

    def draw(self, screen):
        pygame.draw.rect(screen, self.slider_color, (self.x, self.y, self.width, self.height))
        knob_x_pos = int(self.x + self.volume_level * self.width)
        pygame.draw.circle(screen, self.knob_color, (knob_x_pos, self.y + self.height // 2), self.knob_radius)


    def onDrag(self):
        if self.on_drag is not None:
            keys = pygame.mouse.get_pressed()

            if keys[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.x <= mouse_x <= self.x + self.width and self.y - self.knob_radius <= mouse_y <= self.y + self.knob_radius:
                    self.dragging = True
                else: 
                    self.dragging = False

            if self.dragging:
                mouse_x, _ = pygame.mouse.get_pos()
                knob_x = min(max(self.x, mouse_x), self.x + self.width)
                self.volume_level = (knob_x - self.x) / self.width

                self.on_drag(self.volume_level)


    def setInitialVolume(self, volume_level: float):
        self.volume_level = volume_level


    def updatePos(self, pos: tuple[int, int]):
        self.x = pos[0]
        # self.pos[1] = pos[1]


    def getSize(self):
        return (self.width, self.height)