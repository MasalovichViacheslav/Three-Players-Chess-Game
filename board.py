import pygame
import numpy as np
from colors import GOLD_LIGHT, GOLD_VERY_DARK


pygame.init()

"""
THREE PLAYERS CHESS BOARD DRAFTING 
Chess board is a set of lines that cross each other in different points and form board cells as shown in image "Chess 
board draft.png" in "supporting materials" directory. Such points and their coordinates are stored in dictionary 
"points_dict". Initial point "p1" has coordinates [x, y].
"""
points_dict = {}
x1 = 300
y1 = 50
points_dict["p1"] = [x1, y1]


# The function calculates coordinates of points that divide a line into 8 equal lines
def line_equal_split(number: int, start_point_coord: list, end_point_coord: list) -> dict:
    """
    Creating "points_dict" copy. If to iterate a dictionary and add new key-value in this dictionary during iteration,
    an error occurs - RuntimeError: dictionary changed size during iteration. That is why in the FOR LOOP below
    dictionary copy is iterated and original dictionary is updated.
    """
    temp_dict = points_dict.copy()
    coord_repeat = 0
    for i in range(1, 8):
        x = start_point_coord[0] + (end_point_coord[0] - start_point_coord[0]) / 8 * i
        y = start_point_coord[1] + (end_point_coord[1] - start_point_coord[1]) / 8 * i
        """
        Checking whether there is a point with [x, y] coordinates in points_dict or not. No need in points with the same
         coordinates but different names in the dictionary (in particular, the talk is about point "p52").
        """
        for key in temp_dict:
            if round(temp_dict[key][0], 5) == round(x, 5) and round(temp_dict[key][1], 5) == round(y, 5):
                coord_repeat = 1
                break
            elif coord_repeat == 0:
                points_dict["p" + str(number + i)] = [x, y]
            else:
                points_dict["p" + str(number + i - 1)] = [x, y]
    return points_dict


# The required length of board game zone side (regular hexagon side)
board_side = 350

"""
For points coordinates calculation the following features of regular hexagon and regular triangle are used:
- regular hexagon is consist of 6 regular equal to each other triangles;
- height of regular triangle is also median of this triangle;
- height of regular triangle is equal to 3**0.5/2 * triangle side
"""
# Calculate coordinates of points on "p1-p9" line. Firstly "p9" point to be added in points_dict.
points_dict["p9"] = [x1 + board_side, y1]
line_equal_split(1, points_dict["p1"], points_dict["p9"])

# Calculate coordinates of points on "p9-p17" line. Firstly "p17" point to be added in points_dict.
# Triangle
points_dict["p17"] = [x1 + board_side * 1.5, y1 + 3 ** 0.5 / 2 * board_side]
line_equal_split(9, points_dict["p9"], points_dict["p17"])

# Calculate coordinates of points on "p17-p25" line. Firstly "p25" point to be added in points_dict.
points_dict["p25"] = [x1 + board_side, y1 + 3 ** 0.5 * board_side]
line_equal_split(17, points_dict["p17"], points_dict["p25"])

# Calculate coordinates of points on "p25-p33" line. Firstly "p33" point to be added in points_dict.
points_dict["p33"] = [x1, y1 + 3 ** 0.5 * board_side]
line_equal_split(25, points_dict["p25"], points_dict["p33"])

# Calculate coordinates of points on "p33-p41" line. Firstly "p41" point to be added in points_dict.
points_dict["p41"] = [x1 - board_side * 0.5, y1 + 3 ** 0.5 / 2 * board_side]
line_equal_split(33, points_dict["p33"], points_dict["p41"])

# Calculate coordinates of points on "p41-p1" line.
line_equal_split(41, points_dict["p41"], points_dict["p1"])

# Calculate coordinates of points on "p5-p29" line.
line_equal_split(48, points_dict["p5"], points_dict["p29"])

# Calculate coordinates of points on "p13-p37" line.
line_equal_split(55, points_dict["p13"], points_dict["p37"])

# Calculate coordinates of points on "p21-p45" line.
line_equal_split(61, points_dict["p21"], points_dict["p45"])

