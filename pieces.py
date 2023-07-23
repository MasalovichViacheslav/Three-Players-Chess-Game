# Source of piece images - https://opengameart.org/content/colorful-chess-pieces, author - Arsonide
import pygame
import os
from board import board, lines_cross_point
from colors import SPECIAL_WHITE


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
    def __init__(self, name: str, color: str, position: tuple, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.color = color
        self.position = position
        self.image = pygame.transform.scale_by(image, 0.4)
        self.image.set_colorkey(SPECIAL_WHITE)
        self.rect = self.image.get_rect()

    def piece_drawing(self, surface):
        for cell in board:
            if cell.position == self.position:
                rect_center_coords = lines_cross_point(cell.points[0], cell.points[2], cell.points[1], cell.points[3])
        self.rect.center = rect_center_coords
        surface.blit(self.image, self.rect)


class Bishop(Piece):
    pass


class King(Piece):
    pass


class Knight(Piece):
    pass


class Rook(Piece):
    pass


class Queen(Rook, Bishop):
    pass


class Pawn(Piece):
    pass


# Creation of Piece objects
white_left_rook = Rook("w_l_Rook", "white", (0, -4, -4), w_rook)
white_left_knight = Knight("w_l_Knight", "white", (0, -4, -3), w_knight)
white_left_bishop = Bishop("w_l_Bishop", "white", (0, -4, -2), w_bishop)
white_queen = Queen("w_Queen", "white", (0, -4, -1), w_queen)
white_king = King("w_King", "white", (1, -4, 0), w_king)
white_right_bishop = Bishop("w_r_Bishop", "white", (2, -4, 0), w_bishop)
white_right_knight = Knight("w_r_Knight", "white", (3, -4, 0), w_knight)
white_right_rook = Rook("w_r_Rook", "white", (4, -4, 0), w_rook)
white_pawn1 = Pawn("w_1_Pawn", "white", (0, -3, -4), w_pawn)
white_pawn2 = Pawn("w_2_Pawn", "white", (0, -3, -3), w_pawn)
white_pawn3 = Pawn("w_3_Pawn", "white", (0, -3, -2), w_pawn)
white_pawn4 = Pawn("w_4_Pawn", "white", (0, -3, -1), w_pawn)
white_pawn5 = Pawn("w_5_Pawn", "white", (1, -3, 0), w_pawn)
white_pawn6 = Pawn("w_6_Pawn", "white", (2, -3, 0), w_pawn)
white_pawn7 = Pawn("w_7_Pawn", "white", (3, -3, 0), w_pawn)
white_pawn8 = Pawn("w_8_Pawn", "white", (4, -3, 0), w_pawn)

black_left_rook = Rook("b_l_Rook", "black", (-4, 4, 0), b_rook)
black_left_knight = Knight("b_l_Knight", "black", (-4, 3, 0), b_knight)
black_left_bishop = Bishop("b_l_Bishop", "black", (-4, 2, 0), b_bishop)
black_queen = Queen("b_Queen", "black", (-4, 1, 0), b_queen)
black_king = King("b_King", "black", (-4, 0, -1), b_king)
black_right_bishop = Bishop("b_r_Bishop", "black", (-4, 0, -2), b_bishop)
black_right_knight = Knight("b_r_Knight", "black", (-4, 0, -3), b_knight)
black_right_rook = Rook("b_r_Rook", "black", (-4, 0, -4), b_rook)
black_pawn1 = Pawn("b_1_Pawn", "black", (-3, 4, 0), b_pawn)
black_pawn2 = Pawn("b_2_Pawn", "black", (-3, 3, 0), b_pawn)
black_pawn3 = Pawn("b_3_Pawn", "black", (-3, 2, 0), b_pawn)
black_pawn4 = Pawn("b_4_Pawn", "black", (-3, 1, 0), b_pawn)
black_pawn5 = Pawn("b_5_Pawn", "black", (-3, 0, -1), b_pawn)
black_pawn6 = Pawn("b_6_Pawn", "black", (-3, 0, -2), b_pawn)
black_pawn7 = Pawn("b_7_Pawn", "black", (-3, 0, -3), b_pawn)
black_pawn8 = Pawn("b_8_Pawn", "black", (-3, 0, -4), b_pawn)

red_left_rook = Rook("r_l_Rook", "red", (4, 0, 4), r_rook)
red_left_knight = Knight("r_l_Knight", "red", (3, 0, 4), r_knight)
red_left_bishop = Bishop("r_l_Bishop", "red", (2, 0, 4), r_bishop)
red_queen = Queen("r_Queen", "red", (1, 0, 4), r_queen)
red_king = King("r_King", "red", (0, 1, 4), r_king)
red_right_bishop = Bishop("r_r_Bishop", "red", (0, 2, 4), r_bishop)
red_right_knight = Knight("r_r_Knight", "red", (0, 3, 4), r_knight)
red_right_rook = Rook("r_r_Rook", "red", (0, 4, 4), r_rook)
red_pawn1 = Pawn("r_1_Pawn", "red", (4, 0, 3), r_pawn)
red_pawn2 = Pawn("r_2_Pawn", "red", (3, 0, 3), r_pawn)
red_pawn3 = Pawn("r_3_Pawn", "red", (2, 0, 3), r_pawn)
red_pawn4 = Pawn("r_4_Pawn", "red", (1, 0, 3), r_pawn)
red_pawn5 = Pawn("r_5_Pawn", "red", (0, 1, 3), r_pawn)
red_pawn6 = Pawn("r_6_Pawn", "red", (0, 2, 3), r_pawn)
red_pawn7 = Pawn("r_7_Pawn", "red", (0, 3, 3), r_pawn)
red_pawn8 = Pawn("r_8_Pawn", "red", (0, 4, 3), r_pawn)


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
