# day11
import common
import matrix as mat

def apply_function_to_matrix(matrix, function):
    flash_points = []
    for y in matrix.keys():
        for x in matrix[y].keys():
            mat.set_value(matrix, x, y, function(mat.get_value(matrix, x, y)))
            if mat.get_value(matrix, x, y) > 9:
                flash_points.append((x, y))
    return flash_points


def flash(octopus, x, y):
    flash_point_value = mat.get_value(octopus, x, y)
    if flash_point_value == 0:
        return []
    mat.set_value(octopus, x, y, 0)
    adjacents = mat.get_adjacents(x, y, max(octopus[y].keys()), max(octopus.keys()), True)
    new_flash_points = []
    # print(adjacents)
    for point in adjacents:
        value = mat.get_value(octopus, point[0], point[1])
        if value != 0: # already flashed
            mat.set_value(octopus, point[0], point[1], value + 1)
            if value + 1 > 9:
                new_flash_points.append((point[0], point[1]))
    return new_flash_points
                


def simulate_loop(octopus, number_step):
    step = 0
    count_flashes = 0
    while step != number_steps:
        flash_points = apply_function_to_matrix(octopus, lambda a: a+1)
        # print("step", step, "flash_points:", flash_points)
        while len(flash_points) > 0:
            new_flash_points = []
            for point in flash_points:
                # print("flash point", point)
                flash_points_aux = flash(octopus, point[0], point[1])
                # print("flash_point_aux", flash_points_aux)
                # do not add repeated
                for fpa in flash_points_aux:
                    if fpa not in new_flash_points:
                        new_flash_points.append(fpa)
                # mat.print_matrix(octopus)
                # print("new_flash_points:", new_flash_points)
            flash_points = new_flash_points
        step += 1
        count_flashes += mat.do_operation(octopus, lambda a, b: a+1, lambda a: a == 0, 0)
    return count_flashes


def simulate_loop_forever(octopus, number_safety_steps):
    step = 0
    stop_condition = len(octopus.keys()) * len(octopus[0].keys())
    # while step != number_safety_steps:
    while True:
        flash_points = apply_function_to_matrix(octopus, lambda a: a+1)
        # print("step", step, "flash_points:", flash_points)
        while len(flash_points) > 0:
            new_flash_points = []
            for point in flash_points:
                # print("flash point", point)
                flash_points_aux = flash(octopus, point[0], point[1])
                # print("flash_point_aux", flash_points_aux)
                # do not add repeated
                for fpa in flash_points_aux:
                    if fpa not in new_flash_points:
                        new_flash_points.append(fpa)
                # mat.print_matrix(octopus)
                # print("new_flash_points:", new_flash_points)
            flash_points = new_flash_points
        step += 1
        count_flashes = mat.do_operation(octopus, lambda a, b: a+1, lambda a: a == 0, 0)
        if count_flashes == stop_condition:
            break
    return step

def calculate_part1():
    inputs = mat.read_input_to_matrix("input//day11//input.txt", int)
    # mat.print_matrix(inputs)
    flashes = simulate_loop(inputs, 100)
    mat.print_matrix(inputs)
    print(flashes)
    #do other stuff

def calculate_part2():
    inputs = mat.read_input_to_matrix("input//day11//input.txt", int)
    # mat.print_matrix(inputs)
    step = simulate_loop_forever(inputs, 200)
    mat.print_matrix(inputs)
    print(step)
    #do other stuff

# execute
# calculate_part1()
calculate_part2()