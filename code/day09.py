# day09

import common
import matrix as mat

def read_input_to_matrix(filename):
    result = {}
    y = 0
    with open(filename) as file:
        line = file.readline()
        while line:
            result[y] = {}
            number_str = line.strip()
            for x in range(len(number_str)):
                result[y][x] = (int(number_str[x]), 0)
            line = file.readline()
            y += 1
    return result


def calculate_points_to_check(grid, x, y):
    check_points = []
    # first row
    if y == 0:
        if x == 0:
            check_points.append((x+1, y))
            check_points.append((x, y+1))
        elif x == list(grid[0].keys())[-1]:
            check_points.append((x-1, y))
            check_points.append((x, y+1))
        else:
            check_points.append((x+1, y))
            check_points.append((x, y+1))
            check_points.append((x-1, y))
    # last row
    elif y == list(grid.keys())[-1]:
        if x == 0:
            check_points.append((x, y-1))
            check_points.append((x+1, y))
        elif x == list(grid[0].keys())[-1]:
            check_points.append((x-1, y))
            check_points.append((x, y-1))
        else:
            check_points.append((x, y-1))
            check_points.append((x+1, y))
            check_points.append((x-1, y))
    # everything else
    else:
        if x == 0:
            check_points.append((x, y-1))
            check_points.append((x+1, y))
            check_points.append((x, y+1))
        elif x == list(grid[0].keys())[-1]:
            check_points.append((x-1, y))
            check_points.append((x, y+1))
            check_points.append((x, y-1))
        else:
            check_points.append((x+1, y))
            check_points.append((x, y+1))
            check_points.append((x, y-1))
            check_points.append((x-1, y))
    return check_points


def is_low_point(grid, x, y):
    value = mat.get_value(grid, x, y, lambda a: a[0])

    check_points = calculate_points_to_check(grid, x, y)

    # print(x, y)
    # print(check_points)
    for point in check_points:
        point_value = mat.get_value(grid, point[0], point[1], lambda a: a[0])
        if not value < point_value:
            return False
    return True


def find_low_points(grid):
    low_points_values = []
    low_points = []
    for y in grid.keys():
        for x in grid[y].keys():
            if is_low_point(grid, x, y):
                low_points_values.append(mat.get_value(grid, x, y, lambda a: a[0]))
                low_points.append((x, y))
    return low_points_values, low_points


def calculate_risk_level(low_points):
    total = 0
    for p in low_points:
        total += p + 1
    return total


def calculate_part1():
    grid = read_input_to_matrix("input//day09//input.txt")
    # mat.print_matrix(grid)
    low_points_values, low_points = find_low_points(grid)
    # print(low_points)
    result = calculate_risk_level(low_points_values)
    print(result)


# start in a low point, then expand; stop when reach a nine
def mark_basin(grid, x, y, count):
    # print(x, y, count)
    value = mat.get_value(grid, x, y)
    if value[0] == 9:
        return count # stop condition
    if value[1] == 0: # mark if it wasn't already marked
        mat.set_value(grid, x, y, (value[0], 1))
        count += 1
    else:
        return count # if already marked, don't need to check again
    points_to_check_next = calculate_points_to_check(grid, x, y)
    for point in points_to_check_next:
        count = mark_basin(grid, point[0], point[1], count)
    return count

def calculate_part2():
    grid = read_input_to_matrix("input//day09//input.txt")
    # mat.print_matrix(grid)
    low_points_values, low_points = find_low_points(grid)
    # print(low_points)
    # low_point = low_points[0]
    # partial = mark_basin(grid, low_point[0], low_point[1], 0)
    # mat.print_matrix(grid)
    # print(partial)
    basin_values = []
    for low_point in low_points:
        # print(low_point)
        basin_value = mark_basin(grid, low_point[0], low_point[1], 0)
        # mat.print_matrix(grid)
        basin_values.append(basin_value)
    basin_values.sort(reverse = True)
    result = basin_values[0] * basin_values[1] * basin_values[2]
    print(result)
    

# execute
# calculate_part1()
calculate_part2()