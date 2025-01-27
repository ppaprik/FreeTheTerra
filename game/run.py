import pygame
import threading
import time

#------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN GAME CLASS

class Game():
    pygame.init()
    pygame.font.init()


    #----------------------------------------------------------------------------------------------------
    # VARIABLES
    
    # GAME
    running: bool = True

    # DEFAULT PATH TO GAME (IF GAME IS RUNNED FROM ANOTHER LOCATION THIS MUST BE CHANGED)
    main_path: str = "./game/"

    # EVERYTHING FOR WINDOW
    screen: pygame.surface.Surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_icon(pygame.image.load(f"{main_path}assets/sprites/crown.png"))
    pygame.display.set_caption("FreeTheTerra")

    # COLORS
    WHITE: tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)

    # TEXT
    font: pygame.font.Font = pygame.font.Font(None, 20)
    text: pygame.surface.Surface = font.render("SAMPLE TEXT", True, WHITE, None)


    #----------------------------------------------------------------------------------------------------
    # INIT

    def __init__(self):
        pass


    #----------------------------------------------------------------------------------------------------
    # START OF PROGRAM

    def start(self):
        physics_thread = threading.Thread(target=self.physics_update).start()
        self.draw_update()


    #----------------------------------------------------------------------------------------------------
    # UPDATES

    def draw_update(self):
        delta_time: float = 0
        draw_delta_time: float = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            current_time: float = time.time()
            draw_delta_time += delta_time

            if draw_delta_time >= 0.016:
                fps = 1 / draw_delta_time
                print(f"Draw FPS: {fps:.2f} \t Draw delta: {draw_delta_time:.4f}")
                draw_delta_time = 0

            delta_time = round((time.time() - current_time), 4)


    def physics_update(self):
        delta_time: float = 0
        physics_delta_time: float = 0

        while self.running:
            current_time: float = time.time()
            physics_delta_time += delta_time

            if physics_delta_time >= 0.001:
                fps = 1 / physics_delta_time
                print(f"Physics FPS: {fps:.2f} \t Physics delta: {physics_delta_time:.4f}")
                physics_delta_time = 0

            delta_time = round((time.time() - current_time), 4)

            

#------------------------------------------------------------------------------------------------------------------------------------------------------
# EXECUTE

if __name__ == "__main__":
    game = Game()
    game.start()