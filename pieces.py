# Source of piece images - https://opengameart.org/content/colorful-chess-pieces, author - Arsonide
import pygame
import os
from board import board, lines_cross_point, dark_color
from colors import *

pygame.init()
# Video mode for image load
pygame.display.set_mode()

# Assign folder with game
game_dir = os.path.dirname(__file__)
# Path to directory with media files
img_dir = os.path.join(game_dir, "img")

# Chess pieces images load
w_bishop = pygame.image.load(os.path.join(img_dir, "w_bishop.png")).convert()
w_king = pygame.image.load(os.path.join(img_dir, "w_king.png")).convert()
w_knight = pygame.image.load(os.path.join(img_dir, "w_knight.png")).convert()
w_pawn = pygame.image.load(os.path.join(img_dir, "w_pawn.png")).convert()
w_queen = pygame.image.load(os.path.join(img_dir, "w_queen.png")).convert()
w_rook = pygame.image.load(os.path.join(img_dir, "w_rook.png")).convert()

b_bishop = pygame.image.load(os.path.join(img_dir, "b_bishop.png")).convert()
b_king = pygame.image.load(os.path.join(img_dir, "b_king.png")).convert()
b_knight = pygame.image.load(os.path.join(img_dir, "b_knight.png")).convert()
b_pawn = pygame.image.load(os.path.join(img_dir, "b_pawn.png")).convert()
b_queen = pygame.image.load(os.path.join(img_dir, "b_queen.png")).convert()
b_rook = pygame.image.load(os.path.join(img_dir, "b_rook.png")).convert()

r_bishop = pygame.image.load(os.path.join(img_dir, "r_bishop.png")).convert()
r_king = pygame.image.load(os.path.join(img_dir, "r_king.png")).convert()
r_knight = pygame.image.load(os.path.join(img_dir, "r_knight.png")).convert()
r_pawn = pygame.image.load(os.path.join(img_dir, "r_pawn.png")).convert()
r_queen = pygame.image.load(os.path.join(img_dir, "r_queen.png")).convert()
r_rook = pygame.image.load(os.path.join(img_dir, "r_rook.png")).convert()