"""
Function "lines_cross_point" calculates coordinates of two lines cross point with usage of numpy "linalg.solve" method.

Example of this method use.
There are two lines defined by two equations mentioned below. Need to calculate coordinates of their cross point.
4x + 3y = 20
-5x + 9y = 26

Solution
>>>import numpy

>>>A = numpy.array([[4, 3], [-5, 9]])
>>>B = numpy.array([20, 26])
>>>coords = numpy.linalg.solve(A, B)
>>>print(coords)
[2. 4.]


Function "lines_cross_point" receives start and end points of two lines as arguments. In order to present a line as 
linear equation based on this line two points the canonical equation of line is used:
(X - Xs) / (Xe - Xs) = (Y - Ys) / (Ye - Ys)
where (Xs, Ys) and (Xe, Ye) are coordinates two points that belongs to the line

The equation can be converted in the following way:
X / (Xe - Xs) - Xs/ (Xe - Xs) = Y / (Ye - Ys) - Ys / (Ye - Ys)
X / (Xe - Xs) - Y / (Ye - Ys) = Xs/ (Xe - Xs) - Ys / (Ye - Ys)
X * (1 / (Xe - Xs)) + Y * ((-1) / (Ye - Ys)) = Xs/ (Xe - Xs) - Ys / (Ye - Ys)  - such form is equal to the leaner
equations shown in the example above.



If any of two lines has equal X or Y values of start and end points, then specified above method will raise 
ZeroDivisionError. In such case cross point coordinates shall be calculated in the following way:

if one line is parallel to Y-axis, it means that all points on a line have the same value of X coordinate, including 
point of cross with another line, accordingly cross point will have the following coordinates:
X = Xvalue
Y = (Xvalue - Xs)(Ye - Ys)/(Xe - Xs) + Ys,
where [Xs, Ys] and [Xe, Ye] are coordinates of two points of another line

if one line is parallel to X-axis, it means that all points on a line have the same value of Y coordinate, including 
point of cross with another line, accordingly cross point will have coordinates:
Y = Yvalue
X = (Yvalue - Ys)(Xe - Xs) / (Ye - Ys) + Xs,
where [Xs, Ys] and [Xe, Ye] are coordinates of two points of another line

Function "lines_cross_point" firstly check whether any of two line has the same X or Y coordinates or not, if yes, it 
calculates cross point coordinates in accordance with logic specified above, if no, use "numpy.linalg.solve" to
calculate coordinates of cross point.  
"""


def lines_cross_point(line1_start: list, line1_end: list, line2_start: list, line2_end: list) -> list:
    if line1_start[0] == line1_end[0]:
        x = line1_start[0]
        y = (x - line2_start[0]) * (line2_end[1] - line2_start[1]) / (line2_end[0] - line2_start[0]) + line2_start[1]
    elif line1_start[1] == line1_end[1]:
        y = line1_start[1]
        x = (y - line2_start[1]) * (line2_end[0] - line2_start[0]) / (line2_end[1] - line2_start[1]) + line2_start[0]
    elif line2_start[0] == line2_end[0]:
        x = line2_start[0]
        y = (x - line1_start[0]) * (line1_end[1] - line1_start[1]) / (line1_end[0] - line1_start[0]) + line1_start[1]
    elif line2_start[1] == line2_end[1]:
        y = line2_start[1]
        x = (y - line1_start[1]) * (line1_end[0] - line1_start[0]) / (line1_end[1] - line1_start[1]) + line1_start[0]
    else:
        a = np.array(
            [[1 / (line1_end[0] - line1_start[0]), (-1) / (line1_end[1] - line1_start[1])],
             [1 / (line2_end[0] - line2_start[0]), (-1) / (line2_end[1] - line2_start[1])]]
        )
        b = np.array(
        [[line1_start[0] / (line1_end[0] - line1_start[0]) - line1_start[1] / (line1_end[1] - line1_start[1])],
         [line2_start[0] / (line2_end[0] - line2_start[0]) - line2_start[1] / (line2_end[1] - line2_start[1])]]
        )
        x = float(np.linalg.solve(a, b)[0])
        y = float(np.linalg.solve(a, b)[1])
    return [x, y]


# Calculation of points coordinates from point "p68" up to point "p121"
# Points inside of quadrangle p1-p5-p52-p45
points_dict["p68"] = lines_cross_point(points_dict["p2"], points_dict["p67"], points_dict["p48"], points_dict["p49"])
points_dict["p69"] = lines_cross_point(points_dict["p3"], points_dict["p66"], points_dict["p48"], points_dict["p49"])
points_dict["p70"] = lines_cross_point(points_dict["p4"], points_dict["p65"], points_dict["p48"], points_dict["p49"])

points_dict["p71"] = lines_cross_point(points_dict["p2"], points_dict["p67"], points_dict["p47"], points_dict["p50"])
points_dict["p72"] = lines_cross_point(points_dict["p3"], points_dict["p66"], points_dict["p47"], points_dict["p50"])
points_dict["p73"] = lines_cross_point(points_dict["p4"], points_dict["p65"], points_dict["p47"], points_dict["p50"])

points_dict["p74"] = lines_cross_point(points_dict["p2"], points_dict["p67"], points_dict["p46"], points_dict["p51"])
points_dict["p75"] = lines_cross_point(points_dict["p3"], points_dict["p66"], points_dict["p46"], points_dict["p51"])
points_dict["p76"] = lines_cross_point(points_dict["p4"], points_dict["p65"], points_dict["p46"], points_dict["p51"])


# Points inside of quadrangle p5-p9-p13-p52
points_dict["p77"] = lines_cross_point(points_dict["p6"], points_dict["p58"], points_dict["p10"], points_dict["p49"])
points_dict["p78"] = lines_cross_point(points_dict["p7"], points_dict["p57"], points_dict["p10"], points_dict["p49"])
points_dict["p79"] = lines_cross_point(points_dict["p8"], points_dict["p56"], points_dict["p10"], points_dict["p49"])

