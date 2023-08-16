import pygame
from board import points_dict, board, rect_center_coords, draw_symbol
from colors import GOLD_LIGHT, GOLD_VERY_DARK, BLACK, SPECIAL_WHITE, WHITE
from pieces import all_pieces_lst, kings_images, promotion_images, Rook, Bishop, Knight, Queen

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
board_background = pygame.Surface((WIDTH - 500, HEIGHT))
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

# MOVE QUEUE FIELD
queue_background = pygame.Surface((300, 100))
queue_background_rect = queue_background.get_rect()
queue_background_rect.x = 1000
queue_background_rect.y = 25


def draw_queue_field(queue, images=kings_images):
    queue_background.fill(GOLD_LIGHT)
    if queue[0] == "white":
        king1 = images[0]
        king2 = pygame.transform.scale_by(images[3], 0.6)
        king3 = pygame.transform.scale_by(images[3], 0.6)
    elif queue[0] == "black":
        king1 = pygame.transform.scale_by(images[3], 0.6)
        king2 = images[1]
        king3 = pygame.transform.scale_by(images[3], 0.6)
    else:
        king1 = pygame.transform.scale_by(images[3], 0.6)
        king2 = pygame.transform.scale_by(images[3], 0.6)
        king3 = images[2]

    king1.set_colorkey(SPECIAL_WHITE)
    king2.set_colorkey(SPECIAL_WHITE)
    king3.set_colorkey(SPECIAL_WHITE)

    king1_rect = king1.get_rect(center=(50, 50))
    king2_rect = king2.get_rect(center=(150, 50))
    king3_rect = king3.get_rect(center=(250, 50))

    queue_background.blit(king1, king1_rect)
    queue_background.blit(king2, king2_rect)
    queue_background.blit(king3, king3_rect)

    pygame.draw.rect(queue_background, WHITE, (0, 0, 100, 100), width=1)
    pygame.draw.rect(queue_background, WHITE, (100, 0, 100, 100), width=1)
    pygame.draw.rect(queue_background, WHITE, (200, 0, 100, 100), width=1)
    pygame.draw.rect(queue_background, GOLD_VERY_DARK, (0, 0, 300, 100), width=4)


# PAWN PROMOTION CHOICE FIELD
promotion_background = pygame.Surface((400, 100))
promotion_background_rect = promotion_background.get_rect()
promotion_background_rect.x = 950
promotion_background_rect.y = 350 * 10
promotion_background.fill(GOLD_LIGHT)


def draw_promotion_field(queue, images=promotion_images):
    promotion_background.fill(GOLD_LIGHT)
    if queue[0] == "white":
        piece1 = pygame.transform.scale_by(images["white"][0], 0.6)
        piece2 = pygame.transform.scale_by(images["white"][1], 0.6)
        piece3 = pygame.transform.scale_by(images["white"][2], 0.6)
        piece4 = pygame.transform.scale_by(images["white"][3], 0.6)
    elif queue[0] == "black":
        piece1 = pygame.transform.scale_by(images["black"][0], 0.6)
        piece2 = pygame.transform.scale_by(images["black"][1], 0.6)
        piece3 = pygame.transform.scale_by(images["black"][2], 0.6)
        piece4 = pygame.transform.scale_by(images["black"][3], 0.6)
    else:
        piece1 = pygame.transform.scale_by(images["red"][0], 0.6)
        piece2 = pygame.transform.scale_by(images["red"][1], 0.6)
        piece3 = pygame.transform.scale_by(images["red"][2], 0.6)
        piece4 = pygame.transform.scale_by(images["red"][3], 0.6)

    piece1.set_colorkey(SPECIAL_WHITE)
    piece2.set_colorkey(SPECIAL_WHITE)
    piece3.set_colorkey(SPECIAL_WHITE)
    piece4.set_colorkey(SPECIAL_WHITE)

    piece1_rect = piece1.get_rect(center=(promotion_background_rect.x + 50, promotion_background_rect.y + 50))
    piece2_rect = piece2.get_rect(center=(promotion_background_rect.x + 150, promotion_background_rect.y + 50))
    piece3_rect = piece3.get_rect(center=(promotion_background_rect.x + 250, promotion_background_rect.y + 50))
    piece4_rect = piece4.get_rect(center=(promotion_background_rect.x + 350, promotion_background_rect.y + 50))

    pygame.draw.rect(promotion_background, WHITE, (0, 0, 100, 100), width=1)
    pygame.draw.rect(promotion_background, WHITE, (100, 0, 100, 100), width=1)
    pygame.draw.rect(promotion_background, WHITE, (200, 0, 100, 100), width=1)
    pygame.draw.rect(promotion_background, WHITE, (300, 0, 100, 100), width=1)
    pygame.draw.rect(promotion_background, GOLD_VERY_DARK, (0, 0, 400, 100), width=4)

    screen.blit(piece1, piece1_rect)
    screen.blit(piece2, piece2_rect)
    screen.blit(piece3, piece3_rect)
    screen.blit(piece4, piece4_rect)

    return [piece1_rect, piece2_rect, piece3_rect, piece4_rect]


