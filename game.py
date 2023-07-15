import pygame
from board import points_dict

WIDTH = 1024
HEIGHT = 768
FPS = 30

# Colors creation
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game and game window creation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

pygame.draw.lines(screen, GREEN, True, (points_dict["p122"], points_dict["p123"], points_dict["p124"],
                                        points_dict["p125"], points_dict["p126"], points_dict["p127"]), 1)
pygame.display.update()

# Game cycle
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # # Update
    #
    # # Rendering
    # screen.fill(BLACK)
    # # Screen turn over
    # pygame.display.flip()

pygame.quit()
