import pygame
from board import points_dict, board, rect_center_coords, draw_symbol
from colors import GOLD_LIGHT, BLACK
from pieces import all_pieces_lst

WIDTH = 1400
HEIGHT = 800
FPS = 30

# Game and game window creation
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Players Chess Game")
clock = pygame.time.Clock()

# BOARD CONSTANT ELEMENTS DRAWING
board_background = pygame.Surface((WIDTH - 400, HEIGHT))
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
move_queue_list = ["white", "black", "red"]

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in all_pieces_lst:
                # selecting a piece
                if piece.rect.collidepoint(event.pos) and piece.is_selected is False and len(selected_piece_list) == 0 \
                        and piece.move_frozen is False:
                    piece.is_selected = True
                    cells_for_move = piece.highlight_cells()
                    selected_piece_list.append(piece)
                    break

                # unselecting selected piece
                elif piece.rect.collidepoint(event.pos) and piece.is_selected is True and len(selected_piece_list) == 1:
                    piece.is_selected = False
                    cells_for_move = piece.unhighlight_cells()
                    selected_piece_list.clear()
                    break

            # piece move and events triggered by it
            for cell in cells_for_move[:-1]:
                if cell.rect.collidepoint(event.pos):

                    # captured piece delete
                    for piece in all_pieces_lst:
                        if piece.position == cell.position:
                            all_pieces_lst.remove(piece)

                    # checking whether castling move is available or not
                    if selected_piece_list[0].name in ["w_King", "b_King", "r_King"] and \
                            len(selected_piece_list[0].castling()) != 0 and \
                            cell in [key for key in selected_piece_list[0].castling().keys()]:
                        rook = selected_piece_list[0].castling()[cell][0]
                        rook_current_cell = selected_piece_list[0].castling()[cell][1]
                        rook_new_cell = selected_piece_list[0].castling()[cell][2]
                        # rook move during castling
                        rook_current_cell.occupied = False
                        rook.position = rook_new_cell.position
                        rook_new_cell.occupied = True

                    # selected piece move
                    selected_piece_list[0].unhighlight_cells()
                    selected_piece_list[0].position = cell.position
                    cell.occupied = True
                    selected_piece_list[0].first_move = False
                    selected_piece_list[0].is_selected = False
                    selected_piece_list.clear()
                    cells_for_move[-1].occupied = False
                    cells_for_move.clear()

                    # move queue change after piece move is completed
                    move_queue_list.append(move_queue_list.pop(0))
                    for piece in all_pieces_lst:
                        if piece.color == move_queue_list[0]:
                            piece.move_frozen = False
                        else:
                            piece.move_frozen = True
                    break

    # UPDATE

    # RENDERING
    screen.fill(BLACK)
    screen.blit(board_background, board_background_rect)
    # Board cells drawing
    for cell in board:
        cell.cell_draw(board_background)
    # Pieces drawing
    for piece in all_pieces_lst:
        piece.piece_drawing(board_background)

    # SCREEN TURN OVER
    pygame.display.flip()

pygame.quit()