points_dict["p80"] = lines_cross_point(points_dict["p6"], points_dict["p58"], points_dict["p11"], points_dict["p50"])
points_dict["p81"] = lines_cross_point(points_dict["p7"], points_dict["p57"], points_dict["p11"], points_dict["p50"])
points_dict["p82"] = lines_cross_point(points_dict["p8"], points_dict["p56"], points_dict["p11"], points_dict["p50"])

points_dict["p83"] = lines_cross_point(points_dict["p6"], points_dict["p58"], points_dict["p12"], points_dict["p51"])
points_dict["p84"] = lines_cross_point(points_dict["p7"], points_dict["p57"], points_dict["p12"], points_dict["p51"])
points_dict["p85"] = lines_cross_point(points_dict["p8"], points_dict["p56"], points_dict["p12"], points_dict["p51"])


# Points inside of quadrangle p13-p17-p21-p52
points_dict["p86"] = lines_cross_point(points_dict["p58"], points_dict["p20"], points_dict["p14"], points_dict["p64"])
points_dict["p87"] = lines_cross_point(points_dict["p57"], points_dict["p19"], points_dict["p14"], points_dict["p64"])
points_dict["p88"] = lines_cross_point(points_dict["p56"], points_dict["p18"], points_dict["p14"], points_dict["p64"])

points_dict["p89"] = lines_cross_point(points_dict["p58"], points_dict["p20"], points_dict["p15"], points_dict["p63"])
points_dict["p90"] = lines_cross_point(points_dict["p57"], points_dict["p19"], points_dict["p15"], points_dict["p63"])
points_dict["p91"] = lines_cross_point(points_dict["p56"], points_dict["p18"], points_dict["p15"], points_dict["p63"])

points_dict["p92"] = lines_cross_point(points_dict["p58"], points_dict["p20"], points_dict["p16"], points_dict["p62"])
points_dict["p93"] = lines_cross_point(points_dict["p57"], points_dict["p19"], points_dict["p16"], points_dict["p62"])
points_dict["p94"] = lines_cross_point(points_dict["p56"], points_dict["p18"], points_dict["p16"], points_dict["p62"])


# Points inside of quadrangle p21-p25-p29-p52
points_dict["p95"] = lines_cross_point(points_dict["p64"], points_dict["p28"], points_dict["p22"], points_dict["p53"])
points_dict["p96"] = lines_cross_point(points_dict["p63"], points_dict["p27"], points_dict["p22"], points_dict["p53"])
points_dict["p97"] = lines_cross_point(points_dict["p62"], points_dict["p26"], points_dict["p22"], points_dict["p53"])

points_dict["p98"] = lines_cross_point(points_dict["p64"], points_dict["p28"], points_dict["p23"], points_dict["p54"])
points_dict["p99"] = lines_cross_point(points_dict["p63"], points_dict["p27"], points_dict["p23"], points_dict["p54"])
points_dict["p100"] = lines_cross_point(points_dict["p62"], points_dict["p26"], points_dict["p23"], points_dict["p54"])

points_dict["p101"] = lines_cross_point(points_dict["p64"], points_dict["p28"], points_dict["p24"], points_dict["p55"])
points_dict["p102"] = lines_cross_point(points_dict["p63"], points_dict["p27"], points_dict["p24"], points_dict["p55"])
points_dict["p103"] = lines_cross_point(points_dict["p62"], points_dict["p26"], points_dict["p24"], points_dict["p55"])


# Points inside of quadrangle p29-p33-p37-p52
points_dict["p104"] = lines_cross_point(points_dict["p61"], points_dict["p32"], points_dict["p36"], points_dict["p53"])
points_dict["p105"] = lines_cross_point(points_dict["p60"], points_dict["p31"], points_dict["p36"], points_dict["p53"])
points_dict["p106"] = lines_cross_point(points_dict["p59"], points_dict["p30"], points_dict["p36"], points_dict["p53"])

points_dict["p107"] = lines_cross_point(points_dict["p61"], points_dict["p32"], points_dict["p35"], points_dict["p54"])
points_dict["p108"] = lines_cross_point(points_dict["p60"], points_dict["p31"], points_dict["p35"], points_dict["p54"])
points_dict["p109"] = lines_cross_point(points_dict["p59"], points_dict["p30"], points_dict["p35"], points_dict["p54"])

points_dict["p110"] = lines_cross_point(points_dict["p61"], points_dict["p32"], points_dict["p34"], points_dict["p55"])
points_dict["p111"] = lines_cross_point(points_dict["p60"], points_dict["p31"], points_dict["p34"], points_dict["p55"])
points_dict["p112"] = lines_cross_point(points_dict["p59"], points_dict["p30"], points_dict["p34"], points_dict["p55"])


