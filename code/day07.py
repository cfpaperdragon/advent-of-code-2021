# day07
import common


def parse_position_list(inputs):
    input_list = inputs.split(",")
    position_list = []
    for i in input_list:
        position_list.append(int(i))
    return position_list


def calculate_fuel_between_positions(p1, p2):
    # part1 would be abs(p-position)
    # part2, it increases each step
    total = 0
    diff = abs(p1-p2)
    for i in range(1, diff+1):
        total += i
    # print(p1, p2, total)
    return total

def calculate_fuel(position_list, position, is_part_two = False, use_reference_value = False, reference_value = None):
    # reference_value will be used to cut bad branches
    fuel = 0
    for p in position_list:
        if is_part_two:
            # new code
            fuel += calculate_fuel_between_positions(p, position)
        else:
            fuel += abs(p-position)
        if use_reference_value:
            if fuel > reference_value:
                return (fuel, False)
    return (fuel, True)


def calculate_fuel_all_candidates(position_list, is_part_two = False):
    min_pos = position_list[0]
    max_pos = position_list[-1]
    fuel_calculations = {}
    reference_value = calculate_fuel(position_list, min_pos, True)[0] 
    fuel_calculations[min_pos] = reference_value
    for p in range(min_pos+1, max_pos+1):
        result = calculate_fuel(position_list, p, is_part_two, True, reference_value)
        if result[1]:
            fuel_calculations[p] = result[0]
            reference_value = min(reference_value, result[0])
    return fuel_calculations


def min_fuel(fuel_calculations):
    position_candidates = list(fuel_calculations.keys())
    min_value = fuel_calculations[position_candidates[0]]
    for p in range(1, len(position_candidates)):
        min_value = min(min_value, fuel_calculations[position_candidates[p]])
    return min_value


def calculate_part1():
    inputs = common.read_input_to_string("input//day07//input.txt")
    position_list = parse_position_list(inputs)
    position_list.sort()
    fuel_calculations = calculate_fuel_all_candidates(position_list)
    # print(fuel_calculations)
    min_value = min_fuel(fuel_calculations)
    print(min_value)


def calculate_part2():
    inputs = common.read_input_to_string("input//day07//input.txt")
    position_list = parse_position_list(inputs)
    position_list.sort()
    fuel_calculations = calculate_fuel_all_candidates(position_list, True)
    # print(fuel_calculations)
    min_value = min_fuel(fuel_calculations)
    print(min_value)

# execute
calculate_part1()
calculate_part2()