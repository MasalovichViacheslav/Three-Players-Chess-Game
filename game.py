import pygame
from board import points_dict, board, rect_center_coords, draw_symbol
from colors import GOLD_LIGHT, GOLD_VERY_DARK, BLACK

WIDTH = 1300
HEIGHT = 800
FPS = 30

# Game and game window creation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
board_background = pygame.Surface((WIDTH - 300, HEIGHT - 100))
board_background_rect = board_background.get_rect()
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

# Board drawing
# Board frame drawing
pygame.draw.lines(board_background, GOLD_LIGHT, True, (points_dict["p122"], points_dict["p123"], points_dict["p124"],
                                                       points_dict["p125"], points_dict["p126"], points_dict["p127"]))


# Board cells drawing
for index in range(len(board)):
    if index % 2 == 0:
        board[index].cell_draw(board_background, GOLD_VERY_DARK)
    else:
        board[index].cell_draw(board_background, GOLD_LIGHT)


# Letters and digits drawing on the board frame
letters_digits = (
"8", "7", "6", "5", "9", "10", "11", "12", "L", "K", "J", "I", "E", "F", "G", "H", "12", "11", "10", "9", "4", "3", "2",
"1", "H", "G", "F", "E", "D", "C", "B", "A", "1", "2", "3", "4", "5", "6", "7", "8", "A", "B", "C", "D", "I", "J", "K",
"L")
nearby_points_coords_lst = [points_dict["p" + str(numb)] for numb in range(1, 49)]
nearby_points_coords_lst += [points_dict["p1"]]
empty_list = []
center_points_coords = rect_center_coords(empty_list, nearby_points_coords_lst)
draw_symbol(letters_digits, 0, GOLD_LIGHT, board_background, center_points_coords)


# Game cycle
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    # Rendering
    screen.fill(BLACK)
    screen.blit(board_background, board_background_rect)
    # Screen turn over
    pygame.display.flip()


pygame.quit()