# Piece class (sprite) creation
class Piece(pygame.sprite.Sprite):
    def __init__(self, name: str, color: str, position: list, selection_status: bool, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.color = color
        self.position = position
        self.is_selected = selection_status
        self.image = pygame.transform.scale_by(image, 0.4)
        self.image.set_colorkey(SPECIAL_WHITE)
        self.rect = self.image.get_rect()

    # The method draw price on the chess board
    def piece_drawing(self, surface):
        for cell in board:
            if cell.position == self.position:
                rect_center_coords = lines_cross_point(cell.points[0], cell.points[2], cell.points[1], cell.points[3])
        self.rect.center = rect_center_coords
        surface.blit(self.image, self.rect)

    # The method is overriden in corresponding piece class, it's used for sending a list to method "highlight_cells"
    def possible_moves(self):
        possible_move_cells_list = []
        return possible_move_cells_list

    # The method highlights current cell of selected piece and cells available for move
    def highlight_cells(self):
        cells_to_be_highlighted = self.possible_moves()
        for cell in cells_to_be_highlighted:
            if cell.initial_color == dark_color:
                cell.current_color = GREEN_DARK
            else:
                cell.current_color = GREEN_LIGHT
        return cells_to_be_highlighted

    # The method unhighlights already highlighted cells
    def unhighlight_cells(self):
        for cell in board:
            cell.current_color = cell.initial_color
        return []

    def move_piece(self):
        cells_for_moves = self.possible_moves()


class Bishop(Piece):
    def show_possible_moves(self):
        pass


class King(Piece):
    def show_possible_moves(self):
        pass


class Knight(Piece):
    def show_possible_moves(self):
        pass


class Rook(Piece):
    def show_possible_moves(self):
        pass


class Queen(Rook, Bishop):
    def show_possible_moves(self):
        pass


class Pawn(Piece):
    def possible_moves(self):
        super().possible_moves()
        possible_move_cells_list = []

        # # # # FORWARD MOVES # # # #
        '''
        The function below iterates cells of the board, finds the cell that is next to the cell with corresponding piece
        in such piece move direction and that is not occupied by any other piece. If such cell is found, it's added to 
        "possible_move_cells_list"  
        '''
        def next_cell_check(x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> list:
            for cell in board:
                if cell.position == [self.position[0] * x1 + x2, self.position[1] * y1 + y2,
                                     self.position[2] * z1 + z2] and cell.occupied is False:
                        possible_move_cells_list.append(cell)
            return possible_move_cells_list

        # WHITE PAWNS
        if self.color == "white":
            # possible forward moves of white pawns on start positions (one or two cells forward)
            if self.position[1] == -3 and self.position[2] < 0 or self.position[1] == -3 and self.position[0] > 0:
                for cell in board:
                    if cell.occupied is False and \
                            cell.position == [self.position[0], self.position[1] + 2, self.position[2]]:
                        for nearby_cell in board:
                            if nearby_cell.occupied is True and \
                                    nearby_cell.position == [self.position[0], self.position[1] + 1, self.position[2]]:
                                possible_move_cells_list.clear()
                            elif nearby_cell.occupied is False and \
                                    nearby_cell.position == [self.position[0], self.position[1] + 1, self.position[2]]:
                                possible_move_cells_list.append(cell)
                                if nearby_cell not in possible_move_cells_list:
                                    possible_move_cells_list.append(nearby_cell)
                    elif cell.occupied is False:
                        if cell.position == [self.position[0], self.position[1] + 1, self.position[2]]:
                            if cell not in possible_move_cells_list:
                                possible_move_cells_list.append(cell)

            # possible forward moves of white pawns on the line a3-h3
            elif self.position[1] == -2 and self.position[2] < 0 or self.position[1] == -2 and self.position[0] > 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=0)

            # possible forward moves of white pawns on the line a4-d4
            elif self.position[1] == -1 and self.position[2] < 0:
                next_cell_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=0)

            # possible forward moves of white pawns on the line e4-h4
            elif self.position[1] == -1 and self.position[0] > 0:
                next_cell_check(x1=1, x2=0, y1=0, y2=0, z1=1, z2=1)

            # possible forward moves of white pawns in section a5-d7
            elif -4 < self.position[0] < 0 and self.position[1] == 0 and self.position[2] < 0:
                next_cell_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=0)

            # possible forward moves of white pawns in section e9-h11
            elif self.position[0] > 0 and self.position[1] == 0 and 0 < self.position[2] < 4:
                next_cell_check(x1=1, x2=0, y1=1, y2=0, z1=1, z2=1)

            # possible forward moves of white pawns in section i5-l7
            elif 0 > self.position[0] > -4 and 5 > self.position[1] > 0 and self.position[2] == 0:
                next_cell_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=0)

            # possible forward moves of white pawns in section i9-l11
            elif self.position[0] == 0 and 5 > self.position[1] > 0 and 4 > self.position[2] > 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=0, z1=1, z2=1)


        # BLACK PAWNS
        elif self.color == "black":
            # possible forward moves of black pawns on start positions (one or two cells forward)
            if self.position[0] == -3 and self.position[1] > 0 or self.position[0] == -3 and self.position[2] < 0:
                for cell in board:
                    if cell.occupied is False and \
                            cell.position == [self.position[0] + 2, self.position[1], self.position[2]]:
                        for nearby_cell in board:
                            if nearby_cell.occupied is True and \
                                    nearby_cell.position == [self.position[0] + 1, self.position[1], self.position[2]]:
                                possible_move_cells_list.clear()
                            elif nearby_cell.occupied is False and \
                                    nearby_cell.position == [self.position[0] + 1, self.position[1], self.position[2]]:
                                possible_move_cells_list.append(cell)
                                if nearby_cell not in possible_move_cells_list:
                                    possible_move_cells_list.append(nearby_cell)
                    elif cell.occupied is False:
                        if cell.position == [self.position[0] + 1, self.position[1], self.position[2]]:
                            if cell not in possible_move_cells_list:
                                possible_move_cells_list.append(cell)

            # possible forward moves of black pawns on the line a6-l6
            elif self.position[0] == -2 and self.position[1] > 0 or self.position[0] == -2 and self.position[2] < 0:
                next_cell_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=0)

            # possible forward moves of black pawns on the line l5-i5
            elif self.position[0] == -1 and self.position[1] > 0:
                next_cell_check(x1=0, x2=0, y1=1, y2=0, z1=1, z2=1)

            # possible forward moves of black pawns on the line d5-a5
            elif self.position[0] == -1 and self.position[2] < 0:
                next_cell_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=0)

            # possible forward moves of black pawns in section l9-i11
            elif self.position[0] == 0 and 0 < self.position[1] < 5 and self.position[2] > 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=0, z1=1, z2=1)

            # possible forward moves of black pawns in section a4-d2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and self.position[2] < 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=0)

            # possible forward moves of black pawns in section e9-h11
            elif 5 > self.position[0] > 0 and self.position[1] == 0 and 4 > self.position[2] > 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=0, z1=1, z2=1)

            # possible forward moves of black pawns in section e4-h2
            elif 0 < self.position[0] < 5 and 0 > self.position[1] > -4 and self.position[2] == 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=0)


        # RED PAWNS
        elif self.color == "red":
            # possible forward moves of red pawns on start positions (one or two cells forward)
            if self.position[2] == 3 and self.position[0] > 0 or self.position[2] == 3 and self.position[1] > 0:
                for cell in board:
                    if cell.occupied is False and \
                            cell.position == [self.position[0], self.position[1], self.position[2] - 2]:
                        for nearby_cell in board:
                            if nearby_cell.occupied is True and \
                                    nearby_cell.position == [self.position[0], self.position[1], self.position[2] - 1]:
                                possible_move_cells_list.clear()
                            elif nearby_cell.occupied is False and \
                                    nearby_cell.position == [self.position[0], self.position[1], self.position[2] - 1]:
                                possible_move_cells_list.append(cell)
                                if nearby_cell not in possible_move_cells_list:
                                    possible_move_cells_list.append(nearby_cell)
                    elif cell.occupied is False:
                        if cell.position == [self.position[0], self.position[1], self.position[2] - 1]:
                            if cell not in possible_move_cells_list:
                                possible_move_cells_list.append(cell)

            # possible forward moves of red pawns on the line h10-l10
            elif self.position[0] > 0 and self.position[2] == 2 or self.position[1] > 0 and self.position[2] == 2:
                next_cell_check(x1=1, x2=0, y1=1, y2=0, z1=1, z2=-1)

            # possible forward moves of red pawns on the line h9-e9
            elif self.position[0] > 0 and self.position[2] == 1:
                next_cell_check(x1=1, x2=0, y1=1, y2=-1, z1=0, z2=0)

            # possible forward moves of red pawns on the line i9-l9
            elif self.position[1] > 0 and self.position[2] == 1:
                next_cell_check(x1=1, x2=-1, y1=1, y2=0, z1=0, z2=0)

            # possible forward moves of red pawns in section h4-e2
            elif self.position[0] > 0 and 0 > self.position[1] > -4 and self.position[2] == 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=0)

            # possible forward moves of red pawns in section i5-l7
            elif 0 > self.position[0] > -4 and self.position[1] > 0 and self.position[2] == 0:
                next_cell_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=0)

            # possible forward moves of red pawns in section d4-a2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and 0 > self.position[2] > -5:
                next_cell_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=0)

            # possible forward moves of red pawns in section d5-a7
            elif 0 > self.position[0] > -4 and self.position[1] == 0 and 0 > self.position[2] > -5:
                next_cell_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=0)


        # # # # CAPTURE MOVES # # # #
        '''
        The function below iterates cells of the board, finds the cells that are next by diagonal to the cell with 
        corresponding piece in such piece move direction and that are occupied by enemy piece. If such cells are found,
        they are added to "possible_move_cells_list"  
        '''
        def next_diagonal_cells_check(x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> list:
            for cell in board:
                if cell.position == [self.position[0] * x1 + x2, self.position[1] * y1 + y2,
                                     self.position[2] * z1 + z2] and cell.occupied is True:
                    for enemy_piece in all_pieces_lst:
                        if enemy_piece.position == [self.position[0] * x1 + x2, self.position[1] * y1 + y2,
                                                    self.position[2] * z1 + z2] and enemy_piece.color != self.color:
                            possible_move_cells_list.append(cell)
            return possible_move_cells_list


        # WHITE PAWNS
        if self.color == "white":
            # possible capture moves of white pawns in section a2-c3
            if self.position[0] == 0 and -4 < self.position[1] < -1 and -5 < self.position[2] < -1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=-1)

            # possible capture moves of white pawns in section f2-h3
            elif 5 > self.position[0] > 1 and -1 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=1, z2=0)

            # possible capture moves of white pawns in section d2-d3
            elif self.position[0] == 0 and -1 > self.position[1] > -4 and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)

            # possible capture moves of white pawns in section e2-e3
            elif self.position[0] == 1 and -1 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=-1)

            # possible capture moves of white pawns in section a4-c4
            elif self.position[0] == 0 and self.position[1] == -1 and -1 > self.position[2] > -5:
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of white pawns in section f4-h4
            elif 5 > self.position[0] > 1 and self.position[1] == -1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of white pawns in cell d4
            elif self.position == [0, -1, -1]:
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=2, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=2)

            # possible capture moves of white pawns in cell e4
            elif self.position == [1, -1, 0]:
                next_diagonal_cells_check(x1=1, x2=-2, y1=0, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=2, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of white pawns in section a5-c7
            elif 0 > self.position[0] > -4 and self.position[1] == 0 and -1 > self.position[2] > -5:
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of white pawns in section d5-d7
            elif 0 > self.position[0] > -4 and self.position[1] == 0 and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=0, z2=0)

            # possible capture moves of white pawns in section h11-f9
            elif 5 > self.position[0] > 1 and self.position[1] == 0 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of white pawns in section e11-e9
            elif self.position[0] == 1 and self.position[1] == 0 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)

            # possible capture moves of white pawns in section i5-i7
            elif 0 > self.position[0] > -4 and self.position[1] == 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of white pawns in section j5-l7
            elif 0 > self.position[0] > -4 and 5 > self.position[1] > 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=1, z2=0)

            # possible capture moves of white pawns in section i9-i11
            elif self.position[0] == 0 and self.position[1] == 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of white pawns in section j9-l11
            elif self.position[0] == 0 and 5 > self.position[1] > 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=1)


        # BLACK PAWNS
        if self.color == "black":
            # possible capture moves of black pawns in section l7-j6
            if -1 > self.position[0] > -4 and 5 > self.position[1] > 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=1, y1=-1, y2=1, z1=0, z2=0)

            # possible capture moves of black pawns in section a7-c6
            elif -1 > self.position[0] > -4 and self.position[1] == 0 and -1 > self.position[2] > -5:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=-1)

            # possible capture moves of black pawns in section i7-i6
            elif -1 > self.position[0] > -4 and self.position[1] == 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of black pawns in section d7-d6
            elif -1 > self.position[0] > -4 and self.position[1] == 0 and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)

            # possible capture moves of black pawns in section l5-j5
            elif self.position[0] == -1 and 5 > self.position[1] > 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=1)

            # possible capture moves of black pawns in section a5-c5
            elif self.position[0] == -1 and self.position[1] == 0 and -1 > self.position[2] > -5:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of black pawns in cell i5
            elif self.position == [-1, 1, 0]:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=2, y1=0, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-2, z1=1, z2=-1)

            # possible capture moves of black pawns in cell d5
            elif self.position == [-1, 0, -1]:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=2)
                next_diagonal_cells_check(x1=1, x2=2, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of black pawns in section l9-j11
            elif self.position[0] == 0 and 5 > self.position[1] > 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=1)

            # possible capture moves of black pawns in section i9-i11
            elif self.position[0] == 0 and self.position[1] == 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of black pawns in section c4-a2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and -1 > self.position[2] > -5:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of black pawns in section d4-d2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of black pawns in section e9-e11
            elif self.position[0] == 1 and self.position[1] == 0 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)

            # possible capture moves of black pawns in section f9-H11
            elif 5 > self.position[0] > 1 and self.position[1] == 0 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=1)

            # possible capture moves of black pawns in section e4-e2
            elif self.position[0] == 1 and 0 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=1, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of black pawns in section f4-h2
            elif 5 > self.position[0] > 1 and 0 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=1, z2=0)


        # RED PAWNS
        if self.color == "red":
            # possible capture moves of red pawns in section h11-f10
            if 5 > self.position[0] > 1 and self.position[1] == 0 and 4 > self.position[2] > 1:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=-1)

            # possible capture moves of red pawns in section l11-j10
            elif self.position[0] == 0 and 5 > self.position[1] > 1 and 4 > self.position[2] > 1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of red pawns in section e11-e10
            elif self.position[0] == 1 and self.position[1] == 0 and 4 > self.position[2] > 1:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=-1)

            # possible capture moves of red pawns in section i11-i10
            elif self.position[0] == 0 and self.position[1] == 1 and 4 > self.position[2] > 1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of red pawns in section h9-f9
            elif 5 > self.position[0] > 1 and self.position[1] == 0 and self.position[2] == 1:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section j9-l9
            elif self.position[0] == 0 and 5 > self.position[1] > 1 and self.position[2] == 1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in cell e9
            elif self.position == [1, 0, 1]:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=-2)
                next_diagonal_cells_check(x1=1, x2=-2, y1=1, y2=1, z1=0, z2=0)

            # possible capture moves of red pawns in cell i9
            elif self.position == [0, 1, 1]:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-2, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-2)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=0, z2=0)

            # possible capture moves of red pawns in section h4-f2
            elif 5 > self.position[0] > 1 and 0 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section e4-e2
            elif self.position[0] == 1 and 0 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of red pawns in section l5-j7
            elif 0 > self.position[0] > -4 and 5 > self.position[1] > 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section i5-i7
            elif 0 > self.position[0] > -4 and self.position[1] == 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of red pawns in section d4-d2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section c4-a2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and -1 > self.position[2] > -5:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=1)

            # possible capture moves of red pawns in section i5-i7
            elif 0 > self.position[0] > -4 and self.position[1] == 0 and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=1, z1=0, z2=0)

            # possible capture moves of red pawns in section d5-a7
            elif 0 > self.position[0] > -4 and self.position[1] == 0 and -1 > self.position[2] > -5:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=1)


        # Adding piece's current position cell into the list in order to highlight cells when piece is selected
        for cell in board:
            if self.position == cell.position:
                possible_move_cells_list.append(cell)

        # Return list of cells available for move + current cell
        return possible_move_cells_list


