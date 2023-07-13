import pygame
from os import path

# Path to directory with media files
img_dir = path.join(path.dirname(__file__), "img")

# Chess pieces images load
w_bishop = pygame.image.load(path.join(img_dir, "w_bishop.png")).convert()
w_king = pygame.image.load(path.join(img_dir, "w_king.png")).convert()
w_knight = pygame.image.load(path.join(img_dir, "w_knight.png")).convert()
w_pawn = pygame.image.load(path.join(img_dir, "w_pawn.png")).convert()
w_queen = pygame.image.load(path.join(img_dir, "w_queen.png")).convert()
w_rook = pygame.image.load(path.join(img_dir, "w_rook.png")).convert()

b_bishop = pygame.image.load(path.join(img_dir, "b_bishop.png")).convert()
b_king = pygame.image.load(path.join(img_dir, "b_king.png")).convert()
b_knight = pygame.image.load(path.join(img_dir, "b_knight.png")).convert()
b_pawn = pygame.image.load(path.join(img_dir, "b_pawn.png")).convert()
b_queen = pygame.image.load(path.join(img_dir, "b_queen.png")).convert()
b_rook = pygame.image.load(path.join(img_dir, "b_rook.png")).convert()

r_bishop = pygame.image.load(path.join(img_dir, "r_bishop.png")).convert()
r_king = pygame.image.load(path.join(img_dir, "r_king.png")).convert()
r_knight = pygame.image.load(path.join(img_dir, "r_knight.png")).convert()
r_pawn = pygame.image.load(path.join(img_dir, "r_pawn.png")).convert()
r_queen = pygame.image.load(path.join(img_dir, "r_queen.png")).convert()
r_rook = pygame.image.load(path.join(img_dir, "r_rook.png")).convert()
