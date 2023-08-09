from board import board

lst = []
for x in range(-4, 0):
    for cell in board:
        if cell.position[0] == x:
            lst.append(cell)
    lst = sorted(lst, key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else a_cell.position[1])
    print("x" * 100)
    for the_cell in lst:
        print(the_cell.name, the_cell.position)
    lst.clear()

for x in range(1, 5):
    for cell in board:
        if cell.position[0] == x:
            lst.append(cell)
    lst = sorted(lst, key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else a_cell.position[1])
    print("x" * 100)
    for a_cell in lst:
        print(a_cell.name, a_cell.position)
    lst.clear()

print(" " * 500)

for y in range(-4, 0):
    for cell in board:
        if cell.position[1] == y:
            lst.append(cell)
    lst = sorted(lst, key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else a_cell.position[0])
    print("y" * 100)
    for a_cell in lst:
        print(a_cell.name, a_cell.position)
    lst.clear()

for y in range(1, 5):
    for cell in board:
        if cell.position[1] == y:
            lst.append(cell)
    lst = sorted(lst, key=lambda a_cell: a_cell.position[2] if a_cell.position[2] != 0 else a_cell.position[0])
    print("y" * 100)
    for a_cell in lst:
        print(a_cell.name, a_cell.position)
    lst.clear()

print(" " * 500)

for z in range(-4, 0):
    for cell in board:
        if cell.position[2] == z:
            lst.append(cell)
    if z == -3 or z == -1:
        lst = sorted(lst, key=lambda a_cell: a_cell.position[0])
    print("z" * 100)
    for a_cell in lst:
        print(a_cell.name, a_cell.position)
    lst.clear()

for z in range(1, 5):
    for cell in board:
        if cell.position[2] == z:
            lst.append(cell)
    if z == -3 or z == -1:
        lst = sorted(lst, key=lambda a_cell: a_cell.position[0])
    print("z" * 100)
    for a_cell in lst:
        print(a_cell.name, a_cell.position)
    lst.clear()