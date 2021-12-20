# day19
import common
# import numpy as np

# "--- scanner 4 ---"" -> 4
def parse_scanner_name(scanner_string):
    scanner_name = scanner_string.replace("-", "").strip()
    scanner_name = scanner_name.replace("scanner", "").strip()
    return int(scanner_name)

# each scanner data has a list of positions
def process_scanner_data(input_list):
    scanner_data = {}
    scanner = parse_scanner_name(input_list[0])
    scanner_data[scanner] = {}
    for i in range(1, len(input_list)):
        value = input_list[i]
        if len(value) == 0:
            continue
        if value.startswith("---"):
            scanner = parse_scanner_name(input_list[i])
            scanner_data[scanner] = {}
            continue
        parts = value.split(",")
        point_identifier = common.get_unique_identifier()
        position = (int(parts[0]), int(parts[1]), int(parts[2]))
        scanner_data[scanner][point_identifier] = position
    return scanner_data


def print_scanner_data(scanner_data):
    for scanner in scanner_data.keys():
        print(scanner)
        for point in scanner_data[scanner].keys():
            print(point, scanner_data[scanner][point])


def calculate_vector(p1_identifier, p2_identifier, p1, p2):
    vector_identifier = (p1_identifier, p2_identifier)
    vector = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    return vector_identifier, vector


def calculate_vectors(scanner, scanner_data):
    point_list = list(scanner_data[scanner].keys())
    vectors = {}
    for i in range(len(point_list)):
        for j in range(1, len(point_list)):
            vector_identifier, vector = calculate_vector(
                point_list[i],
                point_list[j],
                scanner_data[scanner][point_list[i]],
                scanner_data[scanner][point_list[j]])    
            vectors[vector_identifier] = vector
    return vectors


def is_match_vector(vector1, vector2):
    print(vector1, vector2)
    return False


def match_vectors(scanner_data_base, vectors_scanner_base, vectors_other_scanner):

    for vcb in vectors_scanner_base.keys():
        vector1 = vectors_scanner_base[vcb]
        for vos in vectors_other_scanner.keys():
            vector2 = vectors_other_scanner[vos]
            if is_match_vector(vector1, vector2):
                print("it is a match")


def calculate_part1():
    inputs = common.read_input_to_function_list("input//day19//example.txt", str)
    # print(inputs)
    scanner_data = process_scanner_data(inputs)
    # print_scanner_data(scanner_data)
    # each scanner is its own referential, points are measured in reference to the scanner
    # to compare data from different scanners, my idea was to calculate vectors (p1 -> p2)
    # then check if any vector from scanner 0 matches any vector from scanner 1 and etc    
    # grab scanner 0 data
    scanner_0_vectors = calculate_vectors(0, scanner_data)
    print(len(scanner_0_vectors.keys()))
    scanner_1_vectors = calculate_vectors(1, scanner_data)
    # match_vectors(scanner_data, scanner_0_vectors, scanner_1_vectors)
    # this grows very fast, there must be a better way

def calculate_part2():
    common.echo("part 2")
    #do other stuff

# execute
calculate_part1()
# calculate_part2()