# Points inside of quadrangle p37-p41-p45-p52
points_dict["p113"] = lines_cross_point(points_dict["p67"], points_dict["p40"], points_dict["p44"], points_dict["p59"])
points_dict["p114"] = lines_cross_point(points_dict["p66"], points_dict["p39"], points_dict["p44"], points_dict["p59"])
points_dict["p115"] = lines_cross_point(points_dict["p65"], points_dict["p38"], points_dict["p44"], points_dict["p59"])

points_dict["p116"] = lines_cross_point(points_dict["p67"], points_dict["p40"], points_dict["p43"], points_dict["p60"])
points_dict["p117"] = lines_cross_point(points_dict["p66"], points_dict["p39"], points_dict["p43"], points_dict["p60"])
points_dict["p118"] = lines_cross_point(points_dict["p65"], points_dict["p38"], points_dict["p43"], points_dict["p60"])

points_dict["p119"] = lines_cross_point(points_dict["p67"], points_dict["p40"], points_dict["p42"], points_dict["p61"])
points_dict["p120"] = lines_cross_point(points_dict["p66"], points_dict["p39"], points_dict["p42"], points_dict["p61"])
points_dict["p121"] = lines_cross_point(points_dict["p65"], points_dict["p38"], points_dict["p42"], points_dict["p61"])


"""
BOARD FRAME DRAFTING.
The width of board frame is "frame_width". As angle points (coordinates) of game zone hexagon are already calculated and 
frame_width is assigned, it's possible to calculate angle points (coordinates) of board frame.

Triangle p1-p122-tp03 is regular. Line p1-tp02 is height, median of the triangle and "frame_width".
Height of regular triangle is equal to 3**0.5/2 * triangle side.  
"""
frame_width = 35

# Adding board frame angle points to "points_dict"
points_dict["p122"] = [points_dict["p1"][0] - frame_width / 3 ** 0.5, points_dict["p1"][1] - frame_width]
points_dict["p123"] = [points_dict["p9"][0] + frame_width / 3 ** 0.5, points_dict["p9"][1] - frame_width]
points_dict["p124"] = [points_dict["p17"][0] + frame_width * 2 / 3 ** 0.5, points_dict["p17"][1]]
points_dict["p125"] = [points_dict["p25"][0] + frame_width / 3 ** 0.5, points_dict["p25"][1] + frame_width]
points_dict["p126"] = [points_dict["p33"][0] - frame_width / 3 ** 0.5, points_dict["p33"][1] + frame_width]
points_dict["p127"] = [points_dict["p41"][0] - frame_width * 2 / 3 ** 0.5, points_dict["p41"][1]]


dark_color = GOLD_VERY_DARK
light_color = GOLD_LIGHT


class BoardCell:
    def __init__(self, cell_name: str, xyz_coordinates: list, status: bool, points: tuple, color: tuple):
        self.name = cell_name
        self.position = xyz_coordinates
        self.occupied = status
        self.points = points
        self.initial_color = color
        self.current_color = self.initial_color


    def cell_draw(self, surface):
        self.rect = pygame.draw.polygon(surface, self.current_color, self.points)


board = []

# Adding BoardCell objects (cells) from section a1-h4 into "board"
board.append(BoardCell("a1", [0, -4, -4], True,
                       (points_dict["p33"], points_dict["p34"], points_dict["p110"], points_dict["p32"]), dark_color))
board.append(BoardCell("a2", [0, -3, -4], True,
                       (points_dict["p34"], points_dict["p35"], points_dict["p107"], points_dict["p110"]), light_color))
board.append(BoardCell("a3", [0, -2, -4], False,
                       (points_dict["p35"], points_dict["p36"], points_dict["p104"], points_dict["p107"]), dark_color))
board.append(BoardCell("a4", [0, -1, -4], False,
                       (points_dict["p36"], points_dict["p37"], points_dict["p61"], points_dict["p104"]), light_color))


board.append(BoardCell("b4", [0, -1, -3], False,
                       (points_dict["p105"], points_dict["p104"], points_dict["p61"], points_dict["p60"]), dark_color))
board.append(BoardCell("b3", [0, -2, -3], False,
                       (points_dict["p108"], points_dict["p107"], points_dict["p104"], points_dict["p105"]),
                       light_color))
board.append(BoardCell("b2", [0, -3, -3], True,
                       (points_dict["p111"], points_dict["p110"], points_dict["p107"], points_dict["p108"]),
                       dark_color))
board.append(BoardCell("b1", [0, -4, -3], True,
                       (points_dict["p31"], points_dict["p32"], points_dict["p110"], points_dict["p111"]), light_color))


board.append(BoardCell("c1", [0, -4, -2], True,
                       (points_dict["p30"], points_dict["p31"], points_dict["p111"], points_dict["p112"]), dark_color))
board.append(BoardCell("c2", [0, -3, -2], True,
                       (points_dict["p112"], points_dict["p111"], points_dict["p108"], points_dict["p109"]),
                       light_color))
board.append(BoardCell("c3", [0, -2, -2], False,
                       (points_dict["p109"], points_dict["p108"], points_dict["p105"], points_dict["p106"]),
                       dark_color))
