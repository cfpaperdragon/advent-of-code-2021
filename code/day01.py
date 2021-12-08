# day01

import common

def read_input_to_integer_list(filename):
    result = []
    with open(filename) as file:
        line = file.readline()
        while line:
            value = int(line.strip())
            line = file.readline()
            result.append(value)
    return result

def count_increases(integer_list):
    count = 0
    for i in range(1, len(integer_list)):
        if integer_list[i] > integer_list[i-1]:
            count += 1
    return count


def count_increases_groups(integer_list):
    count = 0
    previous = 1000000 # very large number, the first is never an increase
    for i in range(2, len(integer_list)):
        sum_measurement = integer_list[i-2] + integer_list[i-1] + integer_list[i]
        if sum_measurement > previous:
            count += 1
        previous = sum_measurement
    return count


def calculate_part1():
    input_list = read_input_to_integer_list("input\\day01\\input.txt")
    number_increases = count_increases(input_list)
    common.echo(number_increases)


def calculate_part2():
    input_list = read_input_to_integer_list("input\\day01\\input.txt")
    number_increases = count_increases_groups(input_list)
    common.echo(number_increases)


# execute
# calculate_part1()
calculate_part2()