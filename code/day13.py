# day13 
import common
import matrix as mat

def parse_input(input_list):
    points = []
    instructions = []
    for i in input_list:
        if len(i) == 0:
            continue
        if i.startswith("fold"):
            i_parts = i[11:].split("=")
            instruction = (i_parts[0], int(i_parts[1]))
            instructions.append(instruction)
        else:
            coordinates = i.split(",")
            point = (int(coordinates[0]), int(coordinates[1]))
            points.append(point)
    return points, instructions


def create_matrix(points):
    max_x = 0
    max_y = 0
    for p in points:
        max_x = max(max_x, p[0])
        max_y = max(max_y, p[1])
    matrix = mat.create_empty(max_x+1, max_y+1, ".")
    # mat.print_matrix(matrix)
    for p in points:
        mat.set_value(matrix, p[0], p[1], "#")
    return matrix


def fold_on_y(matrix, y_value):
    new_matrix = mat.create_empty(len(matrix[0].keys()), y_value, ".")
    # copy values until line y
    for y in range(0, y_value):
        for x in matrix[y].keys():
            mat.set_value(new_matrix, x, y, mat.get_value(matrix, x, y))
    # copy values start on line y+1, backwars in y
    for y in reversed(range(0, y_value)):
        for x in matrix[y].keys():
            old_value = mat.get_value(matrix, x, max(matrix.keys())-y)
            if old_value == ".":
                continue
            mat.set_value(new_matrix, x, y, old_value)
    return new_matrix


def fold_on_x(matrix, x_value):
    new_matrix = mat.create_empty(x_value, len(matrix.keys()), ".")
    # copy values until column x
    for y in matrix.keys():
        for x in range(0, x_value):
            mat.set_value(new_matrix, x, y, mat.get_value(matrix, x, y))
    # copy values start on column x+1, backwars in x
    for y in matrix.keys():
        for x in reversed(range(0, x_value)):
            old_value = mat.get_value(matrix, max(matrix[y].keys())-x, y)
            if old_value == ".":
                continue
            mat.set_value(new_matrix, x, y, old_value)
    return new_matrix

def calculate_part1():
    inputs = common.read_input_to_function_list("input//day13//input.txt", str)
    points, instructions = parse_input(inputs)
    # print(points)
    # print(instructions)
    matrix = create_matrix(points)
    # mat.print_matrix(matrix)
    # new_matrix = fold_on_y(matrix, 7)
    # new_matrix = fold_on_x(new_matrix, 5)
    
    first_instruction = instructions[0]
    if first_instruction[0] == "x":
        new_matrix = fold_on_x(matrix, first_instruction[1])
    else:
        new_matrix = fold_on_y(matrix, first_instruction[1])
    # mat.print_matrix(new_matrix)
    number_dots = mat.do_operation(new_matrix, lambda a,b: a+1, lambda a: a == "#", 0)
    print(number_dots)


def calculate_part2():
    inputs = common.read_input_to_function_list("input//day13//input.txt", str)
    points, instructions = parse_input(inputs)
    matrix = create_matrix(points)
    
    for instruction in instructions:
        print(instruction)
        if instruction[0] == "x":
            matrix = fold_on_x(matrix, instruction[1])
        else:
            matrix = fold_on_y(matrix, instruction[1])
    mat.print_matrix(matrix)
    

# execute
# calculate_part1()
calculate_part2()