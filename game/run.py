import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drawing Shapes")

clock = pygame.time.Clock()

delta_time: int = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen

    # Drawing various shapes
    pygame.draw.line(screen, (255, 255, 255), (100, 100), (200, 200), 5)
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, 100, 100))
    pygame.draw.circle(screen, (0, 255, 0), (300, 300), 50)
    pygame.draw.ellipse(screen, (0, 0, 255), (400, 50, 150, 100))
    pygame.draw.polygon(screen, (255, 255, 0), [(150, 50), (200, 150), (100, 150)])
    pygame.draw.arc(screen, (255, 0, 255), (500, 50, 150, 100), 0, math.pi, 5)
    pygame.draw.lines(screen, (0, 255, 255), False, [(300, 400), (350, 450), (400, 400)], 3)
    pygame.draw.aaline(screen, (255, 165, 0), (600, 50), (750, 200), 1)

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000

pygame.quit()
