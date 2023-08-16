# Source of piece images - https://opengameart.org/content/colorful-chess-pieces, author - Arsonide
import pygame
import os
from board import board, lines_cross_point, dark_color, light_color
from colors import *
import random

pygame.init()
# Video mode for image load
pygame.display.set_mode((1400, 800))

# Assign folder with game
game_dir = os.path.dirname(__file__)
# Path to directory with media files
img_dir = os.path.join(game_dir, "img")
snd_dir = os.path.join(game_dir, "snd")

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

g_king = pygame.image.load(os.path.join(img_dir, "g_king.png")).convert()

kings_images = [w_king, b_king, r_king, g_king]

promotion_images = {}
promotion_images["white"] = [w_queen, w_rook, w_bishop, w_knight]
promotion_images["black"] = [b_queen, b_rook, b_bishop, b_knight]
promotion_images["red"] = [r_queen, r_rook, r_bishop, r_knight]


# Piece class (sprite) creation
class Piece(pygame.sprite.Sprite):
    def __init__(self, name: str, color: str, position: list, selection_status: bool, first_move_status: bool,
                 freezing_status: bool, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.color = color
        self.position = position
        self.is_selected = selection_status
        self.first_move = first_move_status
        self.move_frozen = freezing_status
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

    # The method records sound of piece move
    def move_sound(self):
        pygame.mixer.Sound(os.path.join(snd_dir, random.choice(['Sound1.wav', 'Sound2.wav', 'Sound3.wav']))).play()



class Bishop(Piece):
    def bishop_possible_moves(self):
        super().possible_moves()
        possible_move_cells_list = []
        up_right_diagonal = []
        up_left_diagonal = []
        down_right_diagonal = []
        down_left_diagonal = []

        """
        The function below receives a list of cells (diagonal of cells) and checks cells in the list on the following:
        - whether a cell is occupied by another piece or not,
        - if occupied, whether cell is occupied by own piece or by enemy piece.
        The list of possible moves is formed based on results of cheking 
        """

        def move_cells_check(list_of_cells: list) -> list:
            list_to_be_returned = []
            for cell in list_of_cells:
                if cell.occupied is False and cell not in possible_move_cells_list:
                    list_to_be_returned.append(cell)
                elif cell.occupied is True and cell not in possible_move_cells_list:
                    for piece in all_pieces_lst:
                        if piece.position == cell.position and piece.color == self.color:
                            pass
                        elif piece.position == cell.position and piece.color != self.color:
                            list_to_be_returned.append(cell)
                    break
            return list_to_be_returned

        '''
        Search for possible moves relatively axis X. 
        Below specified cells must not be taken into consideration, otherwise the method works not in proper way
        '''
        line_perpendicular_to_axis_x = []
        if 5 > self.position[0] > -5 and self.position[0] != 0 and self.position not in [
            [-3, 4, 0], [-2, 4, 0], [-1, 4, 0], [-2, 3, 0], [-1, 3, 0], [-1, 2, 0],
            [-3, 0, -4], [-2, 0, -4], [-1, 0, -4], [-2, 0, -3], [-1, 0, -3], [-1, 0, -2],
            [3, -4, 0], [2, -4, 0], [1, -4, 0], [2, -3, 0], [1, -3, 0], [1, -2, 0],
            [3, 0, 4], [2, 0, 4], [1, 0, 4], [2, 0, 3], [1, 0, 3], [1, 0, 2]
        ]:
            # collecting cells in line that includes cell with selected piece and that is perpendicular to axis X
            for cell in board:
                if cell.position[0] == self.position[0]:
                    line_perpendicular_to_axis_x.append(cell)

            # sorting of cell in "line_perpendicular_to_axis_x"
            line_perpendicular_to_axis_x = sorted(line_perpendicular_to_axis_x,
                                                  key=lambda a_cell: a_cell.position[2]
                                                  if a_cell.position[2] != 0 else a_cell.position[1])[::-1]

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_x"
            for cell in line_perpendicular_to_axis_x:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_x.index(cell)

            line_parallel_to_axis_x = []
            counter = 0

            if selected_cell_index != 7:
                for a_cell in line_perpendicular_to_axis_x[selected_cell_index + 1: 8]:
                    counter += 1
                    if a_cell.position[1] == 0:
                        for cell in board:
                            if cell.position[2] == a_cell.position[2]:
                                line_parallel_to_axis_x.append(cell)

                        if a_cell.position[2] == -3 or a_cell.position[2] == -1:
                            line_parallel_to_axis_x = sorted(line_parallel_to_axis_x,
                                                             key=lambda a__cell: a__cell.position[0])
                        else:
                            line_parallel_to_axis_x = line_parallel_to_axis_x[::-1]

                        for the_cell in line_parallel_to_axis_x:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_x.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_right_diagonal.append(line_parallel_to_axis_x[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_right_diagonal.append(line_parallel_to_axis_x[the_cell_index - counter])

                    elif a_cell.position[2] == 0:
                        for cell in board:
                            if cell.position[1] == a_cell.position[1]:
                                line_parallel_to_axis_x.append(cell)

                        line_parallel_to_axis_x = sorted(line_parallel_to_axis_x,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[0])

                        for the_cell in line_parallel_to_axis_x:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_x.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_right_diagonal.append(line_parallel_to_axis_x[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_right_diagonal.append(line_parallel_to_axis_x[the_cell_index - counter])

                    line_parallel_to_axis_x.clear()

            counter = 0
            if selected_cell_index != 0:
                for a_cell in line_perpendicular_to_axis_x[selected_cell_index - 1:: -1]:
                    counter += 1
                    if a_cell.position[1] == 0:
                        for cell in board:
                            if cell.position[2] == a_cell.position[2]:
                                line_parallel_to_axis_x.append(cell)

                        if a_cell.position[2] == -3 or a_cell.position[2] == -1:
                            line_parallel_to_axis_x = sorted(line_parallel_to_axis_x,
                                                             key=lambda a__cell: a__cell.position[0])
                        else:
                            line_parallel_to_axis_x = line_parallel_to_axis_x[::-1]

                        for the_cell in line_parallel_to_axis_x:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_x.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_left_diagonal.append(line_parallel_to_axis_x[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_left_diagonal.append(line_parallel_to_axis_x[the_cell_index - counter])

                    elif a_cell.position[2] == 0:
                        for cell in board:
                            if cell.position[1] == a_cell.position[1]:
                                line_parallel_to_axis_x.append(cell)

                        line_parallel_to_axis_x = sorted(line_parallel_to_axis_x,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[0])

                        for the_cell in line_parallel_to_axis_x:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_x.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_left_diagonal.append(line_parallel_to_axis_x[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_left_diagonal.append(line_parallel_to_axis_x[the_cell_index - counter])

                    line_parallel_to_axis_x.clear()

        possible_move_cells_list.extend(move_cells_check(up_right_diagonal))
        up_right_diagonal.clear()

        possible_move_cells_list.extend(move_cells_check(up_left_diagonal))
        up_left_diagonal.clear()

        possible_move_cells_list.extend(move_cells_check(down_right_diagonal))
        down_right_diagonal.clear()

        possible_move_cells_list.extend(move_cells_check(down_left_diagonal))
        down_left_diagonal.clear()

        '''
        Search for possible moves relatively axis Y. 
        Below specified cells must not be taken into consideration, otherwise the method works not in proper way
        '''
        line_perpendicular_to_axis_y = []
        if 5 > self.position[1] > -5 and self.position[1] != 0 and self.position not in [
            [4, -3, 0], [4, -2, 0], [4, -1, 0], [3, -2, 0], [3, -1, 0], [2, -1, 0],
            [0, -3, -4], [0, -2, -4], [0, -1, -4], [0, -2, -3], [0, -1, -3], [0, -1, -2],
            [-4, 3, 0], [-4, 2, 0], [-4, 1, 0], [-3, 2, 0], [-3, 1, 0], [-2, 1, 0],
            [0, 3, 4], [0, 2, 4], [0, 1, 4], [0, 2, 3], [0, 1, 3], [0, 1, 2]
        ]:
            # collecting cells in line that includes cell with selected piece and that is perpendicular to axis Y
            for cell in board:
                if cell.position[1] == self.position[1]:
                    line_perpendicular_to_axis_y.append(cell)

            # sorting of cell in "line_perpendicular_to_axis_y"
            line_perpendicular_to_axis_y = sorted(line_perpendicular_to_axis_y,
                                                  key=lambda a_cell: a_cell.position[2]
                                                  if a_cell.position[2] != 0 else a_cell.position[0])

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_y"
            for cell in line_perpendicular_to_axis_y:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_y.index(cell)

            line_parallel_to_axis_y = []
            counter = 0

            if selected_cell_index != 7:
                for a_cell in line_perpendicular_to_axis_y[selected_cell_index + 1: 8]:
                    counter += 1
                    if a_cell.position[0] == 0:
                        for cell in board:
                            if cell.position[2] == a_cell.position[2]:
                                line_parallel_to_axis_y.append(cell)

                        if a_cell.position[2] == -3 or a_cell.position[2] == -1:
                            line_parallel_to_axis_y = sorted(line_parallel_to_axis_y,
                                                             key=lambda a__cell: a__cell.position[0])[::-1]

                        for the_cell in line_parallel_to_axis_y:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_y.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_right_diagonal.append(line_parallel_to_axis_y[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_right_diagonal.append(line_parallel_to_axis_y[the_cell_index - counter])

                    elif a_cell.position[2] == 0:
                        for cell in board:
                            if cell.position[0] == a_cell.position[0]:
                                line_parallel_to_axis_y.append(cell)

                        line_parallel_to_axis_y = sorted(line_parallel_to_axis_y,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[1])

                        for the_cell in line_parallel_to_axis_y:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_y.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_right_diagonal.append(line_parallel_to_axis_y[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_right_diagonal.append(line_parallel_to_axis_y[the_cell_index - counter])

                    line_parallel_to_axis_y.clear()

            counter = 0
            if selected_cell_index != 0:
                for a_cell in line_perpendicular_to_axis_y[selected_cell_index - 1:: -1]:
                    counter += 1
                    if a_cell.position[0] == 0:
                        for cell in board:
                            if cell.position[2] == a_cell.position[2]:
                                line_parallel_to_axis_y.append(cell)

                        if a_cell.position[2] == -3 or a_cell.position[2] == -1:
                            line_parallel_to_axis_y = sorted(line_parallel_to_axis_y,
                                                             key=lambda a__cell: a__cell.position[0])[::-1]

                        for the_cell in line_parallel_to_axis_y:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_y.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_left_diagonal.append(line_parallel_to_axis_y[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_left_diagonal.append(line_parallel_to_axis_y[the_cell_index - counter])

                    elif a_cell.position[2] == 0:
                        for cell in board:
                            if cell.position[0] == a_cell.position[0]:
                                line_parallel_to_axis_y.append(cell)

                        line_parallel_to_axis_y = sorted(line_parallel_to_axis_y,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[1])

                        for the_cell in line_parallel_to_axis_y:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_y.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_left_diagonal.append(line_parallel_to_axis_y[the_cell_index + counter])

                        if the_cell_index - counter >= 0:
                            down_left_diagonal.append(line_parallel_to_axis_y[the_cell_index - counter])

                    line_parallel_to_axis_y.clear()

        possible_move_cells_list.extend(move_cells_check(up_right_diagonal))
        up_right_diagonal.clear()

        possible_move_cells_list.extend(move_cells_check(up_left_diagonal))
        up_left_diagonal.clear()

        possible_move_cells_list.extend(move_cells_check(down_right_diagonal))
        down_right_diagonal.clear()

        possible_move_cells_list.extend(move_cells_check(down_left_diagonal))
        down_left_diagonal.clear()

        '''
        Search for possible moves relatively axis Z. 
        Below specified cells must not be taken into consideration, otherwise the method works not in proper way
        '''
        line_perpendicular_to_axis_z = []
        if 5 > self.position[2] > -5 and self.position[2] != 0 and self.position not in [
            [-4, 0, -3], [-4, 0, -2], [-4, 0, -1], [-3, 0, -2], [-3, 0, -1], [-2, 0, -1],
            [0, -4, -3], [0, -4, -2], [0, -4, -1], [0, -3, -2], [0, -3, -1], [0, -2, -1],
            [4, 0, 3], [4, 0, 2], [4, 0, 1], [3, 0, 2], [3, 0, 1], [2, 0, 1],
            [0, 4, 3], [0, 4, 2], [0, 4, 1], [0, 3, 2], [0, 3, 1], [0, 2, 1]
        ]:
            # collecting cells in line that includes cell with selected piece and that is perpendicular to axis Z
            for cell in board:
                if cell.position[2] == self.position[2]:
                    line_perpendicular_to_axis_z.append(cell)

            # sorting of cell in "line_perpendicular_to_axis_z"
            if self.position[2] == -3 or self.position[2] == -1:
                line_perpendicular_to_axis_z = sorted(line_perpendicular_to_axis_z,
                                                      key=lambda a_cell: a_cell.position[0])
            else:
                line_perpendicular_to_axis_z = line_perpendicular_to_axis_z[::-1]

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_z"
            for cell in line_perpendicular_to_axis_z:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_z.index(cell)

            line_parallel_to_axis_z = []
            counter = 0

            if selected_cell_index != 7:
                for a_cell in line_perpendicular_to_axis_z[selected_cell_index + 1: 8]:
                    counter += 1
                    if a_cell.position[0] == 0:
                        for cell in board:
                            if cell.position[1] == a_cell.position[1]:
                                line_parallel_to_axis_z.append(cell)

                        line_parallel_to_axis_z = sorted(line_parallel_to_axis_z,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[0])

                        for the_cell in line_parallel_to_axis_z:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_z.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_right_diagonal.append(line_parallel_to_axis_z[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_right_diagonal.append(line_parallel_to_axis_z[the_cell_index - counter])

                    elif a_cell.position[1] == 0:
                        for cell in board:
                            if cell.position[0] == a_cell.position[0]:
                                line_parallel_to_axis_z.append(cell)

                        line_parallel_to_axis_z = sorted(line_parallel_to_axis_z,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[1])

                        for the_cell in line_parallel_to_axis_z:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_z.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_right_diagonal.append(line_parallel_to_axis_z[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_right_diagonal.append(line_parallel_to_axis_z[the_cell_index - counter])

                    line_parallel_to_axis_z.clear()

            counter = 0
            if selected_cell_index != 0:
                for a_cell in line_perpendicular_to_axis_z[selected_cell_index - 1:: -1]:
                    counter += 1
                    if a_cell.position[0] == 0:
                        for cell in board:
                            if cell.position[1] == a_cell.position[1]:
                                line_parallel_to_axis_z.append(cell)

                        line_parallel_to_axis_z = sorted(line_parallel_to_axis_z,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[0])

                        for the_cell in line_parallel_to_axis_z:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_z.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_left_diagonal.append(line_parallel_to_axis_z[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_left_diagonal.append(line_parallel_to_axis_z[the_cell_index - counter])

                    elif a_cell.position[1] == 0:
                        for cell in board:
                            if cell.position[0] == a_cell.position[0]:
                                line_parallel_to_axis_z.append(cell)

                        line_parallel_to_axis_z = sorted(line_parallel_to_axis_z,
                                                         key=lambda a__cell: a__cell.position[2]
                                                         if a__cell.position[2] != 0 else a__cell.position[1])

                        for the_cell in line_parallel_to_axis_z:
                            if the_cell.position == a_cell.position:
                                the_cell_index = line_parallel_to_axis_z.index(the_cell)

                        if the_cell_index + counter < 8:
                            up_left_diagonal.append(line_parallel_to_axis_z[the_cell_index + counter])
                        if the_cell_index - counter >= 0:
                            down_left_diagonal.append(line_parallel_to_axis_z[the_cell_index - counter])

                    line_parallel_to_axis_z.clear()

        possible_move_cells_list.extend(move_cells_check(up_right_diagonal))

        possible_move_cells_list.extend(move_cells_check(up_left_diagonal))

        possible_move_cells_list.extend(move_cells_check(down_right_diagonal))

        possible_move_cells_list.extend(move_cells_check(down_left_diagonal))

        # Adding piece's current position cell into the list in order to highlight cells when piece is selected
        for cell in board:
            if self.position == cell.position:
                possible_move_cells_list.append(cell)

        # Return list of cells available for move + current cell
        return possible_move_cells_list

    def highlight_cells(self):
        super().highlight_cells()
        cells_to_be_highlighted = self.bishop_possible_moves()
        for cell in cells_to_be_highlighted:
            if cell.initial_color == dark_color:
                cell.current_color = GREEN_DARK
            else:
                cell.current_color = GREEN_LIGHT
        return cells_to_be_highlighted


class King(Piece):
    def castling(self):
        dict_to_be_returned = {}
        # white king
        if self.color == "white" and self.first_move is True:
            for piece in all_pieces_lst:
                if piece.name == "w_r_Rook":
                    right_rook = piece
                if piece.name == "w_l_Rook":
                    left_rook = piece
            for cell in board:
                if cell.name == "f1":
                    f1 = cell
                if cell.name == "g1":
                    g1 = cell
                if cell.name == "b1":
                    b1 = cell
                if cell.name == "c1":
                    c1 = cell
                if cell.name == "d1":
                    d1 = cell
                if cell.name == "h1":
                    h1 = cell
                if cell.name == "a1":
                    a1 = cell
            if right_rook.first_move is True and f1.occupied is False and g1.occupied is False:
                dict_to_be_returned[g1] = [right_rook, h1, f1]
            if left_rook.first_move is True and b1.occupied is False and c1.occupied is False and d1.occupied is False:
                dict_to_be_returned[c1] = [left_rook, a1, d1]

        # black king
        if self.color == "black" and self.first_move is True:
            for piece in all_pieces_lst:
                if piece.name == "b_r_Rook":
                    right_rook = piece
                if piece.name == "b_l_Rook":
                    left_rook = piece
            for cell in board:
                if cell.name == "c8":
                    c8 = cell
                if cell.name == "b8":
                    b8 = cell
                if cell.name == "k8":
                    k8 = cell
                if cell.name == "j8":
                    j8 = cell
                if cell.name == "i8":
                    i8 = cell
                if cell.name == "a8":
                    a8 = cell
                if cell.name == "l8":
                    l8 = cell
            if right_rook.first_move is True and c8.occupied is False and b8.occupied is False:
                dict_to_be_returned[b8] = [right_rook, a8, c8]
            if left_rook.first_move is True and k8.occupied is False and j8.occupied is False and i8.occupied is False:
                dict_to_be_returned[j8] = [left_rook, l8, i8]

        # red king
        if self.color == "red" and self.first_move is True:
            for piece in all_pieces_lst:
                if piece.name == "r_r_Rook":
                    right_rook = piece
                if piece.name == "r_l_Rook":
                    left_rook = piece
            for cell in board:
                if cell.name == "j12":
                    j12 = cell
                if cell.name == "k12":
                    k12 = cell
                if cell.name == "g12":
                    g12 = cell
                if cell.name == "f12":
                    f12 = cell
                if cell.name == "e12":
                    e12 = cell
                if cell.name == "l12":
                    l12 = cell
                if cell.name == "h12":
                    h12 = cell
            if right_rook.first_move is True and j12.occupied is False and k12.occupied is False:
                dict_to_be_returned[k12] = [right_rook, l12, j12]
            if left_rook.first_move is True and g12.occupied is False and f12.occupied is False and \
                    e12.occupied is False:
                dict_to_be_returned[f12] = [left_rook, h12, e12]

        return dict_to_be_returned

    def possible_moves(self):
        super().possible_moves()
        possible_move_cells_list = []
        move_cells_to_be_checked = []

        def move_cells_check(cells_list: list):
            """
            The function receives a list of cells and checks cells in the list on the following:
            - whether a cell is occupied by another piece or not,
            - if occupied, whether cell is occupied by own piece or by enemy piece.
            The list of possible moves is formed based on results of checking
            """
            for cell in cells_list:
                if cell.occupied is False and cell not in possible_move_cells_list:
                    possible_move_cells_list.append(cell)
                elif cell.occupied is True and cell not in possible_move_cells_list:
                    for piece in all_pieces_lst:
                        if piece.position == cell.position and piece.color != self.color:
                            possible_move_cells_list.append(cell)

        # search for possible moves relatively axis X
        line_perpendicular_to_axis_x = []
        if 5 > self.position[0] > -5 and self.position[0] != 0:
            for cell in board:
                if cell.position[0] == self.position[0]:
                    line_perpendicular_to_axis_x.append(cell)

            # sorting cells in "line_perpendicular_to_axis_x"
            line_perpendicular_to_axis_x = sorted(line_perpendicular_to_axis_x,
                                                  key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0
                                                  else a_cell.position[1])

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_x"
            for cell in line_perpendicular_to_axis_x:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_x.index(cell)
                    selected_cell = cell

            # cell above and cell below the cell with selected king
            center_line_parallel_to_axis_x = []
            if selected_cell.position[1] == 0:
                for cell in board:
                    if cell.position[2] == selected_cell.position[2]:
                        center_line_parallel_to_axis_x.append(cell)

                if selected_cell.position[2] == -3 or selected_cell.position[2] == -1:
                    center_line_parallel_to_axis_x = sorted(center_line_parallel_to_axis_x,
                                                            key=lambda a__cell: a__cell.position[0])[::-1]

                the_selected_cell_index = center_line_parallel_to_axis_x.index(selected_cell)

                if the_selected_cell_index + 1 < 8:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_x[the_selected_cell_index + 1])
                if the_selected_cell_index - 1 >= 0:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_x[the_selected_cell_index - 1])

            elif selected_cell.position[2] == 0:
                for cell in board:
                    if cell.position[1] == selected_cell.position[1]:
                        center_line_parallel_to_axis_x.append(cell)

                center_line_parallel_to_axis_x = sorted(center_line_parallel_to_axis_x,
                                                        key=lambda a__cell: a__cell.position[2]
                                                        if a__cell.position[2] != 0 else a__cell.position[0])

                the_selected_cell_index = center_line_parallel_to_axis_x.index(selected_cell)

                if the_selected_cell_index + 1 < 8:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_x[the_selected_cell_index + 1])
                if the_selected_cell_index - 1 >= 0:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_x[the_selected_cell_index - 1])

            # 3 nearby cells to the right
            right_line_parallel_to_axis_x = []
            if selected_cell_index != 7:
                right_nearby_cell = line_perpendicular_to_axis_x[selected_cell_index + 1]
                move_cells_to_be_checked.append(right_nearby_cell)
                if right_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[2] == right_nearby_cell.position[2]:
                            right_line_parallel_to_axis_x.append(cell)

                    if right_nearby_cell.position[2] == -3 or right_nearby_cell.position[2] == -1:
                        right_line_parallel_to_axis_x = sorted(right_line_parallel_to_axis_x,
                                                               key=lambda a__cell: a__cell.position[0])[::-1]

                    right_nearby_cell_index = right_line_parallel_to_axis_x.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_x[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_x[right_nearby_cell_index - 1])

                elif right_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[1] == right_nearby_cell.position[1]:
                            right_line_parallel_to_axis_x.append(cell)

                    right_line_parallel_to_axis_x = sorted(right_line_parallel_to_axis_x,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[0])

                    right_nearby_cell_index = right_line_parallel_to_axis_x.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_x[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_x[right_nearby_cell_index - 1])

            # 3 nearby cells to the left
            left_line_parallel_to_axis_x = []
            if selected_cell_index != 0:
                left_nearby_cell = line_perpendicular_to_axis_x[selected_cell_index - 1]
                move_cells_to_be_checked.append(left_nearby_cell)
                if left_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[2] == left_nearby_cell.position[2]:
                            left_line_parallel_to_axis_x.append(cell)

                    if left_nearby_cell.position[2] == -3 or left_nearby_cell.position[2] == -1:
                        left_line_parallel_to_axis_x = sorted(left_line_parallel_to_axis_x,
                                                              key=lambda a__cell: a__cell.position[0])[::-1]

                    left_nearby_cell_index = left_line_parallel_to_axis_x.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_x[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_x[left_nearby_cell_index - 1])

                elif left_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[1] == left_nearby_cell.position[1]:
                            left_line_parallel_to_axis_x.append(cell)

                    left_line_parallel_to_axis_x = sorted(left_line_parallel_to_axis_x,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[0])

                    left_nearby_cell_index = left_line_parallel_to_axis_x.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_x[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_x[left_nearby_cell_index - 1])

        move_cells_check(move_cells_to_be_checked)
        move_cells_to_be_checked.clear()

        # search for possible moves relatively axis Y
        line_perpendicular_to_axis_y = []
        if 5 > self.position[1] > -5 and self.position[1] != 0:
            for cell in board:
                if cell.position[1] == self.position[1]:
                    line_perpendicular_to_axis_y.append(cell)

            # sorting cells in "line_perpendicular_to_axis_y"
            line_perpendicular_to_axis_y = sorted(line_perpendicular_to_axis_y,
                                                  key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else
                                                  a_cell.position[0])

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_y"
            for cell in line_perpendicular_to_axis_y:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_y.index(cell)
                    selected_cell = cell

            # 2 cells above and below the cell with selected king
            center_line_parallel_to_axis_y = []
            if selected_cell.position[0] == 0:
                for cell in board:
                    if cell.position[2] == selected_cell.position[2]:
                        center_line_parallel_to_axis_y.append(cell)

                if selected_cell.position[2] == -3 or selected_cell.position[2] == -1:
                    center_line_parallel_to_axis_y = sorted(center_line_parallel_to_axis_y,
                                                            key=lambda a__cell: a__cell.position[0])[::-1]

                the_selected_cell_index = center_line_parallel_to_axis_y.index(selected_cell)

                if the_selected_cell_index + 1 < 8:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_y[the_selected_cell_index + 1])
                if the_selected_cell_index - 1 >= 0:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_y[the_selected_cell_index - 1])

            elif selected_cell.position[2] == 0:
                for cell in board:
                    if cell.position[0] == selected_cell.position[0]:
                        center_line_parallel_to_axis_y.append(cell)

                center_line_parallel_to_axis_y = sorted(center_line_parallel_to_axis_y,
                                                        key=lambda a__cell: a__cell.position[2]
                                                        if a__cell.position[2] != 0 else a__cell.position[1])

                the_selected_cell_index = center_line_parallel_to_axis_y.index(selected_cell)

                if the_selected_cell_index + 1 < 8:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_y[the_selected_cell_index + 1])
                if the_selected_cell_index - 1 >= 0:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_y[the_selected_cell_index - 1])

            # 3 nearby cells to the right
            right_line_parallel_to_axis_y = []
            if selected_cell_index != 7:
                right_nearby_cell = line_perpendicular_to_axis_y[selected_cell_index + 1]
                move_cells_to_be_checked.append(right_nearby_cell)
                if right_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[2] == right_nearby_cell.position[2]:
                            right_line_parallel_to_axis_y.append(cell)

                    if right_nearby_cell.position[2] == -3 or right_nearby_cell.position[2] == -1:
                        right_line_parallel_to_axis_y = sorted(right_line_parallel_to_axis_y,
                                                               key=lambda a__cell: a__cell.position[0])[::-1]

                    right_nearby_cell_index = right_line_parallel_to_axis_y.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index - 1])

                elif right_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[0] == right_nearby_cell.position[0]:
                            right_line_parallel_to_axis_y.append(cell)

                    right_line_parallel_to_axis_y = sorted(right_line_parallel_to_axis_y,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[1])

                    right_nearby_cell_index = right_line_parallel_to_axis_y.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index - 1])

            # 3 nearby cells to the right
            left_line_parallel_to_axis_y = []
            if selected_cell_index != 0:
                left_nearby_cell = line_perpendicular_to_axis_y[selected_cell_index - 1]
                move_cells_to_be_checked.append(left_nearby_cell)
                if left_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[2] == left_nearby_cell.position[2]:
                            left_line_parallel_to_axis_y.append(cell)

                    if left_nearby_cell.position[2] == -3 or left_nearby_cell.position[2] == -1:
                        left_line_parallel_to_axis_y = sorted(left_line_parallel_to_axis_y,
                                                              key=lambda a__cell: a__cell.position[0])[::-1]

                    left_nearby_cell_index = left_line_parallel_to_axis_y.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index - 1])

                elif left_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[0] == left_nearby_cell.position[0]:
                            left_line_parallel_to_axis_y.append(cell)

                    left_line_parallel_to_axis_y = sorted(left_line_parallel_to_axis_y,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[1])

                    left_nearby_cell_index = left_line_parallel_to_axis_y.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index - 1])

        move_cells_check(move_cells_to_be_checked)
        move_cells_to_be_checked.clear()

        # search for possible moves relatively axis Z
        line_perpendicular_to_axis_z = []
        if 5 > self.position[2] > -5 and self.position[2] != 0:
            for cell in board:
                if cell.position[2] == self.position[2]:
                    line_perpendicular_to_axis_z.append(cell)

            # sorting cells in "line_perpendicular_to_axis_z"
            if self.position[2] == -3 or self.position[2] == -1:
                line_perpendicular_to_axis_z = sorted(line_perpendicular_to_axis_z,
                                                      key=lambda a_cell: a_cell.position[0])[::-1]

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_z"
            for cell in line_perpendicular_to_axis_z:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_z.index(cell)
                    selected_cell = cell

            # cell above and cell below the cell with selected king
            center_line_parallel_to_axis_z = []
            if selected_cell.position[0] == 0:
                for cell in board:
                    if cell.position[1] == selected_cell.position[1]:
                        center_line_parallel_to_axis_z.append(cell)

                center_line_parallel_to_axis_z = sorted(center_line_parallel_to_axis_z,
                                                        key=lambda a__cell: a__cell.position[2]
                                                        if a__cell.position[2] != 0 else a__cell.position[0])

                the_selected_cell_index = center_line_parallel_to_axis_z.index(selected_cell)

                if the_selected_cell_index + 1 < 8:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_z[the_selected_cell_index + 1])
                if the_selected_cell_index - 1 >= 0:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_z[the_selected_cell_index - 1])

            elif selected_cell.position[1] == 0:
                for cell in board:
                    if cell.position[0] == selected_cell.position[0]:
                        center_line_parallel_to_axis_z.append(cell)

                center_line_parallel_to_axis_z = sorted(center_line_parallel_to_axis_z,
                                                        key=lambda a__cell: a__cell.position[2]
                                                        if a__cell.position[2] != 0 else a__cell.position[1])

                the_selected_cell_index = center_line_parallel_to_axis_z.index(selected_cell)

                if the_selected_cell_index + 1 < 8:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_z[the_selected_cell_index + 1])
                if the_selected_cell_index - 1 >= 0:
                    move_cells_to_be_checked.append(center_line_parallel_to_axis_z[the_selected_cell_index - 1])

            # 3 nearby cells to the right
            right_line_parallel_to_axis_z = []
            if selected_cell_index != 7:
                right_nearby_cell = line_perpendicular_to_axis_z[selected_cell_index + 1]
                move_cells_to_be_checked.append(right_nearby_cell)
                if right_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[1] == right_nearby_cell.position[1]:
                            right_line_parallel_to_axis_z.append(cell)

                    right_line_parallel_to_axis_z = sorted(right_line_parallel_to_axis_z,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[0])

                    right_nearby_cell_index = right_line_parallel_to_axis_z.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index - 1])

                elif right_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[0] == right_nearby_cell.position[0]:
                            right_line_parallel_to_axis_z.append(cell)

                    right_line_parallel_to_axis_z = sorted(right_line_parallel_to_axis_z,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[1])

                    right_nearby_cell_index = right_line_parallel_to_axis_z.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index - 1])

            # 3 nearby cells to the left
            left_line_parallel_to_axis_z = []
            if selected_cell_index != 0:
                left_nearby_cell = line_perpendicular_to_axis_z[selected_cell_index - 1]
                move_cells_to_be_checked.append(left_nearby_cell)
                if left_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[1] == left_nearby_cell.position[1]:
                            left_line_parallel_to_axis_z.append(cell)

                    left_line_parallel_to_axis_z = sorted(left_line_parallel_to_axis_z,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[0])

                    left_nearby_cell_index = left_line_parallel_to_axis_z.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index - 1])

                elif left_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[0] == left_nearby_cell.position[0]:
                            left_line_parallel_to_axis_z.append(cell)

                    left_line_parallel_to_axis_z = sorted(left_line_parallel_to_axis_z,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[1])

                    left_nearby_cell_index = left_line_parallel_to_axis_z.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index - 1])

        move_cells_check(move_cells_to_be_checked)

        possible_move_cells_list.extend([key for key in self.castling().keys()])

        # Adding piece's current position cell into the list in order to highlight cells when piece is selected
        for cell in board:
            if self.position == cell.position:
                possible_move_cells_list.append(cell)

        # Return list of cells available for move + current cell
        return possible_move_cells_list


