# day03

import common


# returns first the most common, then the least common
def count_bits(input_list, string_index):
    count_zeros = 0
    count_ones = 0
    for i in range(0, len(input_list)):
        if input_list[i][string_index] == "0":
            count_zeros += 1
        else:
            count_ones += 1
    if count_zeros > count_ones:
        return ("0", "1")
    elif count_zeros == count_ones:
        return ("1", "0")
    else:
        return ("1", "0")


def calculate_power_consumption(input_list):
    gamma_rate_str = ""
    epsilon_rate_str = ""

    for i in range(0, len(input_list[0])):
        result = count_bits(input_list, i)
        # print("result for i = {0} is most comon {1} and least common {2}".format(i, result[0], result[1]))
        gamma_rate_str += result[0]
        epsilon_rate_str += result[1]

    gamma_rate = int(gamma_rate_str, 2)
    epsilon_rate = int(epsilon_rate_str, 2)
    # common.echo("gamma:" + str(gamma_rate))
    # common.echo("epsilon:" + str(epsilon_rate))
    return gamma_rate * epsilon_rate

def calculate_part1():
    input_list = common.read_input_to_function_list("input//day03//input.txt", str)
    consumption = calculate_power_consumption(input_list)
    print(consumption)
    #do other stuff


def calculate_life_support_rating(input_list):
    oxigen_generator_list = input_list.copy()

    for i in range(0, len(input_list[0])):
        result = count_bits(oxigen_generator_list, i)
        # print("result for i = {0} is most comon {1} and least common {2}".format(i, result[0], result[1]))
        oxigen_generator_list = list(filter(lambda x: x[i] == result[0], oxigen_generator_list))
        # print(oxigen_generator_list)
        if len(oxigen_generator_list) == 1:
            break

    oxigen_generator = int(oxigen_generator_list[0], 2)

    co2_scrubber_list = input_list.copy()
    for i in range(0, len(input_list[0])):
        result = count_bits(co2_scrubber_list, i)
        # print("result for i = {0} is most comon {1} and least common {2}".format(i, result[0], result[1]))
        co2_scrubber_list = list(filter(lambda x: x[i] == result[1], co2_scrubber_list))
        # print(co2_scrubber_list)
        if len(co2_scrubber_list) == 1:
            break

    co2_scrubber = int(co2_scrubber_list[0], 2)
    common.echo("oxigen generator:" + str(oxigen_generator))
    common.echo("co2 scrubber:" + str(co2_scrubber))
    return oxigen_generator * co2_scrubber


def calculate_part2():
    input_list = common.read_input_to_function_list("input//day03//input.txt", str)
    life_support = calculate_life_support_rating(input_list)
    print(life_support)


# execute
# calculate_part1()
calculate_part2()