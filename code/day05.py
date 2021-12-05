# day05

import common
import matrix

# input: "0,9"
# output: (0, 9)
def parse_vector(vector_string):
    vector_parts = vector_string.strip().split(",")
    vector = (int(vector_parts[0]), int(vector_parts[1]))
    return vector

# input: "0,9 -> 5,9"
# output: ((0, 9), (5, 9))
def parse_vectors(vector_line_string):
    vector_list = vector_line_string.split("->")
    vector1 = parse_vector(vector_list[0])
    vector2 = parse_vector(vector_list[1])
    return (vector1, vector2)  

def find_max(vector_list):
    max_x = 0
    max_y = 0
    for vector in vector_list:     
        if vector[0][0] > max_x:
            max_x = vector[0][0]
        if vector[0][1] > max_y:
            max_y = vector[0][1]
        if vector[1][0] > max_x:
            max_x = vector[1][0]
        if vector[1][1] > max_y:
            max_y = vector[1][1]
    return max_x, max_y


def cover_one_vector_one_diagonal(pos_matrix, start_x, start_y, advance_x, advance_y, end_x, end_y):
    x = start_x
    y = start_y
    # print(x, y)
    # print(end_x, end_y)
    while x != end_x and y != end_y:
        # print(x, y)
        matrix.set_value(pos_matrix, x, y, matrix.get_value(pos_matrix, x, y) + 1)
        x = advance_x(x)
        y = advance_y(y)
    matrix.set_value(pos_matrix, x, y, matrix.get_value(pos_matrix, x, y) + 1)


def cover_one_vector_diagonals(pos_matrix, vector):
    start = vector[0]
    end = vector[1]

    # there's 4 directions possible
    if start[0] < end[0] and start[1] < end[1]:
        cover_one_vector_one_diagonal(pos_matrix, start[0], start[1], 
            lambda x: x+1, lambda y: y+1, end[0], end[1])

    elif start[0] > end[0] and start[1] > end[1]:
        cover_one_vector_one_diagonal(pos_matrix, end[0], end[1], 
            lambda x: x+1, lambda y: y+1, start[0], start[1])

    elif start[0] < end[0] and start[1] > end[1]:
        cover_one_vector_one_diagonal(pos_matrix, start[0], start[1], 
            lambda x: x+1, lambda y: y-1, end[0], end[1])
    
    elif start[0] > end[0] and start[1] < end[1]:
        cover_one_vector_one_diagonal(pos_matrix, start[0], start[1], 
            lambda x: x-1, lambda y: y+1, end[0], end[1])
    


def cover_one_vector(pos_matrix, vector, diagonals = False):
    start = vector[0]
    end = vector[1]
    
    # same x?
    if start[0] == end[0]:
        # range only works from smaller to bigger
        if start[1] < end[1]:
            for y in range(start[1], end[1]):
                matrix.set_value(pos_matrix, start[0], y, matrix.get_value(pos_matrix, start[0], y) + 1)
            # don't forget end position
            matrix.set_value(pos_matrix, start[0], end[1], matrix.get_value(pos_matrix, end[0], end[1]) + 1)
        elif start[1] > end[1]:
            for y in range(end[1], start[1]):
                matrix.set_value(pos_matrix, start[0], y, matrix.get_value(pos_matrix, start[0], y) + 1)
            # don't forget start position
            matrix.set_value(pos_matrix, start[0], start[1], matrix.get_value(pos_matrix, start[0], start[1]) + 1)
        # else: # not sure I need this condition
    # same y?
    elif start[1] == end[1]:
        if start[0] < end[0]:
            for x in range(start[0], end[0]):
                matrix.set_value(pos_matrix, x, start[1], matrix.get_value(pos_matrix, x, start[1]) + 1)
            # don't forget end position    
            matrix.set_value(pos_matrix, end[0], end[1], matrix.get_value(pos_matrix, end[0], end[1]) + 1)
        elif start[0] > end[0]:
            for x in range(end[0], start[0]):
                matrix.set_value(pos_matrix, x, start[1], matrix.get_value(pos_matrix, x, start[1]) + 1)
            # don't forget start position
            matrix.set_value(pos_matrix, start[0], start[1], matrix.get_value(pos_matrix, start[0], start[1]) + 1)
    # diagonals?
    else:
        if diagonals:
            cover_one_vector_diagonals(pos_matrix, vector)


def cover_points(pos_matrix, vector_list, diagonals = False):
    for vector in vector_list:
        # print(vector)
        cover_one_vector(pos_matrix, vector, diagonals)
        # matrix.print_matrix(pos_matrix)


def calculate_score(pos_matrix):
    count = 0
    for y in pos_matrix.keys():
        for x in pos_matrix[y].keys():
            if matrix.get_value(pos_matrix, x, y) >= 2:
                count += 1
    return count


def calculate_part1(diagonals = False):
    inputs = common.read_input_to_function_list("input//day05//input.txt", parse_vectors)
    # print(inputs)
    max_x, max_y = find_max(inputs)
    new_matrix = matrix.create_empty(max_x+1, max_y+1, 0)
    cover_points(new_matrix, inputs, diagonals)
    # matrix.print_matrix(new_matrix)
    score = calculate_score(new_matrix)
    print(score)


def calculate_part2():
    calculate_part1(True)
    # test_matrix = matrix.create_empty(5, 5, 0)
    # inputs = [((3, 0), (0, 3))]
    # cover_points(test_matrix, inputs, True)

# execute
# calculate_part1()
calculate_part2()