class Knight(Piece):
    def possible_moves(self):
        super().possible_moves()
        move_cells_to_be_checked = []
        possible_move_cells_list = []

        """
        The function below receives a list of cells and checks cells in the list on the following:
        - whether a cell is occupied by another piece or not,
        - if occupied, whether cell is occupied by own piece or by enemy piece.
        The list of possible moves is formed based on results of checking 
        """

        def move_cells_check(cells_list: list):
            for cell in cells_list:
                if cell.occupied is False and cell not in possible_move_cells_list:
                    possible_move_cells_list.append(cell)
                elif cell.occupied is True and cell not in possible_move_cells_list:
                    for piece in all_pieces_lst:
                        if piece.position == cell.position and piece.color != self.color:
                            possible_move_cells_list.append(cell)

        # search for possible moves relatively axis X
        line_perpendicular_to_axis_x = []
        if 5 > self.position[0] > -5 and self.position[0] != 0:
            for cell in board:
                if cell.position[0] == self.position[0]:
                    line_perpendicular_to_axis_x.append(cell)

            # sorting cells in "line_perpendicular_to_axis_x"
            line_perpendicular_to_axis_x = sorted(line_perpendicular_to_axis_x,
                                                  key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0
                                                  else a_cell.position[1])

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_x"
            for cell in line_perpendicular_to_axis_x:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_x.index(cell)

            # 2 cells up/down and 1 cell to the right move
            right_line_parallel_to_axis_x = []
            if selected_cell_index != 7:
                right_nearby_cell = line_perpendicular_to_axis_x[selected_cell_index + 1]
                if right_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[2] == right_nearby_cell.position[2]:
                            right_line_parallel_to_axis_x.append(cell)

                    if right_nearby_cell.position[2] == -3 or right_nearby_cell.position[2] == -1:
                        right_line_parallel_to_axis_x = sorted(right_line_parallel_to_axis_x,
                                                               key=lambda a__cell: a__cell.position[0])[::-1]

                    right_nearby_cell_index = right_line_parallel_to_axis_x.index(right_nearby_cell)

                    if right_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index + 2])
                    if right_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index - 2])

                elif right_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[1] == right_nearby_cell.position[1]:
                            right_line_parallel_to_axis_x.append(cell)

                    right_line_parallel_to_axis_x = sorted(right_line_parallel_to_axis_x,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[0])

                    right_nearby_cell_index = right_line_parallel_to_axis_x.index(right_nearby_cell)

                    if right_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index + 2])
                    if right_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index - 2])

            # 2 cells up/down and 1 cell to the left move
            left_line_parallel_to_axis_x = []
            if selected_cell_index != 0:
                left_nearby_cell = line_perpendicular_to_axis_x[selected_cell_index - 1]
                if left_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[2] == left_nearby_cell.position[2]:
                            left_line_parallel_to_axis_x.append(cell)

                    if left_nearby_cell.position[2] == -3 or left_nearby_cell.position[2] == -1:
                        left_line_parallel_to_axis_x = sorted(left_line_parallel_to_axis_x,
                                                              key=lambda a__cell: a__cell.position[0])[::-1]

                    left_nearby_cell_index = left_line_parallel_to_axis_x.index(left_nearby_cell)

                    if left_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index + 2])
                    if left_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index - 2])

                elif left_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[1] == left_nearby_cell.position[1]:
                            left_line_parallel_to_axis_x.append(cell)

                    left_line_parallel_to_axis_x = sorted(left_line_parallel_to_axis_x,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[0])

                    left_nearby_cell_index = left_line_parallel_to_axis_x.index(left_nearby_cell)

                    if left_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index + 2])
                    if left_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index - 2])

            #  1 cell up/down and 2 cells to the right move
            right_line_parallel_to_axis_x = []
            if selected_cell_index <= 5:
                right_nearby_cell = line_perpendicular_to_axis_x[selected_cell_index + 2]
                if right_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[2] == right_nearby_cell.position[2]:
                            right_line_parallel_to_axis_x.append(cell)

                    if right_nearby_cell.position[2] == -3 or right_nearby_cell.position[2] == -1:
                        right_line_parallel_to_axis_x = sorted(right_line_parallel_to_axis_x,
                                                               key=lambda a__cell: a__cell.position[0])[::-1]

                    right_nearby_cell_index = right_line_parallel_to_axis_x.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index - 1])

                elif right_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[1] == right_nearby_cell.position[1]:
                            right_line_parallel_to_axis_x.append(cell)

                    right_line_parallel_to_axis_x = sorted(right_line_parallel_to_axis_x,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[0])

                    right_nearby_cell_index = right_line_parallel_to_axis_x.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(
                            right_line_parallel_to_axis_x[right_nearby_cell_index - 1])

            #  1 cell up/down and 2 cells to the left move
            left_line_parallel_to_axis_x = []
            if selected_cell_index >= 2:
                left_nearby_cell = line_perpendicular_to_axis_x[selected_cell_index - 2]
                if left_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[2] == left_nearby_cell.position[2]:
                            left_line_parallel_to_axis_x.append(cell)

                    if left_nearby_cell.position[2] == -3 or left_nearby_cell.position[2] == -1:
                        left_line_parallel_to_axis_x = sorted(left_line_parallel_to_axis_x,
                                                              key=lambda a__cell: a__cell.position[0])[::-1]

                    left_nearby_cell_index = left_line_parallel_to_axis_x.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index - 1])

                elif left_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[1] == left_nearby_cell.position[1]:
                            left_line_parallel_to_axis_x.append(cell)

                    left_line_parallel_to_axis_x = sorted(left_line_parallel_to_axis_x,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[0])

                    left_nearby_cell_index = left_line_parallel_to_axis_x.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(
                            left_line_parallel_to_axis_x[left_nearby_cell_index - 1])

        move_cells_check(move_cells_to_be_checked)
        move_cells_to_be_checked.clear()

        # search for possible moves relatively axis Y
        line_perpendicular_to_axis_y = []
        if 5 > self.position[1] > -5 and self.position[1] != 0:
            for cell in board:
                if cell.position[1] == self.position[1]:
                    line_perpendicular_to_axis_y.append(cell)

            # sorting cells in "line_perpendicular_to_axis_y"
            line_perpendicular_to_axis_y = sorted(line_perpendicular_to_axis_y,
                                                  key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else
                                                  a_cell.position[0])

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_y"
            for cell in line_perpendicular_to_axis_y:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_y.index(cell)

            # 2 cells up/down and 1 cell to the right move
            right_line_parallel_to_axis_y = []
            if selected_cell_index != 7:
                right_nearby_cell = line_perpendicular_to_axis_y[selected_cell_index + 1]
                if right_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[2] == right_nearby_cell.position[2]:
                            right_line_parallel_to_axis_y.append(cell)

                    if right_nearby_cell.position[2] == -3 or right_nearby_cell.position[2] == -1:
                        right_line_parallel_to_axis_y = sorted(right_line_parallel_to_axis_y,
                                                               key=lambda a__cell: a__cell.position[0])[::-1]

                    right_nearby_cell_index = right_line_parallel_to_axis_y.index(right_nearby_cell)

                    if right_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index + 2])
                    if right_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index - 2])

                elif right_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[0] == right_nearby_cell.position[0]:
                            right_line_parallel_to_axis_y.append(cell)

                    right_line_parallel_to_axis_y = sorted(right_line_parallel_to_axis_y,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[1])

                    right_nearby_cell_index = right_line_parallel_to_axis_y.index(right_nearby_cell)

                    if right_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index + 2])
                    if right_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index - 2])

            # 2 cells up/down and 1 cell to the left move
            left_line_parallel_to_axis_y = []
            if selected_cell_index != 0:
                left_nearby_cell = line_perpendicular_to_axis_y[selected_cell_index - 1]
                if left_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[2] == left_nearby_cell.position[2]:
                            left_line_parallel_to_axis_y.append(cell)

                    if left_nearby_cell.position[2] == -3 or left_nearby_cell.position[2] == -1:
                        left_line_parallel_to_axis_y = sorted(left_line_parallel_to_axis_y,
                                                              key=lambda a__cell: a__cell.position[0])[::-1]

                    left_nearby_cell_index = left_line_parallel_to_axis_y.index(left_nearby_cell)

                    if left_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index + 2])
                    if left_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index - 2])

                elif left_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[0] == left_nearby_cell.position[0]:
                            left_line_parallel_to_axis_y.append(cell)

                    left_line_parallel_to_axis_y = sorted(left_line_parallel_to_axis_y,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[1])

                    left_nearby_cell_index = left_line_parallel_to_axis_y.index(left_nearby_cell)

                    if left_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index + 2])
                    if left_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index - 2])

            #  1 cell up/down and 2 cells to the right move
            right_line_parallel_to_axis_y = []
            if selected_cell_index <= 5:
                right_nearby_cell = line_perpendicular_to_axis_y[selected_cell_index + 2]
                if right_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[2] == right_nearby_cell.position[2]:
                            right_line_parallel_to_axis_y.append(cell)

                    if right_nearby_cell.position[2] == -3 or right_nearby_cell.position[2] == -1:
                        right_line_parallel_to_axis_y = sorted(right_line_parallel_to_axis_y,
                                                               key=lambda a__cell: a__cell.position[0])[::-1]

                    right_nearby_cell_index = right_line_parallel_to_axis_y.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index - 1])

                elif right_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[0] == right_nearby_cell.position[0]:
                            right_line_parallel_to_axis_y.append(cell)

                    right_line_parallel_to_axis_y = sorted(right_line_parallel_to_axis_y,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[1])

                    right_nearby_cell_index = right_line_parallel_to_axis_y.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_y[right_nearby_cell_index - 1])

            #  1 cell up/down and 2 cells to the left move
            left_line_parallel_to_axis_y = []
            if selected_cell_index >= 2:
                left_nearby_cell = line_perpendicular_to_axis_y[selected_cell_index - 2]
                if left_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[2] == left_nearby_cell.position[2]:
                            left_line_parallel_to_axis_y.append(cell)

                    if left_nearby_cell.position[2] == -3 or left_nearby_cell.position[2] == -1:
                        left_line_parallel_to_axis_y = sorted(left_line_parallel_to_axis_y,
                                                              key=lambda a__cell: a__cell.position[0])[::-1]

                    left_nearby_cell_index = left_line_parallel_to_axis_y.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index - 1])

                elif left_nearby_cell.position[2] == 0:
                    for cell in board:
                        if cell.position[0] == left_nearby_cell.position[0]:
                            left_line_parallel_to_axis_y.append(cell)

                    left_line_parallel_to_axis_y = sorted(left_line_parallel_to_axis_y,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[1])

                    left_nearby_cell_index = left_line_parallel_to_axis_y.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_y[left_nearby_cell_index - 1])

        move_cells_check(move_cells_to_be_checked)
        move_cells_to_be_checked.clear()

        # search for possible moves relatively axis Z
        line_perpendicular_to_axis_z = []
        if 5 > self.position[2] > -5 and self.position[2] != 0:
            for cell in board:
                if cell.position[2] == self.position[2]:
                    line_perpendicular_to_axis_z.append(cell)

            # sorting cells in "line_perpendicular_to_axis_z"
            if self.position[2] == -3 or self.position[2] == -1:
                line_perpendicular_to_axis_z = sorted(line_perpendicular_to_axis_z,
                                                      key=lambda a_cell: a_cell.position[0])[::-1]

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_z"
            for cell in line_perpendicular_to_axis_z:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_z.index(cell)

            # 2 cells up/down and 1 cell to the right move
            right_line_parallel_to_axis_z = []
            if selected_cell_index != 7:
                right_nearby_cell = line_perpendicular_to_axis_z[selected_cell_index + 1]
                if right_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[1] == right_nearby_cell.position[1]:
                            right_line_parallel_to_axis_z.append(cell)

                    right_line_parallel_to_axis_z = sorted(right_line_parallel_to_axis_z,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[0])

                    right_nearby_cell_index = right_line_parallel_to_axis_z.index(right_nearby_cell)

                    if right_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index + 2])
                    if right_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index - 2])

                elif right_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[0] == right_nearby_cell.position[0]:
                            right_line_parallel_to_axis_z.append(cell)

                    right_line_parallel_to_axis_z = sorted(right_line_parallel_to_axis_z,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[1])

                    right_nearby_cell_index = right_line_parallel_to_axis_z.index(right_nearby_cell)

                    if right_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index + 2])
                    if right_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index - 2])

            # 2 cells up/down and 1 cell to the left move
            left_line_parallel_to_axis_z = []
            if selected_cell_index != 0:
                left_nearby_cell = line_perpendicular_to_axis_z[selected_cell_index - 1]
                if left_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[1] == left_nearby_cell.position[1]:
                            left_line_parallel_to_axis_z.append(cell)

                    left_line_parallel_to_axis_z = sorted(left_line_parallel_to_axis_z,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[0])

                    left_nearby_cell_index = left_line_parallel_to_axis_z.index(left_nearby_cell)

                    if left_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index + 2])
                    if left_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index - 2])

                elif left_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[0] == left_nearby_cell.position[0]:
                            left_line_parallel_to_axis_z.append(cell)

                    left_line_parallel_to_axis_z = sorted(left_line_parallel_to_axis_z,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[1])

                    left_nearby_cell_index = left_line_parallel_to_axis_z.index(left_nearby_cell)

                    if left_nearby_cell_index + 2 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index + 2])
                    if left_nearby_cell_index - 2 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index - 2])

            #  1 cell up/down and 2 cells to the right move
            right_line_parallel_to_axis_z = []
            if selected_cell_index <= 5:
                right_nearby_cell = line_perpendicular_to_axis_z[selected_cell_index + 2]
                if right_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[1] == right_nearby_cell.position[1]:
                            right_line_parallel_to_axis_z.append(cell)

                    right_line_parallel_to_axis_z = sorted(right_line_parallel_to_axis_z,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[0])

                    right_nearby_cell_index = right_line_parallel_to_axis_z.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index - 1])

                elif right_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[0] == right_nearby_cell.position[0]:
                            right_line_parallel_to_axis_z.append(cell)

                    right_line_parallel_to_axis_z = sorted(right_line_parallel_to_axis_z,
                                                           key=lambda a__cell: a__cell.position[2]
                                                           if a__cell.position[2] != 0 else a__cell.position[1])

                    right_nearby_cell_index = right_line_parallel_to_axis_z.index(right_nearby_cell)

                    if right_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index + 1])
                    if right_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(right_line_parallel_to_axis_z[right_nearby_cell_index - 1])

            #  1 cell up/down and 2 cells to the left move
            left_line_parallel_to_axis_z = []
            if selected_cell_index >= 2:
                left_nearby_cell = line_perpendicular_to_axis_z[selected_cell_index - 2]
                if left_nearby_cell.position[0] == 0:
                    for cell in board:
                        if cell.position[1] == left_nearby_cell.position[1]:
                            left_line_parallel_to_axis_z.append(cell)

                    left_line_parallel_to_axis_z = sorted(left_line_parallel_to_axis_z,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[0])

                    left_nearby_cell_index = left_line_parallel_to_axis_z.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index - 1])

                elif left_nearby_cell.position[1] == 0:
                    for cell in board:
                        if cell.position[0] == left_nearby_cell.position[0]:
                            left_line_parallel_to_axis_z.append(cell)

                    left_line_parallel_to_axis_z = sorted(left_line_parallel_to_axis_z,
                                                          key=lambda a__cell: a__cell.position[2]
                                                          if a__cell.position[2] != 0 else a__cell.position[1])

                    left_nearby_cell_index = left_line_parallel_to_axis_z.index(left_nearby_cell)

                    if left_nearby_cell_index + 1 < 8:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index + 1])
                    if left_nearby_cell_index - 1 >= 0:
                        move_cells_to_be_checked.append(left_line_parallel_to_axis_z[left_nearby_cell_index - 1])

        move_cells_check(move_cells_to_be_checked)

        # Adding piece's current position cell into the list in order to highlight cells when piece is selected
        for cell in board:
            if self.position == cell.position:
                possible_move_cells_list.append(cell)

        # Return list of cells available for move + current cell
        return possible_move_cells_list


