# day19
import common
# import numpy as np
import math
import matrix as mat

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
            if i == j: # don't do anything if it is the same point, need those repeated vectors
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
        if sv[2] == osv[2]: # vectors with same len, probably a match
            # print(sv[1], osv[1])
            # matched_vectors.append((sv, osv))
            # advance both
            other_index += 1
            index += 1
            # I now have repeated vectors in the list a -> b and b <- a
            # because they have the same lenght, and the list is sorted, they should be next to each other
            sv_dup = scanner_vector_list[index]
            osv_dup = other_scanner_vector_list[other_index]
            if sv_dup[2] == osv_dup[2]: # it should
                matched_vectors.append((sv, sv_dup, osv, osv_dup))
                other_index += 1
                index += 1
            else:
                print("something went wrong :/")
                print(sv_dup[1], osv_dup[1])
        elif sv[2] > osv[2]: # advance on osv
            other_index += 1
        else: # advance on sv
            index += 1
    return matched_vectors

# so I am assuming something here that I think is correct by accident
# and will probably need to improve for this to work
# in the example, there is a rotation on the y axis
# when vector base and vector other have the same direction, there's only the y rotation (changing the sign of x and z)
# when vector base and vector other have opposite directions, there's that extra rotation (changing one more coordinate)
# I previously matched the vectors by length so here, I need to understand if there's a rotation
# according to the problem, there are 24 different orientations
# having found the correct orientation/rotation between vectors, it is trivial to apply it to find the position of the scanner
# then can apply the changes to all beacons
def exact_match(v1, v2):
    if v1[0] == v2[0] and v1[1] != v2[1] and v1[2] != v2[2]:
        return True
    if v1[0] != v2[0] and v1[1] == v2[1] and v1[2] != v2[2]:
        return True
    if v1[0] != v2[0] and v1[1] != v2[1] and v1[2] == v2[2]:
        return True
    return False


def apply_matrix_to_vector(v1, rm):
    x = 0
    y = 1
    z = 2

    x_coordinate = v1[x]*mat.get_value(rm, 0, 0) + v1[y]*mat.get_value(rm, 0, 1) + v1[z]*mat.get_value(rm, 0, 2)
    y_coordinate = v1[x]*mat.get_value(rm, 1, 0) + v1[y]*mat.get_value(rm, 1, 1) + v1[z]*mat.get_value(rm, 1, 2)
    z_coordinate = v1[x]*mat.get_value(rm, 2, 0) + v1[y]*mat.get_value(rm, 2, 1) + v1[z]*mat.get_value(rm, 2, 2)

    return (x_coordinate, y_coordinate, z_coordinate)

# applying rotation matrix to v1, I should obtain v2
# rm is a 4x4 matrix, like so
# [1  0 0 0]
# [0 -1 0 0]
# [0  0 1 0]
# [0  0 0 1]
def is_match(v1, v2, rm):
    new_v2 = apply_matrix_to_vector(v1, rm)
    return v2 == new_v2


def matched_vectors_to_matched_points(matched_vectors, rotation_matrix_list):
    matched_points = {}
    rotation_matrix = None
    for i in range(len(matched_vectors)):
        vector_base = matched_vectors[i][0]
        other_vector = matched_vectors[i][2]
        other_vector_dup = matched_vectors[i][2]
        # print(vector_base)
        # print(other_vector)
        # in a vector I have: (identifier, vector actual, vector length)

        # in the final version we need to try and find the rotation matrix, for now we will cheat
        # rotation_matrix = mat.create_empty(3, 3, 0)
        # mat.set_value(rotation_matrix, 0, 0, -1)
        # mat.set_value(rotation_matrix, 1, 1, 1)
        # mat.set_value(rotation_matrix, 2, 2, -1)
        if rotation_matrix == None: # first match
            for rm in rotation_matrix_list:
                if is_match(vector_base[1], other_vector[1], rm):
                    # found the matrix
                    rotation_matrix = rm

        if is_match(vector_base[1], other_vector[1], rotation_matrix): # try to check if the first one matches
            if vector_base[0][0] not in matched_points:
                matched_points[vector_base[0][0]] = other_vector[0][0]
            if vector_base[0][1] not in matched_points:
                matched_points[vector_base[0][1]] = other_vector[0][1] 
        elif is_match(vector_base[1], other_vector_dup[1], rotation_matrix): # try to check if the second one matches
            if vector_base[0][0] not in matched_points:
                matched_points[vector_base[0][0]] = other_vector_dup[0][0]
            if vector_base[0][1] not in matched_points:
                matched_points[vector_base[0][1]] = other_vector_dup[0][1]       
        # if neither matches, ignore this one

    return matched_points, rotation_matrix


