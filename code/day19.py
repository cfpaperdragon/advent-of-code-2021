# day19
import common
# import numpy as np
import math

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


def calculate_vector_length(vector):
    return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])

def calculate_vectors(scanner, scanner_data):
    point_list = list(scanner_data[scanner].keys())
    vectors = {}
    for i in range(len(point_list)):
        for j in range(len(point_list)):
            if i >= j: # don't do anything if it is the same point, avoid repeated vectors
                continue
            vector_identifier, vector = calculate_vector(
                point_list[i],
                point_list[j],
                scanner_data[scanner][point_list[i]],
                scanner_data[scanner][point_list[j]])    
            vector_length = calculate_vector_length(vector)
            vectors[vector_identifier] = (vector, vector_length)
    return vectors


def is_match_vector(vector1, vector2):
    print(vector1, vector2)
    return False


def match_vectors(scanner_vector_list, other_scanner_vector_list):
    matched_vectors = []
    # we are going to search in paralel through the lists
    index = 0
    other_index = 0
    while index < len(scanner_vector_list) and other_index < len(other_scanner_vector_list):
        sv = scanner_vector_list[index]
        osv = other_scanner_vector_list[other_index]
        if sv[2] == osv[2]: # vectors with same len, probably a match - try not to get screwed by precision
            # print(sv[1], osv[1])
            matched_vectors.append((sv, osv))
            # advance both
            other_index += 1
            index += 1
        elif sv[2] > osv[2]: # advance on osv
            other_index += 1
        else: # advance on sv
            index += 1
    return matched_vectors


def exact_match(v1, v2):
    if v1[0] == v2[0] and v1[1] != v2[1] and v1[2] != v2[2]:
        return True
    if v1[0] != v2[0] and v1[1] == v2[1] and v1[2] != v2[2]:
        return True
    if v1[0] != v2[0] and v1[1] != v2[1] and v1[2] == v2[2]:
        return True
    return False

def matched_vectors_to_matched_points(matched_vectors):
    matched_points = {}
    for i in range(len(matched_vectors)):
        vector_base = matched_vectors[i][0]
        other_vector = matched_vectors[i][1]
        # print(vector_base)
        # print(other_vector)
        # in a vector I have: (identifier, vector actual, vector length)
        # check the x in the vector actual to see if they are equal
        # if yes, then p1 from vector base matches p1 of other vector
        # if not, p1 is actual p2 of other vector
        
            # print("add to matched points")
        if exact_match(vector_base[1], other_vector[1]):
            if vector_base[0][0] not in matched_points:
                matched_points[vector_base[0][0]] = other_vector[0][0]
            if vector_base[0][1] not in matched_points:
                matched_points[vector_base[0][1]] = other_vector[0][1]
        else:
            if vector_base[0][0] not in matched_points:
                matched_points[vector_base[0][0]] = other_vector[0][1]
            if vector_base[0][1] not in matched_points:
                matched_points[vector_base[0][1]] = other_vector[0][0]
    return matched_points


def scanner_vectors_to_list(scanner_vectors):
    scanner_vector_list = []
    for key in scanner_vectors:
        scanner_vector_list.append((key, scanner_vectors[key][0], scanner_vectors[key][1]))
    return scanner_vector_list


def print_matched_points(matched_points, scanner_data, base_scanner, other_scanner):
    for point in matched_points:
        print(scanner_data[base_scanner][point], "=", scanner_data[other_scanner][matched_points[point]])

def print_matched_vectors(matched_vectors, scanner_data, base_scanner, other_scanner):
    for vector_pair in matched_vectors:
        base_vector = vector_pair[0]
        other_vector = vector_pair[1]
        print("base:", base_vector)
        print("other:", other_vector)
        print("base:", scanner_data[base_scanner][base_vector[0][0]], scanner_data[base_scanner][base_vector[0][1]])
        print("other:", scanner_data[other_scanner][other_vector[0][0]], scanner_data[other_scanner][other_vector[0][1]])


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
    # print(scanner_0_vectors)
    scanner_0_vectors_list = scanner_vectors_to_list(scanner_0_vectors)
    scanner_0_vectors_list.sort(key=lambda a: a[2])
    # print(scanner_0_vectors_list)
    # for i in range(len(scanner_0_vectors_list)):
    #     print(scanner_0_vectors_list[i])
    # print("")
    scanner_1_vectors = calculate_vectors(1, scanner_data)
    scanner_1_vectors_list = scanner_vectors_to_list(scanner_1_vectors)
    scanner_1_vectors_list.sort(key=lambda a: a[2])
    # for i in range(len(scanner_1_vectors_list)):
    #     print(scanner_1_vectors_list[i])
    # match_vectors(scanner_data, scanner_0_vectors, scanner_1_vectors)
    # this grows very fast, there must be a better way
    matched_vectors = match_vectors(scanner_0_vectors_list, scanner_1_vectors_list)
    # print_matched_vectors(matched_vectors, scanner_data, 0, 1)
    matched_points = matched_vectors_to_matched_points(matched_vectors)
    print_matched_points(matched_points, scanner_data, 0, 1)


def calculate_part2():
    common.echo("part 2")
    #do other stuff

# execute
calculate_part1()
# calculate_part2()