# Creation of Piece objects
white_left_rook = Rook("w_l_Rook", "white", [0, -4, -4], False, w_rook)
white_left_knight = Knight("w_l_Knight", "white", [0, -4, -3], False, w_knight)
white_left_bishop = Bishop("w_l_Bishop", "white", [0, -4, -2], False, w_bishop)
white_queen = Queen("w_Queen", "white", [0, -4, -1], False, w_queen)
white_king = King("w_King", "white", [1, -4, 0], False, w_king)
white_right_bishop = Bishop("w_r_Bishop", "white", [2, -4, 0], False, w_bishop)
white_right_knight = Knight("w_r_Knight", "white", [3, -4, 0], False, w_knight)
white_right_rook = Rook("w_r_Rook", "white", [4, -4, 0], False, w_rook)
white_pawn1 = Pawn("w_1_Pawn", "white", [0, -3, -4], False, w_pawn)
white_pawn2 = Pawn("w_2_Pawn", "white", [0, -3, -3], False, w_pawn)
white_pawn3 = Pawn("w_3_Pawn", "white", [0, -3, -2], False, w_pawn)
white_pawn4 = Pawn("w_4_Pawn", "white", [0, -3, -1], False, w_pawn)
white_pawn5 = Pawn("w_5_Pawn", "white", [1, -3, 0], False, w_pawn)
white_pawn6 = Pawn("w_6_Pawn", "white", [2, -3, 0], False, w_pawn)
white_pawn7 = Pawn("w_7_Pawn", "white", [3, -3, 0], False, w_pawn)
white_pawn8 = Pawn("w_8_Pawn", "white", [4, -3, 0], False, w_pawn)

