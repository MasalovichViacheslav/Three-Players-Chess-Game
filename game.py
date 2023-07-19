import pygame
from board import points_dict, board
from colors import GRAY, GREEN, OLIVE, WHITE

WIDTH = 1200
HEIGHT = 800
FPS = 30

# Game and game window creation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

pygame.draw.lines(screen, GRAY, True, (points_dict["p122"], points_dict["p123"], points_dict["p124"],
                                        points_dict["p125"], points_dict["p126"], points_dict["p127"]))

for index in range(len(board)):
    if index % 2 == 0:
        board[index].cell_draw(screen, GRAY)
    else:
        board[index].cell_draw(screen, WHITE)


# Game cycle
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    # Rendering
    # screen.fill(GRAY)
    # Screen turn over
    pygame.display.flip()

pygame.quit()