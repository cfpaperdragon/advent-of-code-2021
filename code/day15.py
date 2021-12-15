# day15
import common
import matrix as mat

def traverse_matrix(matrix, start_position, steps):
    count_steps = 0
    max_x = max(matrix[0].keys())
    max_y = max(matrix.keys())
    paths = []
    # a path will be (risk, [position1, position2, position3])
    path = (0, [start_position])
    paths.append(path)
    finished_paths = []
    while len(paths) > 0: # count_steps < steps:
        count_steps += 1
        print("steps", count_steps)
        new_paths = []
        for p in paths:
            last_position = p[1][-1]
            adjacents = mat.get_adjacents(last_position[0], last_position[1], max_x, max_y) # no diagonals
            adjacents_not_in_path = [a for a in adjacents if a not in p[1]]
            if len(adjacents_not_in_path) == 0:
                continue
            min_risk = min([mat.get_value(matrix, a[0], a[1]) for a in adjacents_not_in_path])
            adjacents = adjacents_not_in_path # [a for a in adjacents if mat.get_value(matrix, a[0], a[1]) == min_risk]
            # print(adjacents)
            for i in range(len(adjacents)):
                adjacent = adjacents[i]
                if adjacent in p[1]: # point already in path, we don't want to walk back
                    continue
                risk = mat.get_value(matrix, adjacent[0], adjacent[1])
                path_copy = p[1].copy()
                path_copy.append(adjacent)
                new_path = (p[0] + risk, path_copy)
                if adjacent[0] == max_x and adjacent[1] == max_y:
                    finished_paths.append(new_path)
                else:
                    new_paths.append(new_path)
        paths = new_paths
        if len(paths) == 0:
            break
        current_min_risk = min([x[0] for x in paths])
        filtered_paths = [fp for fp in paths if fp[0] < current_min_risk * 2 and len(fp[1]) < max_x + max_y + 2]
        paths = filtered_paths
        # print(current_min_risk)
        # print(paths)
        # print(filtered_paths)
    return finished_paths



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
    



def calculate_part2():
    common.echo("part 2")
    #do other stuff

# execute
calculate_part1()
# calculate_part2()