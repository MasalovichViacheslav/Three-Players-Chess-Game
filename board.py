import pygame
import numpy as np

"""
THREE PLAYERS CHESS BOARD DRAFTING 
Chess board game zone is a set of lines that cross each other in different points and form board cells as shown in 
image "Chess board draft.png" in "supporting materials" directory. Such points and their coordinates are stored in
dictionary "points_dict". Initial point "p1" has coordinates [x, y].
"""
points_dict = {}
x1 = 300
y1 = 50
points_dict["p1"] = [x1, y1]


# The function calculates coordinates of points that divide a line into 8 equal lines
def line_equal_split(number: int, start_point_coord: list, end_point_coord: list) -> dict:
    global points_dict
    """
    Creation of points_dict copy. If to iterate a dictionary and add new key-value in this dictionary, an error occurs -
    RuntimeError: dictionary changed size during iteration. That is why in the FOR LOOP below dictionary copy is 
    iterated and original dictionary is updated.
    """
    temp_dict = points_dict.copy()
    coord_repeat = 0
    for i in range(1, 8):
        x = start_point_coord[0] + (end_point_coord[0] - start_point_coord[0]) / 8 * i
        y = start_point_coord[1] + (end_point_coord[1] - start_point_coord[1]) / 8 * i
        """
        Checking whether there is a point with [x, y] coordinates in points_dict or not. No need in the points with 
        the same coordinates but different names in the dictionary.
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
For points coordinates calculation features of regular hexagon and regular triangle are used:
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
"""


def lines_cross_point(line1_start: list, line1_end: list, line2_start: list, line2_end: list) -> list:
    a = np.array(
        [[1 / (line1_end[0] - line1_start[0]), (-1) / (line1_end[1] - line1_start[1])],
         [1 / (line2_end[0] - line2_start[0]), (-1) / (line2_end[1] - line2_start[1])]]
    )
    b = np.array(
        [[line1_start[0] / (line1_end[0] - line1_start[0]) - line1_start[1] / (line1_end[1] - line1_start[1])],
         [line2_start[0] / (line2_end[0] - line2_start[0]) - line2_start[1] / (line2_end[1] - line2_start[1])]]
    )
    return [float(np.linalg.solve(a, b)[0]), float(np.linalg.solve(a, b)[1])]


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

Triangle p1-p122-tp03 is regualar. Line p1-tp02 is height, median of the triangle and "frame_width".
Height of regular triangle is equal to 3**0.5/2 * triangle side.  
"""
frame_width = 40

# Adding new points to "points_dict"
points_dict["p122"] = [points_dict["p1"][0] - frame_width / 3 ** 0.5, points_dict["p1"][1] - frame_width]
points_dict["p123"] = [points_dict["p9"][0] + frame_width / 3 ** 0.5, points_dict["p9"][1] - frame_width]
points_dict["p124"] = [points_dict["p17"][0] + frame_width * 2 / 3 ** 0.5, points_dict["p17"][1]]
points_dict["p125"] = [points_dict["p25"][0] + frame_width / 3 ** 0.5, points_dict["p25"][1] + frame_width]
points_dict["p126"] = [points_dict["p33"][0] - frame_width / 3 ** 0.5, points_dict["p33"][1] + frame_width]
points_dict["p127"] = [points_dict["p41"][0] - frame_width * 2 / 3 ** 0.5, points_dict["p41"][1]]


class BoardCell(pygame.sprite.Sprite):
    pass