def scanner_vectors_to_list(scanner_vectors):
    scanner_vector_list = []
    for key in scanner_vectors:
        scanner_vector_list.append((key, scanner_vectors[key][0], scanner_vectors[key][1]))
    return scanner_vector_list


def print_matched_points(matched_points, scanner_data, base_scanner, other_scanner):
    for point in matched_points:
        print(scanner_data[base_scanner][point], "=", scanner_data[other_scanner][matched_points[point]])

def print_matched_vectors(matched_vectors, scanner_data, base_scanner, other_scanner):
    for vector_quadruple in matched_vectors:
        base_vector = vector_quadruple[0]
        base_vector_dup = vector_quadruple[1]
        other_vector = vector_quadruple[2]
        other_vector_dup = vector_quadruple[3]
        print("base:", base_vector)
        print("other:", other_vector)
        print("base_dup:", base_vector_dup)
        print("other_dup:", other_vector_dup)
        print("base:", scanner_data[base_scanner][base_vector[0][0]], scanner_data[base_scanner][base_vector[0][1]])
        print("other:", scanner_data[other_scanner][other_vector[0][0]], scanner_data[other_scanner][other_vector[0][1]])
        print("base_dup:", scanner_data[base_scanner][base_vector_dup[0][0]], scanner_data[base_scanner][base_vector_dup[0][1]])
        print("other_dup:", scanner_data[other_scanner][other_vector_dup[0][0]], scanner_data[other_scanner][other_vector_dup[0][1]])


def create_rotation_matrix(alpha, beta, gama):
    matrix = mat.create_empty(3, 3, 0) 
    cos_alpha = int(math.cos(math.radians(alpha)))
    cos_beta = int(math.cos(math.radians(beta)))
    cos_gama = int(math.cos(math.radians(gama)))
    sin_alpha = int(math.sin(math.radians(alpha)))
    sin_beta = int(math.sin(math.radians(beta)))
    sin_gama = int(math.sin(math.radians(gama)))
    mat.set_value(matrix, 0, 0, cos_beta*cos_gama)
    mat.set_value(matrix, 1, 0, cos_beta*sin_gama)
    mat.set_value(matrix, 2, 0, -sin_beta)
    mat.set_value(matrix, 0, 1, sin_alpha*sin_beta*cos_gama - cos_alpha*sin_gama)
    mat.set_value(matrix, 1, 1, sin_alpha*sin_beta*sin_gama + cos_alpha*cos_gama)
    mat.set_value(matrix, 2, 1, sin_alpha*cos_beta)
    mat.set_value(matrix, 0, 2, cos_alpha*sin_beta*cos_gama + sin_alpha*sin_gama) 
    mat.set_value(matrix, 1, 2, cos_alpha*sin_beta*sin_gama - sin_alpha*cos_gama)
    mat.set_value(matrix, 2, 2, cos_alpha*cos_beta)
    # print("angles", alpha, beta, gama)
    # mat.print_matrix(matrix)
    return matrix