class Rook(Piece):
    def rook_possible_moves(self):
        super().possible_moves()
        possible_move_cells_list = []
        all_moves_cells_list = []

        """
        The function below receives a list of cells (a line of cells perpendicular to corresponding axis), finds the 
        index of cell with selected piece and then checks cells in the line which index is less than found index and 
        cells in the line which index is greater than found index. The cells are checked on the following:
        - whether a cell is occupied by another piece or not,
        - if occupied, whether cell is occupied by own piece or by enemy piece.
        The list of possible moves is formed based on results of chcking 
        """

        def move_cells_check(cells_list: list) -> list:
            list_to_be_returned = []
            # finding out the index of cell with selected piece in collection of cells
            for cell in cells_list:
                if cell.position == self.position:
                    selected_cell_index = cells_list.index(cell)

            if selected_cell_index != 7:
                for index in range(selected_cell_index + 1, 8):
                    if cells_list[index].occupied is False:
                        list_to_be_returned.append(cells_list[index])
                    elif cells_list[index].occupied is True:
                        for piece in all_pieces_lst:
                            if piece.position == cells_list[index].position and piece.color == self.color:
                                pass
                            elif piece.position == cells_list[index].position and piece.color != self.color:
                                list_to_be_returned.append(cells_list[index])
                        break
            if selected_cell_index != 0:
                for index in range(selected_cell_index - 1, -1, -1):
                    if cells_list[index].occupied is False:
                        list_to_be_returned.append(cells_list[index])
                    elif cells_list[index].occupied is True:
                        for piece in all_pieces_lst:
                            if piece.position == cells_list[index].position and piece.color == self.color:
                                pass
                            elif piece.position == cells_list[index].position and piece.color != self.color:
                                list_to_be_returned.append(cells_list[index])
                        break
            return list_to_be_returned

        # Moves perpendicular to axis X
        if 5 > self.position[0] > -5 and self.position[0] != 0:
            # collecting all cells available for move (obstacles(other pieces) are not taken into consideration)
            for cell in board:
                if cell.position[0] == self.position[0]:
                    all_moves_cells_list.append(cell)

            # sorting of collected cells
            all_moves_cells_list = sorted(all_moves_cells_list,
                                          key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else
                                          a_cell.position[1])

            possible_move_cells_list.extend(move_cells_check(all_moves_cells_list))
            all_moves_cells_list.clear()

        # Moves perpendicular to axis Y
        if 5 > self.position[1] > -5 and self.position[1] != 0:
            # collecting all cells available for move (obstacles(other pieces) are not taken into consideration)
            for cell in board:
                if cell.position[1] == self.position[1]:
                    all_moves_cells_list.append(cell)

            # sorting of collected cells
            all_moves_cells_list = sorted(all_moves_cells_list,
                                          key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else
                                          a_cell.position[0])

            possible_move_cells_list.extend(move_cells_check(all_moves_cells_list))
            all_moves_cells_list.clear()

        # Moves perpendicular to axis Z
        if 5 > self.position[2] > -5 and self.position[2] != 0:
            # collecting all cells available for move (obstacles(other pieces) are not taken into consideration)
            for cell in board:
                if cell.position[2] == self.position[2]:
                    all_moves_cells_list.append(cell)

            # sorting of collected cells
            if self.position[2] == -3 or self.position[2] == -1:
                all_moves_cells_list = sorted(all_moves_cells_list, key=lambda a_cell: a_cell.position[0])

            possible_move_cells_list.extend(move_cells_check(all_moves_cells_list))

        # Adding piece's current position cell into the list in order to highlight cells when piece is selected
        for cell in board:
            if self.position == cell.position:
                possible_move_cells_list.append(cell)

        # Return list of cells available for move + current cell
        return possible_move_cells_list

    def highlight_cells(self):
        super().highlight_cells()
        cells_to_be_highlighted = self.rook_possible_moves()
        for cell in cells_to_be_highlighted:
            if cell.initial_color == dark_color:
                cell.current_color = GREEN_DARK
            else:
                cell.current_color = GREEN_LIGHT
        return cells_to_be_highlighted