# GAME CYCLE
running = True
selected_piece_list = []
cells_for_move = []
move_queue_list = ["white", "black", "red"]
moves_dict = {}
moves_counter = 0
promotion_in_process = False

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # pawn promotion proceeding
            if promotion_in_process is True:
                for rect in promotion_pieces_rects:
                    print(event.pos)
                    print(promotion_pieces_rects)
                    print(rect.collidepoint(event.pos))
                    if rect.collidepoint(event.pos) and promotion_pieces_rects.index(rect) == 0:
                        new_piece = Queen(
                            pawn.name[0] + "_Queen(p_" + pawn.name[2] + "_pawn)", pawn.color, pawn.position, False,
                            False, False, promotion_images[pawn.color][0]
                        )
                    elif rect.collidepoint(event.pos) and promotion_pieces_rects.index(rect) == 1:
                        new_piece = Rook(
                            pawn.name[0] + "_Rook(p_" + pawn.name[2] + "_pawn)", pawn.color, pawn.position, False,
                            False, False, promotion_images[pawn.color][1]
                        )
                    elif rect.collidepoint(event.pos) and promotion_pieces_rects.index(rect) == 2:
                        new_piece = Bishop(
                            pawn.name[0] + "_Bishop(p_" + pawn.name[2] + "_pawn)", pawn.color, pawn.position, False,
                            False, False, promotion_images[pawn.color][2]
                        )
                    elif rect.collidepoint(event.pos) and promotion_pieces_rects.index(rect) == 3:
                        new_piece = Knight(
                            pawn.name[0] + "_Knight(p_" + pawn.name[2] + "_pawn)", pawn.color, pawn.position, False,
                            False, False, promotion_images[pawn.color][3]
                        )
                all_pieces_lst.append(new_piece)
                print(all_pieces_lst[-1].name, all_pieces_lst[-1].position)
                move_queue_list.append(move_queue_list.pop(0))
                for piece in all_pieces_lst:
                    if piece.color == move_queue_list[0]:
                        piece.move_frozen = False
                    else:
                        piece.move_frozen = True
                all_pieces_lst.remove(pawn)
                promotion_in_process = False
                promotion_background_rect.y = 350 * 10

            for piece in all_pieces_lst:

                # selecting a piece
                if piece.rect.collidepoint(event.pos) and piece.is_selected is False and len(selected_piece_list) == 0 \
                        and piece.move_frozen is False:
                    piece.is_selected = True
                    cells_for_move = piece.highlight_cells()
                    if "Pawn" in piece.name and len(piece.en_passant(moves_dict, moves_counter)) != 0:
                        cells_for_move.insert(-1, piece.en_passant(moves_dict, moves_counter)[0])
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

                    """
                    checking whether en passant move is available or not, if yes, the following en passant actions will
                    be executed:
                        - delete enemy piece captured through en passant;
                        - change "occupied status" of the cell occupied by the captured enemy piece.
                    The rest actions of en passant move are executed in "selected piece simple move" section
                    """
                    if "Pawn" in selected_piece_list[0].name and \
                            len(selected_piece_list[0].en_passant(moves_dict, moves_counter)) != 0:
                        selected_piece_list[0].en_passant(moves_dict, moves_counter)[2].occupied = False
                        all_pieces_lst.remove(selected_piece_list[0].en_passant(moves_dict, moves_counter)[1])

                    # adding move record in moves_dict
                    moves_counter += 1
                    """
                    each "key-value" pair in "moves_dict" will include:
                    key - move sequence number;
                    value - list that contains:
                        index 0 - piece (Piece object) that is moved to new position;
                        index 1 - cell occupied by the piece before move;
                        index 2 - cell to be occupied by the piece after move.
                    """
                    moves_dict[moves_counter] = [selected_piece_list[0], cells_for_move[-1], cell]

                    # captured piece delete
                    for piece in all_pieces_lst:
                        if piece.position == cell.position:
                            all_pieces_lst.remove(piece)

                    """
                    checking whether casting move is available or not, if yes, the following casting actions will 
                    be executed:
                        - change the rook position;
                        - change "occupied status" of the cells occupied by the rook before and after castling.
                    The rest actions of casting move are executed in "selected piece simple move" section 
                    """
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

                    # selected piece simple move
                    selected_piece_list[0].unhighlight_cells()
                    selected_piece_list[0].position = cell.position
                    cell.occupied = True
                    selected_piece_list[0].first_move = False
                    selected_piece_list[0].is_selected = False
                    if "Pawn" in selected_piece_list[0].name and selected_piece_list[0].promotion() is True:
                        promotion_in_process = True
                        promotion_background_rect.y /= 10
                        for piece in all_pieces_lst:
                            piece.move_frozen = True
                        pawn = selected_piece_list[0]
                    selected_piece_list[0].move_sound()
                    selected_piece_list.clear()
                    cells_for_move[-1].occupied = False
                    cells_for_move.clear()

                    # move queue change after piece move is completed
                    if promotion_in_process is False:
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

    screen.blit(queue_background, queue_background_rect)
    draw_queue_field(move_queue_list)

    screen.blit(promotion_background, promotion_background_rect)
    promotion_pieces_rects = draw_promotion_field(move_queue_list)

    # Board cells drawing
    screen.blit(board_background, board_background_rect)
    for cell in board:
        cell.cell_draw(board_background)
    # Pieces drawing
    for piece in all_pieces_lst:
        piece.piece_drawing(board_background)

    # SCREEN TURN OVER
    pygame.display.flip()

pygame.quit()