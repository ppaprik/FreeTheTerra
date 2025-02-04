import pygame


#----------------------------------------------------------------------------------------------------
# Text Class

class Text(pygame.font.Font):
    def __init__(self, font_name: str, font_size: int, text, antialiased: bool = True, color: tuple[int, int, int] = (255, 255, 255), background: str = None):
        super().__init__(font_name, font_size)
        self.text: str = text
        self.antialiased: bool = antialiased
        self.color: tuple[int, int, int] = color
        self.background: str = background

        self.text: pygame.surface.Surface = super().render(text, antialiased, color, background)


    #--------------------------------------------------
    # Getter

    def getText(self) -> pygame.surface.Surface:
        return self.text


    #--------------------------------------------------
    # Setter

    def setText(self, text: str) -> None:
        self.text = super().render(text, self.antialiased, self.color, self.background)