class Queen(Rook, Bishop):
    def highlight_cells(self):
        super().highlight_cells()
        cells_to_be_highlighted = self.rook_possible_moves()[:-1]
        cells_to_be_highlighted.extend(self.bishop_possible_moves())
        for cell in cells_to_be_highlighted:
            if cell.initial_color == dark_color:
                cell.current_color = GREEN_DARK
            else:
                cell.current_color = GREEN_LIGHT
        return cells_to_be_highlighted


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

            # possible forward moves of white pawns in section a5-l7
            elif -4 < self.position[0] < 0 <= self.position[1] and self.position[2] <= 0:
                next_cell_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=0)

            # possible forward moves of white pawns in section l9-h11
            elif self.position[0] >= 0 and self.position[1] >= 0 and 0 < self.position[2] < 4:
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
            elif self.position[0] >= 0 and 0 <= self.position[1] and self.position[2] > 0:
                next_cell_check(x1=1, x2=0, y1=1, y2=0, z1=1, z2=1)

            # possible forward moves of black pawns in section a4-h2
            elif self.position[0] >= 0 > self.position[1] > -4 and self.position[2] <= 0:
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

            # possible forward moves of red pawns in section h4-a2
            elif self.position[0] >= 0 > self.position[1] > -4 and 0 >= self.position[2]:
                next_cell_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=0)

            # possible forward moves of red pawns in section a5-l7
            elif -4 < self.position[0] < 0 <= self.position[1] and 0 >= self.position[2]:
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
            if self.position[0] == 0 and -4 < self.position[1] < -1 and self.position[2] < -1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=-1)

            # possible capture moves of white pawns in section f2-h3
            elif self.position[0] > 1 and -1 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=1, z2=0)

            # possible capture moves of white pawns in section d2-d3
            elif self.position[0] == 0 and -4 < self.position[1] < -1 == self.position[2]:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)

            # possible capture moves of white pawns in section e2-e3
            elif self.position[0] == 1 and -1 > self.position[1] > -4 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=-1)

            # possible capture moves of white pawns in section a4-c4
            elif self.position[0] == 0 and self.position[1] == -1 and -1 > self.position[2]:
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of white pawns in section f4-h4
            elif self.position[0] > 1 and self.position[1] == -1 and self.position[2] == 0:
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
            elif -4 < self.position[0] < 0 == self.position[1] and -1 > self.position[2]:
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of white pawns in section d5-d7
            elif -4 < self.position[0] < 0 == self.position[1] and self.position[2] == -1:
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
            elif -4 < self.position[0] < 0 == self.position[2] and self.position[1] == 1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of white pawns in section j5-l7
            elif -4 < self.position[0] < 0 == self.position[2] and self.position[1] > 1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=1, z2=0)

            # possible capture moves of white pawns in section i9-i11
            elif self.position[0] == 0 and self.position[1] == 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of white pawns in section j9-l11
            elif self.position[0] == 0 and self.position[1] > 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=1)

        # BLACK PAWNS
        if self.color == "black":
            # possible capture moves of black pawns in section l7-j6
            if -1 > self.position[0] > -4 and self.position[1] > 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of black pawns in section a7-c6
            elif -1 > self.position[0] > -4 and self.position[1] == 0 and -1 > self.position[2]:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=-1)

            # possible capture moves of black pawns in section i7-i6
            elif -1 > self.position[0] > -4 and self.position[1] == 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of black pawns in section d7-d6
            elif -4 < self.position[0] < -1 == self.position[2] and self.position[1] == 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=1, z1=0, z2=0)

            # possible capture moves of black pawns in section l5-j5
            elif self.position[0] == -1 and self.position[1] > 1 and self.position[2] == 0:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=1)

            # possible capture moves of black pawns in section a5-c5
            elif self.position[0] == -1 and self.position[1] == 0 and -1 > self.position[2]:
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
            elif self.position[0] == 0 and self.position[1] > 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=1)

            # possible capture moves of black pawns in section i9-i11
            elif self.position[0] == 0 and self.position[1] == 1 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=1, z1=1, z2=1)
                next_diagonal_cells_check(x1=0, x2=1, y1=0, y2=0, z1=1, z2=1)

            # possible capture moves of black pawns in section c4-a2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and -1 > self.position[2]:
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
            elif self.position[0] > 1 and self.position[1] == 0 and 4 > self.position[2] > 0:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=1)

            # possible capture moves of black pawns in section e4-e2
            elif self.position[0] == 1 and -4 < self.position[1] < 0 == self.position[2]:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=1, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of black pawns in section f4-h2
            elif self.position[0] > 1 and -4 < self.position[1] < 0 == self.position[2]:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=1, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=1, z2=0)

        # RED PAWNS
        if self.color == "red":
            # possible capture moves of red pawns in section h11-f10
            if self.position[0] > 1 and self.position[1] == 0 and 4 > self.position[2] > 1:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=-1)

            # possible capture moves of red pawns in section l11-j10
            elif self.position[0] == 0 and self.position[1] > 1 and 4 > self.position[2] > 1:
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
            elif self.position[0] > 1 and self.position[1] == 0 and self.position[2] == 1:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section j9-l9
            elif self.position[0] == 0 and self.position[1] > 1 and self.position[2] == 1:
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
            elif self.position[0] > 1 and -4 < self.position[1] < 0 == self.position[2]:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section e4-e2
            elif self.position[0] == 1 and -4 < self.position[1] < 0 == self.position[2]:
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)
                next_diagonal_cells_check(x1=0, x2=0, y1=1, y2=-1, z1=1, z2=-1)

            # possible capture moves of red pawns in section l5-j7
            elif -4 < self.position[0] < 0 == self.position[2] and self.position[1] > 1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section i5-i7
            elif -4 < self.position[0] < 0 == self.position[2] and self.position[1] == 1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=1, z1=0, z2=0)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=0, z1=1, z2=-1)

            # possible capture moves of red pawns in section d4-d2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=1, y1=1, y2=-1, z1=0, z2=0)

            # possible capture moves of red pawns in section c4-a2
            elif self.position[0] == 0 and 0 > self.position[1] > -4 and -1 > self.position[2]:
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=0, y1=1, y2=-1, z1=1, z2=1)

            # possible capture moves of red pawns in section i5-i7
            elif -4 < self.position[0] < 0 == self.position[1] and self.position[2] == -1:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=0, y2=1, z1=0, z2=0)

            # possible capture moves of red pawns in section d5-a7
            elif -4 < self.position[0] < 0 == self.position[1] and -1 > self.position[2]:
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=-1)
                next_diagonal_cells_check(x1=1, x2=-1, y1=1, y2=0, z1=1, z2=1)

        # Adding piece's current position cell into the list in order to highlight cells when piece is selected
        for cell in board:
            if self.position == cell.position:
                possible_move_cells_list.append(cell)

        # Return list of cells available for move + current cell
        return possible_move_cells_list

    def en_passant(self, moves_records: dict, current_move_number: int) -> list:
        """
        "list_to_be_returned" has the following values:
        index 0 - a cell to be highlighted as a cell available for move and to be added to "possible_move_cells_list"
        index 1 - a pawn to be captured through en passant
        index 2 - a cell where the pawn to be captured through en passant is located currently
        """
        list_to_be_returned = []

        # line of cells "a5-l5"
        line_perpendicular_to_axis_x = []
        if self.color == "white" and self.position[0] == -1 or self.color == "red" and self.position[0] == -1:
            for cell in board:
                if cell.position[0] == self.position[0]:
                    line_perpendicular_to_axis_x.append(cell)

            # sorting cells in "line_perpendicular_to_axis_x"
            line_perpendicular_to_axis_x = sorted(line_perpendicular_to_axis_x,
                                                  key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0
                                                  else a_cell.position[1])

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_x"
            for cell in line_perpendicular_to_axis_x:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_x.index(cell)
                    break

            for piece in all_pieces_lst:
                if selected_cell_index != 7 and \
                        piece.position == line_perpendicular_to_axis_x[selected_cell_index + 1].position and \
                        "Pawn" in piece.name:

                    if len(moves_records) > 0 and piece == moves_records[current_move_number][0] and \
                            moves_records[current_move_number][1].position[0] == -3:

                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number][1].position[0] + 1,
                                moves_records[current_move_number][1].position[1],
                                moves_records[current_move_number][1].position[2]
                            ]:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_x[selected_cell_index + 1]))
                                break

                    elif len(moves_records) > 1 and piece == moves_records[current_move_number - 1][0] and \
                            moves_records[current_move_number - 1][1].position[0] == -3:

                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number - 1][1].position[0] + 1,
                                moves_records[current_move_number - 1][1].position[1],
                                moves_records[current_move_number - 1][1].position[2]
                            ] and cell.occupied is False:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_x[selected_cell_index + 1]))
                                break

                if selected_cell_index != 0 and \
                        piece.position == line_perpendicular_to_axis_x[selected_cell_index - 1].position and \
                        "Pawn" in piece.name:
                    if len(moves_records) > 0 and piece == moves_records[current_move_number][0] and \
                            moves_records[current_move_number][1].position[0] == -3:
                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number][1].position[0] + 1,
                                moves_records[current_move_number][1].position[1],
                                moves_records[current_move_number][1].position[2]
                            ]:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_x[selected_cell_index + 1]))
                                break
                    elif len(moves_records) > 1 and piece == moves_records[current_move_number - 1][0] and \
                            moves_records[current_move_number - 1][1].position[0] == -3:
                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number - 1][1].position[0] + 1,
                                moves_records[current_move_number - 1][1].position[1],
                                moves_records[current_move_number - 1][1].position[2]
                            ] and cell.occupied is False:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_x[selected_cell_index + 1]))

        # line of cells "h9-l9"
        line_perpendicular_to_axis_z = []
        if self.color == "white" and self.position[2] == 1 or self.color == "black" and self.position[2] == 1:
            for cell in board:
                if cell.position[2] == self.position[2]:
                    line_perpendicular_to_axis_z.append(cell)

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_z"
            for cell in line_perpendicular_to_axis_z:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_z.index(cell)
                    break

            for piece in all_pieces_lst:
                if selected_cell_index != 7 and \
                        piece.position == line_perpendicular_to_axis_z[selected_cell_index + 1].position and \
                        "Pawn" in piece.name:

                    if len(moves_records) > 0 and piece == moves_records[current_move_number][0] and \
                            moves_records[current_move_number][1].position[2] == 3:

                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number][1].position[0],
                                moves_records[current_move_number][1].position[1],
                                moves_records[current_move_number][1].position[2] - 1
                            ]:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_z[selected_cell_index + 1]))
                                break

                    elif len(moves_records) > 1 and piece == moves_records[current_move_number - 1][0] and \
                            moves_records[current_move_number - 1][1].position[2] == 3:

                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number - 1][1].position[0],
                                moves_records[current_move_number - 1][1].position[1],
                                moves_records[current_move_number - 1][1].position[2] - 1
                            ] and cell.occupied is False:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_z[selected_cell_index + 1]))
                                break

                if selected_cell_index != 0 and \
                        piece.position == line_perpendicular_to_axis_z[selected_cell_index - 1].position and \
                        "Pawn" in piece.name:
                    if len(moves_records) > 0 and piece == moves_records[current_move_number][0] and \
                            moves_records[current_move_number][1].position[2] == 3:
                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number][1].position[0],
                                moves_records[current_move_number][1].position[1],
                                moves_records[current_move_number][1].position[2] - 1
                            ]:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_z[selected_cell_index + 1]))
                                break
                    elif len(moves_records) > 1 and piece == moves_records[current_move_number - 1][0] and \
                            moves_records[current_move_number - 1][1].position[2] == 3:
                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number - 1][1].position[0],
                                moves_records[current_move_number - 1][1].position[1],
                                moves_records[current_move_number - 1][1].position[2] - 1
                            ] and cell.occupied is False:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_z[selected_cell_index + 1]))

        # line of cells "a4-h4"
        line_perpendicular_to_axis_y = []
        if self.color == "black" and self.position[1] == -1 or self.color == "red" and self.position[1] == -1:
            for cell in board:
                if cell.position[1] == self.position[1]:
                    line_perpendicular_to_axis_y.append(cell)

            # sorting cells in "line_perpendicular_to_axis_y"
            line_perpendicular_to_axis_y = sorted(line_perpendicular_to_axis_y,
                                                  key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0
                                                  else a_cell.position[0])

            print([cell.name for cell in line_perpendicular_to_axis_y])

            # finding out the index of cell with selected piece in "line_perpendicular_to_axis_y"
            for cell in line_perpendicular_to_axis_y:
                if cell.position == self.position:
                    selected_cell_index = line_perpendicular_to_axis_y.index(cell)
                    break

            for piece in all_pieces_lst:
                if selected_cell_index != 7 and \
                        piece.position == line_perpendicular_to_axis_y[selected_cell_index + 1].position and \
                        "Pawn" in piece.name:

                    if len(moves_records) > 0 and piece == moves_records[current_move_number][0] and \
                            moves_records[current_move_number][1].position[1] == -3:

                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number][1].position[0],
                                moves_records[current_move_number][1].position[1] + 1,
                                moves_records[current_move_number][1].position[2]
                            ]:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_y[selected_cell_index + 1]))
                                break

                    elif len(moves_records) > 1 and piece == moves_records[current_move_number - 1][0] and \
                            moves_records[current_move_number - 1][1].position[1] == -3:

                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number - 1][1].position[0],
                                moves_records[current_move_number - 1][1].position[1] + 1,
                                moves_records[current_move_number - 1][1].position[2]
                            ] and cell.occupied is False:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_y[selected_cell_index + 1]))
                                break

                if selected_cell_index != 0 and \
                        piece.position == line_perpendicular_to_axis_y[selected_cell_index - 1].position and \
                        "Pawn" in piece.name:
                    if len(moves_records) > 0 and piece == moves_records[current_move_number][0] and \
                            moves_records[current_move_number][1].position[1] == -3:
                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number][1].position[0],
                                moves_records[current_move_number][1].position[1] + 1,
                                moves_records[current_move_number][1].position[2]
                            ]:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_y[selected_cell_index + 1]))
                                break
                    elif len(moves_records) > 1 and piece == moves_records[current_move_number - 1][0] and \
                            moves_records[current_move_number - 1][1].position[1] == -3:
                        for cell in board:
                            if cell.position == [
                                moves_records[current_move_number - 1][1].position[0],
                                moves_records[current_move_number - 1][1].position[1] + 1,
                                moves_records[current_move_number - 1][1].position[2]
                            ] and cell.occupied is False:
                                list_to_be_returned.extend((cell, piece,
                                                            line_perpendicular_to_axis_y[selected_cell_index + 1]))

        if len(list_to_be_returned) != 0 and list_to_be_returned[0].initial_color == dark_color:
            list_to_be_returned[0].current_color = GREEN_DARK
        elif len(list_to_be_returned) != 0 and list_to_be_returned[0].initial_color == light_color:
            list_to_be_returned[0].current_color = GREEN_LIGHT

        return list_to_be_returned

    def promotion(self):
        promotion_available = False
        if self.color != "white" and self.position[1] == -4 or self.color != "black" and self.position[0] == -4 or \
            self.color != "red" and self.position[2] == 4:
            promotion_available = True
        return promotion_available


