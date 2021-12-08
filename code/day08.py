# day08
import common

# acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
# ((sample1, sample2, ...), (digit1, digit2, digit3, digit4)
def parse_input(input_string):
    parts = input_string.split("|")
    samples = parts[0].strip().split()
    digits = parts[1].strip().split()
    sample_list = []
    for s in samples:
        sample_list.append(s.strip())
    digit_list = []
    for d in digits:
        digit_list.append(d.strip())
    return (sample_list, digit_list)

# 1 - 2 segments
# 4 - 4 segments
# 7 - 3 segments
# 8 - 7 segments
def find_unique_digits(input_list):
    count = 0
    for i in input_list:
        digit_part = i[1]
        for digit in digit_part:
            if len(digit) in [2, 3, 4, 7]:
                count += 1
    return count


def calculate_part1():
    inputs = common.read_input_to_function_list("input//day08//input.txt", parse_input)
    # print(inputs)
    unique_digits = find_unique_digits(inputs)
    print(unique_digits)
    
# can't assume the order of stuff

# ADG are the common segments in numbers 2, 3 and 5
def calculate_ADG_sequence(sequence_list):
    ADG_sequence = ""
    for c in sequence_list[0]:
        if c in sequence_list[1] and c in sequence_list[2]:
            ADG_sequence += c
    return ADG_sequence

# ABFG are the common segments in numbers 0, 6, and 9
def calculate_ABFG_sequence(sequence_list):
    ABFG_sequence = ""
    for c in sequence_list[0]:
        if c in sequence_list[1] and c in sequence_list[2]:
            ABFG_sequence += c
    return ABFG_sequence

# these are all the segments
#   AAAA  
#  B    C 
#  B    C 
#   DDDD  
#  E    F 
#  E    F 
#   GGGG  

def calculate_segments(input_sample):
    dict_by_size = {}
    for s in input_sample:
        l = len(s)
        if l in dict_by_size:
            dict_by_size[l].append(s)
        else:
            dict_by_size[l] = [s]
    
    # print(dict_by_size)
    segments = {}

    # calculate A
    # A = is in 7 and not in 1
    for c in dict_by_size[3][0]:
        if c not in dict_by_size[2][0]:
            segments["A"] = c

    # calculate B
    # B = is in 4, is not in 1, is not ADG
    ADG_sequence = calculate_ADG_sequence(dict_by_size[5])
    for c in dict_by_size[4][0]:
        if c not in dict_by_size[2][0] and c not in ADG_sequence:
            segments["B"] = c

    # calculate D
    # D = is in 4, and is on ADG
    for c in dict_by_size[4][0]:
        if c in ADG_sequence:
            segments["D"] = c
    
    # calculate G
    # G = is in ADG and is not A nor D
    for c in ADG_sequence:
        if c != segments["A"] and c != segments["D"]:
            segments["G"] = c

    # calculate F
    # F = is in 1 and is in ABFG sequence
    ABFG_sequence = calculate_ABFG_sequence(dict_by_size[6])
    for c in dict_by_size[2][0]:
        if c in ABFG_sequence:
            segments["F"] = c

    # calculate C
    # C = is in 1 and is different than F
    for c in dict_by_size[2][0]:
        if c != segments["F"]:
            segments["C"] = c

    # calculate E
    # E is the one that remains
    for c in dict_by_size[7][0]:
        if c not in segments.values():
            segments["E"] = c

    return segments
    

def create_decoder(segments):
    segment_decoder = {v: k for k, v in segments.items()}
    return segment_decoder


def get_number_decoder():
    return {
        "ABCEFG": "0",
        "CF": "1",
        "ACDEG": "2",
        "ACDFG": "3", 
        "BCDF": "4",
        "ABDFG": "5",
        "ABDEFG": "6",
        "ACF": "7",
        "ABCDEFG": "8",
        "ABCDFG": "9"
    }

def decode_digit(digit_string, segment_decoder, number_decoder):
    intermediate_state = ""
    for d in digit_string:
        intermediate_state += segment_decoder[d]
    intermediate_state = ''.join(sorted(intermediate_state))
    decoded_digit = number_decoder[intermediate_state]
    return decoded_digit

def calculate_number(digit_list, segment_decoder, number_decoder):
    number_str = ""
    for digit in digit_list:
        decoded_digit_str = decode_digit(digit, segment_decoder, number_decoder)
        number_str += decoded_digit_str
    return int(number_str)    

def calculate_part2():
    inputs = common.read_input_to_function_list("input//day08//input.txt", parse_input)
    # print(inputs)
    number_decoder = get_number_decoder()
    total = 0
    for i in inputs:
        # print(i)
        segments = calculate_segments(i[0])
        segment_decoder = create_decoder(segments)
        number = calculate_number(i[1], segment_decoder, number_decoder)
        total += number
    print(total)


# execute
# calculate_part1()
calculate_part2()