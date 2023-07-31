import pygame
from board import points_dict, board, rect_center_coords, draw_symbol
from colors import GOLD_LIGHT, GOLD_VERY_DARK, BLACK
from pieces import all_pieces, all_pieces_lst

WIDTH = 1200
HEIGHT = 800
FPS = 30

# Game and game window creation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

# BOARD CONSTANT ELEMENTS DRAWING
board_background = pygame.Surface((WIDTH - 300, HEIGHT))
board_background_rect = board_background.get_rect()

# Board frame drawing
pygame.draw.lines(board_background, GOLD_LIGHT, True, (points_dict["p122"], points_dict["p123"], points_dict["p124"],
                                                       points_dict["p125"], points_dict["p126"], points_dict["p127"]))


# Letters and digits drawing on the board frame
letters_digits = (
    "8", "7", "6", "5", "9", "10", "11", "12", "L", "K", "J", "I", "E", "F", "G", "H", "12", "11", "10", "9", "4", "3",
    "2", "1", "H", "G", "F", "E", "D", "C", "B", "A", "1", "2", "3", "4", "5", "6", "7", "8", "A", "B", "C", "D", "I",
    "J", "K", "L"
)
nearby_points_coords_lst = [points_dict["p" + str(numb)] for numb in range(1, 49)]
nearby_points_coords_lst += [points_dict["p1"]]
empty_list = []
center_points_coords = rect_center_coords(empty_list, nearby_points_coords_lst)
draw_symbol(letters_digits, 0, GOLD_LIGHT, board_background, center_points_coords)


# GAME CYCLE
running = True
selected_piece_list = []
cells_for_move = []
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in all_pieces_lst:
                if piece.rect.collidepoint(event.pos) and piece.is_selected is False and len(selected_piece_list) == 0:
                    piece.is_selected = True
                    cells_for_move = piece.highlight_cells()
                    selected_piece_list.append(piece)
                    break

                elif piece.rect.collidepoint(event.pos) and piece.is_selected is True and len(selected_piece_list) == 1:
                    piece.is_selected = False
                    cells_for_move = piece.unhighlight_cells()
                    selected_piece_list.clear()
                    break

            for cell in cells_for_move[:-1]:
                if cell.rect.collidepoint(event.pos) and len(cells_for_move) != 1:
                    for piece in all_pieces_lst:
                        if piece.position == cell.position:
                            all_pieces_lst.remove(piece)
                    selected_piece_list[0].unhighlight_cells()
                    selected_piece_list[0].position = cell.position
                    cell.occupied = True
                    selected_piece_list[0].is_selected = False
                    selected_piece_list.clear()
                    cells_for_move[-1].occupied = False


        elif event.type == pygame.MOUSEBUTTONUP:
            pass


    # UPDATE


    # RENDERING
    screen.fill(BLACK)
    screen.blit(board_background, board_background_rect)
    # Board cells drawing
    for index in range(len(board)):
        board[index].cell_draw(board_background)
    # Pieces drawing
    for piece in all_pieces_lst:
        piece.piece_drawing(board_background)

    # SCREEN TURN OVER
    pygame.display.flip()


pygame.quit()