board.append(BoardCell("c4", [0, -1, -2], False,
                       (points_dict["p106"], points_dict["p105"], points_dict["p60"], points_dict["p59"]), light_color))


board.append(BoardCell("d4", [0, -1, -1], False,
                       (points_dict["p52"], points_dict["p59"], points_dict["p106"], points_dict["p53"]), dark_color))
board.append(BoardCell("d3", [0, -2, -1], False,
                       (points_dict["p53"], points_dict["p106"], points_dict["p109"], points_dict["p54"]), light_color))
board.append(BoardCell("d2", [0, -3, -1], True,
                       (points_dict["p54"], points_dict["p109"], points_dict["p112"], points_dict["p55"]), dark_color))
board.append(BoardCell("d1", [0, -4, -1], True,
                       (points_dict["p55"], points_dict["p112"], points_dict["p30"], points_dict["p29"]), light_color))


board.append(BoardCell("e1", [1, -4, 0], True,
                       (points_dict["p28"], points_dict["p29"], points_dict["p55"], points_dict["p101"]), dark_color))
board.append(BoardCell("e2", [1, -3, 0], True,
                       (points_dict["p101"], points_dict["p55"], points_dict["p54"], points_dict["p98"]), light_color))
board.append(BoardCell("e3", [1, -2, 0], False,
                       (points_dict["p98"], points_dict["p54"], points_dict["p53"], points_dict["p95"]), dark_color))
board.append(BoardCell("e4", [1, -1, 0], False,
                       (points_dict["p95"], points_dict["p53"], points_dict["p52"], points_dict["p64"]), light_color))


board.append(BoardCell("f4", [2, -1, 0], False,
                       (points_dict["p63"], points_dict["p64"], points_dict["p95"], points_dict["p96"]), dark_color))
board.append(BoardCell("f3", [2, -2, 0], False,
                       (points_dict["p96"], points_dict["p95"], points_dict["p98"], points_dict["p99"]), light_color))
board.append(BoardCell("f2", [2, -3, 0], True,
                       (points_dict["p99"], points_dict["p98"], points_dict["p101"], points_dict["p102"]), dark_color))
board.append(BoardCell("f1", [2, -4, 0], True,
                       (points_dict["p102"], points_dict["p101"], points_dict["p28"], points_dict["p27"]), light_color))


board.append(BoardCell("g1", [3, -4, 0], True,
                       (points_dict["p26"], points_dict["p27"], points_dict["p102"], points_dict["p103"]), dark_color))
board.append(BoardCell("g2", [3, -3, 0], True,
                       (points_dict["p103"], points_dict["p102"], points_dict["p99"], points_dict["p100"]),
                       light_color))
board.append(BoardCell("g3", [3, -2, 0], False,
                       (points_dict["p100"], points_dict["p99"], points_dict["p96"], points_dict["p97"]), dark_color))
board.append(BoardCell("g4", [3, -1, 0], False,
                       (points_dict["p97"], points_dict["p96"], points_dict["p63"], points_dict["p62"]), light_color))


board.append(BoardCell("h4", [4, -1, 0], False,
                       (points_dict["p21"], points_dict["p62"], points_dict["p97"], points_dict["p22"]), dark_color))
board.append(BoardCell("h3", [4, -2, 0], False,
                       (points_dict["p22"], points_dict["p97"], points_dict["p100"], points_dict["p23"]), light_color))
board.append(BoardCell("h2", [4, -3, 0], True,
                       (points_dict["p23"], points_dict["p100"], points_dict["p103"], points_dict["p24"]), dark_color))
board.append(BoardCell("h1", [4, -4, 0], True,
                       (points_dict["p24"], points_dict["p103"], points_dict["p26"], points_dict["p25"]), light_color))


# Adding BoardCell objects (cells) from section l8-a5 into "board"
board.append(BoardCell("l8", [-4, 4, 0], True,
                       (points_dict["p1"], points_dict["p2"], points_dict["p68"], points_dict["p48"]), dark_color))
board.append(BoardCell("l7", [-3, 4, 0], True,
                       (points_dict["p2"], points_dict["p3"], points_dict["p69"], points_dict["p68"]), light_color))
board.append(BoardCell("l6", [-2, 4, 0], False,
                       (points_dict["p3"], points_dict["p4"], points_dict["p70"], points_dict["p69"]), dark_color))
board.append(BoardCell("l5", [-1, 4, 0], False,
                       (points_dict["p4"], points_dict["p5"], points_dict["p49"], points_dict["p70"]), light_color))


board.append(BoardCell("k5", [-1, 3, 0], False,
                       (points_dict["p49"], points_dict["p70"], points_dict["p73"], points_dict["p50"]), dark_color))
board.append(BoardCell("k6", [-2, 3, 0], False,
                       (points_dict["p70"], points_dict["p69"], points_dict["p72"], points_dict["p73"]), light_color))
board.append(BoardCell("k7", [-3, 3, 0], True,
                       (points_dict["p69"], points_dict["p68"], points_dict["p71"], points_dict["p72"]), dark_color))