# Creation of Piece objects
white_left_rook = Rook("w_l_Rook", "white", [0, -4, -4], False, True, False, w_rook)
white_left_knight = Knight("w_l_Knight", "white", [0, -4, -3], False, True, False, w_knight)
white_left_bishop = Bishop("w_l_Bishop", "white", [0, -4, -2], False, True, False, w_bishop)
white_queen = Queen("w_Queen", "white", [0, -4, -1], False, True, False, w_queen)
white_king = King("w_King", "white", [1, -4, 0], False, True, False, w_king)
white_right_bishop = Bishop("w_r_Bishop", "white", [2, -4, 0], False, True, False, w_bishop)
white_right_knight = Knight("w_r_Knight", "white", [3, -4, 0], False, True, False, w_knight)
white_right_rook = Rook("w_r_Rook", "white", [4, -4, 0], False, True, False, w_rook)
white_pawn1 = Pawn("w_1_Pawn", "white", [0, -3, -4], False, True, False, w_pawn)
white_pawn2 = Pawn("w_2_Pawn", "white", [0, -3, -3], False, True, False, w_pawn)
white_pawn3 = Pawn("w_3_Pawn", "white", [0, -3, -2], False, True, False, w_pawn)
white_pawn4 = Pawn("w_4_Pawn", "white", [0, -3, -1], False, True, False, w_pawn)
white_pawn5 = Pawn("w_5_Pawn", "white", [1, -3, 0], False, True, False, w_pawn)
white_pawn6 = Pawn("w_6_Pawn", "white", [2, -3, 0], False, True, False, w_pawn)
white_pawn7 = Pawn("w_7_Pawn", "white", [3, -3, 0], False, True, False, w_pawn)
white_pawn8 = Pawn("w_8_Pawn", "white", [4, -3, 0], False, True, False, w_pawn)