def get_all_possible_rotation_matrixes():
    rotation_matrix_list = []
    # positive z up
    rotation_matrix_list.append(create_rotation_matrix(0, 0, 0))
    rotation_matrix_list.append(create_rotation_matrix(0, 0, 90))
    rotation_matrix_list.append(create_rotation_matrix(0, 0, 180))
    rotation_matrix_list.append(create_rotation_matrix(0, 0, 270))
    # positive z down
    rotation_matrix_list.append(create_rotation_matrix(180, 0, 0))
    rotation_matrix_list.append(create_rotation_matrix(180, 0, 90))
    rotation_matrix_list.append(create_rotation_matrix(180, 0, 180))
    rotation_matrix_list.append(create_rotation_matrix(180, 0, 270))
    # positive y up
    rotation_matrix_list.append(create_rotation_matrix(90, 0, 0))
    rotation_matrix_list.append(create_rotation_matrix(90, 90, 0))
    rotation_matrix_list.append(create_rotation_matrix(90, 180, 0))
    rotation_matrix_list.append(create_rotation_matrix(90, 270, 0))
    # positive y down
    rotation_matrix_list.append(create_rotation_matrix(-90, 0, 0))
    rotation_matrix_list.append(create_rotation_matrix(-90, 90, 0))
    rotation_matrix_list.append(create_rotation_matrix(-90, 180, 0))
    rotation_matrix_list.append(create_rotation_matrix(-90, 270, 0))
    # positive x up
    rotation_matrix_list.append(create_rotation_matrix(0, 90, 0))
    rotation_matrix_list.append(create_rotation_matrix(90, 90, 0))
    rotation_matrix_list.append(create_rotation_matrix(180, 90, 0))
    rotation_matrix_list.append(create_rotation_matrix(270, 90, 0))
    # positive x down
    rotation_matrix_list.append(create_rotation_matrix(0, -90, 0))
    rotation_matrix_list.append(create_rotation_matrix(90, -90, 0))
    rotation_matrix_list.append(create_rotation_matrix(180, -90, 0))
    rotation_matrix_list.append(create_rotation_matrix(270, -90, 0))
    return rotation_matrix_list


def transpose_matrix(m, x_len, y_len):
    new_matrix = mat.create_empty(3, 3, 0)
    for y in range(y_len):
        for x in range(y_len):
            mat.set_value(new_matrix, y, x, mat.get_value(m, x, y))
    return new_matrix


def change_beacons_to_base_referential(scanner_data, final_scanner_data, current_scanner, inverse_rotation_matrix, current_scanner_position):
    for beacon_key in scanner_data[current_scanner].keys():
        beacon = scanner_data[current_scanner][beacon_key]
        # PX_0 = S1 + PX_1'
        px_current = apply_matrix_to_vector(beacon, inverse_rotation_matrix)
        px_base = (current_scanner_position[0]+px_current[0], current_scanner_position[1]+px_current[1], current_scanner_position[2]+px_current[2])
        final_scanner_data[current_scanner][beacon_key] = px_base


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
    rotation_matrix_list = get_all_possible_rotation_matrixes()
    matched_points, rotation_matrix = matched_vectors_to_matched_points(matched_vectors, rotation_matrix_list)
    # print_matched_points(matched_points, scanner_data, 0, 1)
    # mat.print_matrix(rotation_matrix)
    # calculate scanner 1 coordinates in scanner 0 referential
    # S1 = -P1_1' + P1_0
    # P1' is obtained by multiplying the inverse rotation matrix (also known as the transpose matrix)
    p1_0 = scanner_data[0][list(matched_points.keys())[0]]
    p1_1 = scanner_data[1][matched_points[list(matched_points.keys())[0]]]
    inverse_rotation_matrix = transpose_matrix(rotation_matrix, 3, 3)
    p1_1_moved = apply_matrix_to_vector(p1_1, inverse_rotation_matrix)
    s1 = (-p1_1_moved[0]+p1_0[0], -p1_1_moved[1]+p1_0[1], -p1_1_moved[2]+ p1_0[2])
    # print(s1)
    final_scanner_data = {}
    final_scanner_data[0] = scanner_data[0]
    # next step is transposing all beacons from scanner1 to scanner0 referential
    # PX_0 = S1 + PX_1'
    final_scanner_data[1] = {}
    change_beacons_to_base_referential(scanner_data, final_scanner_data, 1, inverse_rotation_matrix, s1)
    # then repeat the steps for the other scanners
    print_scanner_data(final_scanner_data)




def calculate_part2():
    common.echo("part 2")
    #do other stuff


def test():
    count = 0

# execute
# test()
calculate_part1()
# calculate_part2()