board.append(BoardCell("k8", [-4, 3, 0], True,
                       (points_dict["p68"], points_dict["p48"], points_dict["p47"], points_dict["p71"]), light_color))


board.append(BoardCell("j8", [-4, 2, 0], True,
                       (points_dict["p47"], points_dict["p71"], points_dict["p74"], points_dict["p46"]), dark_color))
board.append(BoardCell("j7", [-3, 2, 0], True,
                       (points_dict["p71"], points_dict["p72"], points_dict["p75"], points_dict["p74"]), light_color))
board.append(BoardCell("j6", [-2, 2, 0], False,
                       (points_dict["p72"], points_dict["p73"], points_dict["p76"], points_dict["p75"]), dark_color))
board.append(BoardCell("j5", [-1, 2, 0], False,
                       (points_dict["p73"], points_dict["p50"], points_dict["p51"], points_dict["p76"]), light_color))


board.append(BoardCell("i5", [-1, 1, 0], False,
                       (points_dict["p51"], points_dict["p76"], points_dict["p65"], points_dict["p52"]), dark_color))
board.append(BoardCell("i6", [-2, 1, 0], False,
                       (points_dict["p76"], points_dict["p75"], points_dict["p66"], points_dict["p65"]), light_color))
board.append(BoardCell("i7", [-3, 1, 0], True,
                       (points_dict["p75"], points_dict["p74"], points_dict["p67"], points_dict["p66"]), dark_color))
board.append(BoardCell("i8", [-4, 1, 0], True,
                       (points_dict["p74"], points_dict["p46"], points_dict["p45"], points_dict["p67"]), light_color))


board.append(BoardCell("d8", [-4, 0, -1], True,
                       (points_dict["p45"], points_dict["p67"], points_dict["p113"], points_dict["p44"]), dark_color))
board.append(BoardCell("d7", [-3, 0, -1], True,
                       (points_dict["p67"], points_dict["p66"], points_dict["p114"], points_dict["p113"]), light_color))
board.append(BoardCell("d6", [-2, 0, -1], False,
                       (points_dict["p66"], points_dict["p65"], points_dict["p115"], points_dict["p114"]), dark_color))
board.append(BoardCell("d5", [-1, 0, -1], False,
                       (points_dict["p65"], points_dict["p52"], points_dict["p59"], points_dict["p115"]), light_color))


board.append(BoardCell("c5", [-1, 0, -2], False,
                       (points_dict["p59"], points_dict["p115"], points_dict["p118"], points_dict["p60"]), dark_color))
board.append(BoardCell("c6", [-2, 0, -2], False,
                       (points_dict["p115"], points_dict["p114"], points_dict["p117"], points_dict["p118"]),
                       light_color))
board.append(BoardCell("c7", [-3, 0, -2], True,
                       (points_dict["p114"], points_dict["p113"], points_dict["p116"], points_dict["p117"]),
                       dark_color))
board.append(BoardCell("c8", [-4, 0, -2], True,
                       (points_dict["p113"], points_dict["p44"], points_dict["p43"], points_dict["p116"]), light_color))


board.append(BoardCell("b8", [-4, 0, -3], True,
                       (points_dict["p43"], points_dict["p116"], points_dict["p119"], points_dict["p42"]), dark_color))
board.append(BoardCell("b7", [-3, 0, -3], True,
                       (points_dict["p116"], points_dict["p117"], points_dict["p120"], points_dict["p119"]),
                       light_color))
board.append(BoardCell("b6", [-2, 0, -3], False,
                       (points_dict["p117"], points_dict["p118"], points_dict["p121"], points_dict["p120"]),
                       dark_color))
board.append(BoardCell("b5", [-1, 0, -3], False,
                       (points_dict["p118"], points_dict["p60"], points_dict["p61"], points_dict["p121"]), light_color))


board.append(BoardCell("a5", [-1, 0, -4], False,
                       (points_dict["p61"], points_dict["p121"], points_dict["p38"], points_dict["p37"]), dark_color))
board.append(BoardCell("a6", [-2, 0, -4], False,
                       (points_dict["p121"], points_dict["p120"], points_dict["p39"], points_dict["p38"]), light_color))
board.append(BoardCell("a7", [-3, 0, -4], True,
                       (points_dict["p120"], points_dict["p119"], points_dict["p40"], points_dict["p39"]), dark_color))
board.append(BoardCell("a8", [-4, 0, -4], True,
                       (points_dict["p119"], points_dict["p42"], points_dict["p41"], points_dict["p40"]), light_color))


# Adding BoardCell objects (cells) from section h12-l9 into "board"
board.append(BoardCell("h12", [4, 0, 4], True,
                       (points_dict["p17"], points_dict["p18"], points_dict["p94"], points_dict["p16"]), dark_color))
board.append(BoardCell("h11", [4, 0, 3], True,
                       (points_dict["p18"], points_dict["p19"], points_dict["p93"], points_dict["p94"]), light_color))