black_left_rook = Rook("b_l_Rook", "black", [-4, 4, 0], False, b_rook)
black_left_knight = Knight("b_l_Knight", "black", [-4, 3, 0], False, b_knight)
black_left_bishop = Bishop("b_l_Bishop", "black", [-4, 2, 0], False, b_bishop)
black_queen = Queen("b_Queen", "black", [-4, 1, 0], False, b_queen)
black_king = King("b_King", "black", [-4, 0, -1], False, b_king)
black_right_bishop = Bishop("b_r_Bishop", "black", [-4, 0, -2], False, b_bishop)
black_right_knight = Knight("b_r_Knight", "black", [-4, 0, -3], False, b_knight)
black_right_rook = Rook("b_r_Rook", "black", [-4, 0, -4], False, b_rook)
black_pawn1 = Pawn("b_1_Pawn", "black", [-3, 4, 0], False, b_pawn)
black_pawn2 = Pawn("b_2_Pawn", "black", [-3, 3, 0], False, b_pawn)
black_pawn3 = Pawn("b_3_Pawn", "black", [-3, 2, 0], False, b_pawn)
black_pawn4 = Pawn("b_4_Pawn", "black", [-3, 1, 0], False, b_pawn)
black_pawn5 = Pawn("b_5_Pawn", "black", [-3, 0, -1], False, b_pawn)
black_pawn6 = Pawn("b_6_Pawn", "black", [-3, 0, -2], False, b_pawn)
black_pawn7 = Pawn("b_7_Pawn", "black", [-3, 0, -3], False, b_pawn)
black_pawn8 = Pawn("b_8_Pawn", "black", [-3, 0, -4], False, b_pawn)