black_left_rook = Rook("b_l_Rook", "black", [-4, 4, 0], False, True, True, b_rook)
black_left_knight = Knight("b_l_Knight", "black", [-4, 3, 0], False, True, True, b_knight)
black_left_bishop = Bishop("b_l_Bishop", "black", [-4, 2, 0], False, True, True, b_bishop)
black_queen = Queen("b_Queen", "black", [-4, 1, 0], False, True, True, b_queen)
black_king = King("b_King", "black", [-4, 0, -1], False, True, True, b_king)
black_right_bishop = Bishop("b_r_Bishop", "black", [-4, 0, -2], False, True, True, b_bishop)
black_right_knight = Knight("b_r_Knight", "black", [-4, 0, -3], False, True, True, b_knight)
black_right_rook = Rook("b_r_Rook", "black", [-4, 0, -4], False, True, True, b_rook)
black_pawn1 = Pawn("b_1_Pawn", "black", [-3, 4, 0], False, True, True, b_pawn)
black_pawn2 = Pawn("b_2_Pawn", "black", [-3, 3, 0], False, True, True, b_pawn)
black_pawn3 = Pawn("b_3_Pawn", "black", [-3, 2, 0], False, True, True, b_pawn)
black_pawn4 = Pawn("b_4_Pawn", "black", [-3, 1, 0], False, True, True, b_pawn)
black_pawn5 = Pawn("b_5_Pawn", "black", [-3, 0, -1], False, True, True, b_pawn)
black_pawn6 = Pawn("b_6_Pawn", "black", [-3, 0, -2], False, True, True, b_pawn)
black_pawn7 = Pawn("b_7_Pawn", "black", [-3, 0, -3], False, True, True, b_pawn)
black_pawn8 = Pawn("b_8_Pawn", "black", [-3, 0, -4], False, True, True, b_pawn)