board.append(BoardCell("h10", [4, 0, 2], False,
                       (points_dict["p19"], points_dict["p20"], points_dict["p92"], points_dict["p93"]), dark_color))
board.append(BoardCell("h9", [4, 0, 1], False,
                       (points_dict["p20"], points_dict["p21"], points_dict["p62"], points_dict["p92"]), light_color))


board.append(BoardCell("g9", [3, 0, 1], False,
                       (points_dict["p92"], points_dict["p62"], points_dict["p63"], points_dict["p89"]), dark_color))
board.append(BoardCell("g10", [3, 0, 2], False,
                       (points_dict["p93"], points_dict["p92"], points_dict["p89"], points_dict["p90"]), light_color))
board.append(BoardCell("g11", [3, 0, 3], True,
                       (points_dict["p94"], points_dict["p93"], points_dict["p90"], points_dict["p91"]), dark_color))
board.append(BoardCell("g12", [3, 0, 4], True,
                       (points_dict["p16"], points_dict["p94"], points_dict["p91"], points_dict["p15"]), light_color))


board.append(BoardCell("f12", [2, 0, 4], True,
                       (points_dict["p15"], points_dict["p91"], points_dict["p88"], points_dict["p14"]), dark_color))
board.append(BoardCell("f11", [2, 0, 3], True,
                       (points_dict["p91"], points_dict["p90"], points_dict["p87"], points_dict["p88"]), light_color))
board.append(BoardCell("f10", [2, 0, 2], False,
                       (points_dict["p90"], points_dict["p89"], points_dict["p86"], points_dict["p87"]), dark_color))
board.append(BoardCell("f9", [2, 0, 1], False,
                       (points_dict["p89"], points_dict["p63"], points_dict["p64"], points_dict["p86"]), light_color))


board.append(BoardCell("e9", [1, 0, 1], False,
                       (points_dict["p86"], points_dict["p64"], points_dict["p52"], points_dict["p58"]), dark_color))
board.append(BoardCell("e10", [1, 0, 2], False,
                       (points_dict["p87"], points_dict["p86"], points_dict["p58"], points_dict["p57"]), light_color))
board.append(BoardCell("e11", [1, 0, 3], True,
                       (points_dict["p88"], points_dict["p87"], points_dict["p57"], points_dict["p56"]), dark_color))
board.append(BoardCell("e12", [1, 0, 4], True,
                       (points_dict["p14"], points_dict["p88"], points_dict["p56"], points_dict["p13"]), light_color))


board.append(BoardCell("i12", [0, 1, 4], True,
                       (points_dict["p13"], points_dict["p56"], points_dict["p85"], points_dict["p12"]), dark_color))
board.append(BoardCell("i11", [0, 1, 3], True,
                       (points_dict["p56"], points_dict["p57"], points_dict["p84"], points_dict["p85"]), light_color))
board.append(BoardCell("i10", [0, 1, 2], False,
                       (points_dict["p57"], points_dict["p58"], points_dict["p83"], points_dict["p84"]), dark_color))
board.append(BoardCell("i9", [0, 1, 1], False,
                       (points_dict["p58"], points_dict["p52"], points_dict["p51"], points_dict["p83"]), light_color))


board.append(BoardCell("j9", [0, 2, 1], False,
                       (points_dict["p83"], points_dict["p51"], points_dict["p50"], points_dict["p80"]), dark_color))
board.append(BoardCell("j10", [0, 2, 2], False,
                       (points_dict["p84"], points_dict["p83"], points_dict["p80"], points_dict["p81"]), light_color))
board.append(BoardCell("j11", [0, 2, 3], True,
                       (points_dict["p85"], points_dict["p84"], points_dict["p81"], points_dict["p82"]), dark_color))
board.append(BoardCell("j12", [0, 2, 4], True,
                       (points_dict["p12"], points_dict["p85"], points_dict["p82"], points_dict["p11"]), light_color))


board.append(BoardCell("k12", [0, 3, 4], True,
                       (points_dict["p11"], points_dict["p82"], points_dict["p79"], points_dict["p10"]), dark_color))
board.append(BoardCell("k11", [0, 3, 3], True,
                       (points_dict["p82"], points_dict["p81"], points_dict["p78"], points_dict["p79"]), light_color))
board.append(BoardCell("k10", [0, 3, 2], False,
                       (points_dict["p81"], points_dict["p80"], points_dict["p77"], points_dict["p78"]), dark_color))
board.append(BoardCell("i9", [0, 3, 1], False,
                       (points_dict["p80"], points_dict["p50"], points_dict["p49"], points_dict["p77"]), light_color))


board.append(BoardCell("l9", [0, 4, 1], False,
                       (points_dict["p77"], points_dict["p49"], points_dict["p5"], points_dict["p6"]), dark_color))
board.append(BoardCell("l10", [0, 4, 2], False,
                       (points_dict["p78"], points_dict["p77"], points_dict["p6"], points_dict["p7"]), light_color))