red_left_rook = Rook("r_l_Rook", "red", [4, 0, 4], False, r_rook)
red_left_knight = Knight("r_l_Knight", "red", [3, 0, 4], False, r_knight)
red_left_bishop = Bishop("r_l_Bishop", "red", [2, 0, 4], False, r_bishop)
red_queen = Queen("r_Queen", "red", [1, 0, 4], False, r_queen)
red_king = King("r_King", "red", [0, 1, 4], False, r_king)
red_right_bishop = Bishop("r_r_Bishop", "red", [0, 2, 4], False, r_bishop)
red_right_knight = Knight("r_r_Knight", "red", [0, 3, 4], False, r_knight)
red_right_rook = Rook("r_r_Rook", "red", [0, 4, 4], False, r_rook)
red_pawn1 = Pawn("r_1_Pawn", "red", [4, 0, 3], False, r_pawn)
red_pawn2 = Pawn("r_2_Pawn", "red", [3, 0, 3], False, r_pawn)
red_pawn3 = Pawn("r_3_Pawn", "red", [2, 0, 3], False, r_pawn)
red_pawn4 = Pawn("r_4_Pawn", "red", [1, 0, 3], False, r_pawn)
red_pawn5 = Pawn("r_5_Pawn", "red", [0, 1, 3], False, r_pawn)
red_pawn6 = Pawn("r_6_Pawn", "red", [0, 2, 3], False, r_pawn)
red_pawn7 = Pawn("r_7_Pawn", "red", [0, 3, 3], False, r_pawn)
red_pawn8 = Pawn("r_8_Pawn", "red", [0, 4, 3], False, r_pawn)

# Creation of all pieces list (iterable)
all_pieces_lst = [
    white_left_rook, white_left_knight, white_left_bishop, white_queen, white_king, white_right_bishop,
    white_right_knight, white_right_rook, white_pawn1, white_pawn2, white_pawn3, white_pawn4, white_pawn5, white_pawn6,
    white_pawn7, white_pawn8,

    black_left_rook, black_left_knight, black_left_bishop, black_queen, black_king, black_right_bishop,
    black_right_knight, black_right_rook, black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6,
    black_pawn7, black_pawn8,

    red_left_rook, red_left_knight, red_left_bishop, red_queen, red_king, red_right_bishop, red_right_knight,
    red_right_rook, red_pawn1, red_pawn2, red_pawn3, red_pawn4, red_pawn5, red_pawn6, red_pawn7, red_pawn8
]

# Creation of sprites group (not iterable) that contains piece sprites
all_pieces = pygame.sprite.Group
for piece in all_pieces_lst:
    all_pieces.add(piece)