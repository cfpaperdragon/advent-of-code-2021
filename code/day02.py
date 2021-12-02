# day02

import common

def process_input(text):
    two_parts = text.split()
    first_part = two_parts[0]
    second_part = int(two_parts[1])
    return (first_part, second_part)


def calculate_position(instruction_list):
    horizontal_position = 0
    depth = 0
    for i in range(0, len(instruction_list)):
        command = instruction_list[i][0]
        value = instruction_list[i][1]
        if command == 'forward':
            horizontal_position += value
        elif command == 'down':
            depth += value
        else: # up
            depth -= value
    return (horizontal_position, depth)


def calculate_position_with_aim(instruction_list):
    horizontal_position = 0
    depth = 0
    aim = 0
    for i in range(0, len(instruction_list)):
        command = instruction_list[i][0]
        value = instruction_list[i][1]
        if command == 'forward':
            horizontal_position += value
            depth += aim * value
        elif command == 'down':
            aim += value
        else: # up
            aim -= value
    return (horizontal_position, depth)

def calculate_part1():
    instructions = common.read_input_to_function_list("input\\day02\\input.txt", process_input)
    result = calculate_position(instructions)
    print(result)
    print(result[0]*result[1])

def calculate_part2():
    instructions = common.read_input_to_function_list("input\\day02\\input.txt", process_input)
    result = calculate_position_with_aim(instructions)
    print(result)
    print(result[0]*result[1])


# execute
# calculate_part1()
calculate_part2()