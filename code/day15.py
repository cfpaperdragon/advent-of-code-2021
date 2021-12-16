# day15
import common
import matrix as mat


def create_grid_cell(value):
    return (int(value), 0)


def traverse_matrix_v2(matrix, start_position, steps):
    count_steps = 0
    max_x = max(matrix[0].keys())
    max_y = max(matrix.keys())
    positions = [start_position]
    while len(positions) > 0:
        count_steps += 1
        new_positions = []
        for position in positions:
            current_risk = mat.get_value(matrix, position[0], position[1], lambda a: a[1])
            adjacents = mat.get_adjacents(position[0], position[1], max_x, max_y) # no diagonals
            for a in adjacents:
                if a[0] == 0 and a[1] == 0:
                    continue # skip start position
                risk = mat.get_value(matrix, a[0], a[1])
                if risk[1] != 0: # it was already  updated
                    if current_risk + risk[0] > risk[1]:
                        continue
                mat.set_value(matrix, a[0], a[1], (risk[0], current_risk + risk[0]))
                if a not in new_positions:
                    new_positions.append(a)
        positions = new_positions
    return mat.get_value(matrix, max_x, max_y, lambda a: a[1])


def calculate_part1():
    matrix = mat.read_input_to_matrix("input//day15//input.txt", create_grid_cell)
    result = traverse_matrix_v2(matrix, (0, 0), 20)
    # mat.print_matrix(matrix)
    print(result)


def calculate_new_value(value, iteration):
    new_value = value + iteration
    if new_value > 9:
        new_value -= 9
    return new_value


def fill_mega_matrix(mega_matrix, matrix):
    length_matrix_x = len(matrix[0].keys())
    length_matrix_y = len(matrix.keys())
    for y in matrix.keys():
        for x in matrix[y].keys():
            value = mat.get_value(matrix, x, y)
            for a in range(5):
                for b in range(5):
                    mat.set_value(mega_matrix, x + b*length_matrix_x, y + a*length_matrix_y, (calculate_new_value(value[0], a+b), 0))
# mega matrix doesn't work
# need to do 1 matrix at a time, with borders flowing to the next one

def traverse_matrix_v3(matrix, start_position, min_x, min_y, max_x, max_y):
    count_steps = 0
    positions = [start_position]
    while len(positions) > 0:
        count_steps += 1
        new_positions = []
        # print("step", count_steps, "positions", positions)
        for position in positions:
            current_risk = mat.get_value(matrix, position[0], position[1], lambda a: a[1])
            adjacents = mat.get_adjacents(position[0], position[1], max_x, max_y, False, min_x, min_y) # no diagonals
            for a in adjacents:
                # print(a)
                if a[0] == start_position[0] and a[1] == start_position[1]:
                    continue # skip start position
                if a[0] < min_x or a[0] > max_x:
                    print("invalid x", a)
                    continue # skip
                if a[1] < min_y or a[1] > max_y:
                    print("invalid y", a)
                    continue # skip
                risk = mat.get_value(matrix, a[0], a[1])
                if risk[1] != 0: # it was already  updated
                    if current_risk + risk[0] > risk[1]:
                        continue
                mat.set_value(matrix, a[0], a[1], (risk[0], current_risk + risk[0]))
                if a not in new_positions:
                    new_positions.append(a)
        positions = new_positions
    return mat.get_value(matrix, max_x, max_y, lambda a: a[1])


def calculate_part2():
    matrix = mat.read_input_to_matrix("input//day15//example.txt", create_grid_cell)
    mega_matrix = mat.create_empty(5*len(matrix[0].keys()), 5*len(matrix.keys()), (0, 0))
    fill_mega_matrix(mega_matrix, matrix)
    
    for a in range(5):   
        min_x = 0
        min_y = 0 + a*len(matrix.keys())
        if min_y > 0:
            min_y -= 1
        max_x = max(mega_matrix[0].keys())
        max_y = max(matrix.keys()) + a*len(matrix.keys())
        start_position = (min_x, min_y)
        print(start_position, min_x, min_y, max_x, max_y)
        result = traverse_matrix_v3(mega_matrix, start_position, min_x, min_y, max_x, max_y)
    
    # fill_mega_matrix(mega_matrix, matrix)
    # result = traverse_matrix_v2(mega_matrix, (0, 0), 0)
    # result = traverse_matrix_v3(mega_matrix, (0, 0), 0, 0, 49, 9)
    mat.print_matrix(mega_matrix, lambda a: str(a[1]))

    # print(result)

# execute
# calculate_part1()
calculate_part2()