red_left_rook = Rook("r_l_Rook", "red", [4, 0, 4], False, True, True, r_rook)
red_left_knight = Knight("r_l_Knight", "red", [3, 0, 4], False, True, True, r_knight)
red_left_bishop = Bishop("r_l_Bishop", "red", [2, 0, 4], False, True, True, r_bishop)
red_queen = Queen("r_Queen", "red", [1, 0, 4], False, True, True, r_queen)
red_king = King("r_King", "red", [0, 1, 4], False, True, True, r_king)
red_right_bishop = Bishop("r_r_Bishop", "red", [0, 2, 4], False, True, True, r_bishop)
red_right_knight = Knight("r_r_Knight", "red", [0, 3, 4], False, True, True, r_knight)
red_right_rook = Rook("r_r_Rook", "red", [0, 4, 4], False, True, True, r_rook)
red_pawn1 = Pawn("r_1_Pawn", "red", [4, 0, 3], False, True, True, r_pawn)
red_pawn2 = Pawn("r_2_Pawn", "red", [3, 0, 3], False, True, True, r_pawn)
red_pawn3 = Pawn("r_3_Pawn", "red", [2, 0, 3], False, True, True, r_pawn)
red_pawn4 = Pawn("r_4_Pawn", "red", [1, 0, 3], False, True, True, r_pawn)
red_pawn5 = Pawn("r_5_Pawn", "red", [0, 1, 3], False, True, True, r_pawn)
red_pawn6 = Pawn("r_6_Pawn", "red", [0, 2, 3], False, True, True, r_pawn)
red_pawn7 = Pawn("r_7_Pawn", "red", [0, 3, 3], False, True, True, r_pawn)
red_pawn8 = Pawn("r_8_Pawn", "red", [0, 4, 3], False, True, True, r_pawn)

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