board.append(BoardCell("l11", [0, 4, 3], True,
                       (points_dict["p79"], points_dict["p78"], points_dict["p7"], points_dict["p8"]), dark_color))
board.append(BoardCell("l12", [0, 4, 4], True,
                       (points_dict["p10"], points_dict["p79"], points_dict["p8"], points_dict["p9"]), light_color))


# Board frame letters and digits
font_size = 16
path_to_font = pygame.font.match_font('arial', bold=True)
font_to_be_used = pygame.font.Font(path_to_font, font_size)


def draw_symbol(symbols: tuple, rotation: int, color: tuple, surface: object, coords: list):
    for index in range(len(symbols)):
        symbol_surface = font_to_be_used.render(symbols[index], True, color)
        symbol_surface = pygame.transform.rotate(symbol_surface, rotation)
        symbol_rect = symbol_surface.get_rect()
        symbol_rect.center = coords[index]
        surface.blit(symbol_surface, symbol_rect)


'''
Function rect_center_coords calculates coordinates of a point that is a center of corresponding symbol rectangle 
(symbol_rect.center) and end them into the lsit. Calculation is made based on already calculated coordinates of two 
nearby points. Below the logic of coordinates calculation is shown for symbol "L" nearby points "p9" and "p10" (check 
"Chess board draft.png" in "supporting materials" directory. For other symbols to be drawn the logic similar.


Calculation of point "TP07" coordinates is made based on geometric features:

1) lines p8-p9 and TP04-TP06 are parallel, angel p8-p9-p10 is regular hexagon inner angle and is equal to 120 degrees,
accordingly angle p10-TP05-TP04 is equal to 60 degrees, as well as angle p10-TP05-TP06;

2) line TP07-TP05 is  equal to a half of the board frame width (frame_width), also line TP07-TP05 is perpendicular and 
median of line p9-10; as angle p10-TP05-TP06 is equal to 60 degrees and andle TP07-TP05-p10 is equal to 90 degrees,
accordingly angle TP07-TP05-TP06 is equal to 30 degrees;

3) line TP07-TP06 is perpendicular to the line TP06-TP05, accordingly triangle TP07-TP06-TP05 is right triangle with  
angle TP07-TP05-TP06 equal to 30 degrees;

4) as line TP07-TP05 is median of line p9-10, point TP05 divides into two equal parts and it has the following 
coordinates:
X(tp05) = X(p9) + (X(p10) - X(p9)) / 2
Y(tp05) = Y(p9) + (Y(p10) - Y(p9)) / 2

5) coordinates of TP07 are equal to:
X(tp07) = X(tp05) + TP05-TP06 line length
Y(tp07) = Y(tp05) + TP07-TP06 line length

6) TP07-TP05 is hypotenuse of triangle TP07-TP06-TP05, angle TP07-TP05-TP06 is equal to 30 degrees, accordingly:
TP05-TP06 = TP07-TP05 * cos 30 (cos 30 is equal to 3**0.5/2)
TP07-TP06 = TP07-TP05 * sin 30 (sin 30 is equal to 0.5)     
'''


def rect_center_coords(rects_center_coords_lst: list, points_coords: list) -> list:
    for index in range(len(points_coords) - 1):
        if index < 8:
            x = points_coords[index][0] + (points_coords[index + 1][0] - points_coords[index][0]) / 2
            y = points_coords[index][1] - frame_width / 2
        elif 8 <= index < 16:
            x = points_coords[index][0] + (
                        points_coords[index + 1][0] - points_coords[index][0]) / 2 + frame_width / 2 * 3 ** 0.5 / 2
            y = points_coords[index][1] + (
                        points_coords[index + 1][1] - points_coords[index][1]) / 2 - frame_width / 2 * 0.5
        elif 16 <= index < 24:
            x = points_coords[index][0] + (
                        points_coords[index + 1][0] - points_coords[index][0]) / 2 + frame_width / 2 * 3 ** 0.5 / 2
            y = points_coords[index][1] + (
                        points_coords[index + 1][1] - points_coords[index][1]) / 2 + frame_width / 2 * 0.5
        elif 24 <= index < 32:
            x = points_coords[index][0] + (points_coords[index + 1][0] - points_coords[index][0]) / 2
            y = points_coords[index][1] + frame_width / 2
        elif 32 <= index < 40:
            x = points_coords[index][0] + (
                        points_coords[index + 1][0] - points_coords[index][0]) / 2 - frame_width / 2 * 3 ** 0.5 / 2
            y = points_coords[index][1] + (
                        points_coords[index + 1][1] - points_coords[index][1]) / 2 + frame_width / 2 * 0.5
        else:
            x = points_coords[index][0] + (
                        points_coords[index + 1][0] - points_coords[index][0]) / 2 - frame_width / 2 * 3 ** 0.5 / 2
            y = points_coords[index][1] + (
                        points_coords[index + 1][1] - points_coords[index][1]) / 2 - frame_width / 2 * 0.5
        rects_center_coords_lst.append([x, y])
    return rects_center_coords_lst