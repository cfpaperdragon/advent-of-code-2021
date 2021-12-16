# day15
import common
import matrix as mat


def create_grid_cell(value):
    return (int(value), 0, 0)


def get_min_risk_position(positions):
    min_risk = positions[0][1]
    min_risk_index = 0
    if len(positions) == 1:
        return positions.pop(0)
    for i in range(1, len(positions)):
        if positions[i][1] < min_risk:
            min_risk = positions[i][1]
            min_risk_index = i
    return positions.pop(min_risk_index)


def traverse_matrix_v2(matrix, start_position, steps):
    count_steps = 0
    max_x = max(matrix[0].keys())
    max_y = max(matrix.keys())
    positions = [(start_position, 0)]
    while len(positions) > 0:
        count_steps += 1
        # print(positions)
        position = get_min_risk_position(positions)
        p = position[0]
        current_risk = mat.get_value(matrix, p[0], p[1])
        adjacents = mat.get_adjacents(p[0], p[1], max_x, max_y) # no diagonals
        for a in adjacents:
            if a[0] == 0 and a[1] == 0:
                continue # skip start position
            risk = mat.get_value(matrix, a[0], a[1])
            if risk[1] != 0: # it was already  updated
                if current_risk[1] + risk[0] > risk[1]:
                    continue
            mat.set_value(matrix, a[0], a[1], (risk[0], current_risk[1] + risk[0], risk[2]))
            if risk[2] == 0:
                if (a, current_risk[1] + risk[0]) not in positions:
                    positions.append((a, current_risk[1] + risk[0]))
        mat.set_value(matrix, p[0], p[1], (current_risk[0], current_risk[1], current_risk[2]+1))
    return mat.get_value(matrix, max_x, max_y, lambda a: a[1])


def calculate_part1():
    matrix = mat.read_input_to_matrix("input//day15//input.txt", create_grid_cell)
    # mat.print_matrix(matrix)
    result = traverse_matrix_v2(matrix, (0,0), 20)
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
                    mat.set_value(mega_matrix, x + b*length_matrix_x, y + a*length_matrix_y, (calculate_new_value(value[0], a+b), 0, 0))


def calculate_part2():
    matrix = mat.read_input_to_matrix("input//day15//input.txt", create_grid_cell)
    mega_matrix = mat.create_empty(5*len(matrix[0].keys()), 5*len(matrix.keys()), (0, 0))
    fill_mega_matrix(mega_matrix, matrix)
    result = traverse_matrix_v2(mega_matrix, (0,0), 20)
    # mat.print_matrix(matrix)
    print(result)
    # mat.print_matrix(mega_matrix, lambda a: str(a[1]))

    # print(result)

# execute
# calculate_part1()
calculate_part2()

# I might not remember what was written there, but it was essential to keep track of visited nodes. That's what the 3 value on the cell is for.