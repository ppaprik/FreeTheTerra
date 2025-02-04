import pygame

from scripts.Text import Text


#----------------------------------------------------------------------------------------------------
# Main Scene (here is everything that will be on the main screen)

class FPSmonitor():
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.draw_fps: Text = Text(None, 20, "FPS:")
        self.physics_fps: Text = Text(None, 20, "FPS:")
        self.screen: pygame.surface.Surface = screen


    #--------------------------------------------------
    # Updates

    def physicsUpdate(self, physics_delta_time: float) -> list:
        self.physics_fps.setText(f"Physics FPS: {round(1 / physics_delta_time, 2)}")


    def update(self, draw_delta_time: float) -> None:
        self.draw_fps.setText(f"FPS: {round(1 / draw_delta_time, 2)}")
        self.screen.blit(self.draw_fps.getText(), (0, 0))
        self.screen.blit(self.physics_fps.getText(), (0, 20))


    #--------------------------------------------------
    # Getters