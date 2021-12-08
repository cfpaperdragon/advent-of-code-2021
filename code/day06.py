# day01

def read_input_to_string(filename):
    result = ""
    with open(filename) as file:
        line = file.readline()
        while line:
            value = line.strip()
            line = file.readline()
            result += value
    return result


def parse_input_string(input_string):
    inputs = input_string.split(",")
    result = []
    for i in inputs:
        result.append(int(i))
    return result

# what about a dictionary, I don't need the order...
# 1: number of fish in one state
# 2: number of fish in two state
# 3: number of fish in three state
...
def make_lanternfish_storage(lanternfish_list):
    lanternfish_dict = {}
    # initialize
    for i in range(9):
        lanternfish_dict[i] = 0

    for lf in lanternfish_list:
        lanternfish_dict[lf] = lanternfish_dict[lf] + 1

    return lanternfish_dict

# 0, becomes 6
# 1, becomes 0 and 8
# 2, becomes 1
# 3, becomes 2
def inc_day(lanternfish_dict):
    new_dict = {}
    for k in range(1, 9):
        new_dict[k-1] = lanternfish_dict[k]
    new_dict[6] += lanternfish_dict[0]
    new_dict[8] = lanternfish_dict[0]
    # print(new_dict)
    return new_dict

def print_lanternfish(lanternfish_dict):
    for i in range(9):
        print(i, ":", lanternfish_dict[i])


def count_lanternfish(lanternfish_dict):
    count = 0
    for i in range(9):
        count += lanternfish_dict[i]
    return count


def calculate_part1(days = 80):
    input_string = read_input_to_string("input//day06//input.txt")
    lanternfish_list = parse_input_string(input_string)
    lanternfish_dict = make_lanternfish_storage(lanternfish_list)
    
    for i in range(days):
        lanternfish_dict = inc_day(lanternfish_dict)
    print_lanternfish(lanternfish_dict)
    total = count_lanternfish(lanternfish_dict)
    print(total)

def calculate_part2():
    calculate_part1(256)



# execute
# calculate_part1()
calculate_part2()