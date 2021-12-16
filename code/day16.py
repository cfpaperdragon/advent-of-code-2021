# day16
import common

def decode_hexadeximal(input_string):
    the_bits = ""
    decoder = {
        "0" : "0000",
        "1" : "0001",
        "2" : "0010",
        "3" : "0011",
        "4" : "0100",
        "5" : "0101",
        "6" : "0110",
        "7" : "0111",
        "8" : "1000",
        "9" : "1001",
        "A" : "1010",
        "B" : "1011",
        "C" : "1100",
        "D" : "1101",
        "E" : "1110",
        "F" : "1111"
    }
    for c in input_string:
        if c in decoder:
            # print(c, decoder[c])
            the_bits += decoder[c]
    return the_bits

def parse_number_n_bits(bit_string, index, n_bits):
    number_bits = bit_string[index:index+n_bits]
    number = int(number_bits, 2)
    index += n_bits
    return index, number


def parse_version(bit_string, index):
    # first 3 bits are the packet version
    return parse_number_n_bits(bit_string, index, 3)


def parse_literal(bit_string, i):
    list_number_bit_parts = []
    number_bit_part = bit_string[i:i+5]
    list_number_bit_parts.append(number_bit_part)
    i += 5
    while number_bit_part[0] == "1": # keep reading
        number_bit_part = bit_string[i:i+5]
        list_number_bit_parts.append(number_bit_part)
        i += 5
    number_bits = ""
    # print(list_number_bit_parts)
    for nbp in list_number_bit_parts:
        number_bits += nbp[1:] # remove leading bit
    number = int(number_bits, 2)
    return i, number


def parse_packets(bit_string, i, packets, continue_condition, extra_parameter=None):
    if extra_parameter == None:
        packets_count = 0
    else:
        packets_count = extra_parameter
    while continue_condition(i) or packets_count > 0:
        # print(i, len(bit_string))
        if len(bit_string) - i <= 7: # 
            break
        i, version = parse_version(bit_string, i)
        # type is the same as version
        i, type_num = parse_version(bit_string, i)
        if type_num == 4: # it is a literal
            i, number = parse_literal(bit_string, i)
            packet = (version, type_num, number)
            # print(packet)
            packets.append(packet)
        else: 
            length_type_id = bit_string[i]
            i += 1
            if length_type_id == "0":
                # next 15 bits are total length in bits of the sub-packets
                i, total_length = parse_number_n_bits(bit_string, i, 15)
                # print(total_length, i)
                i, sub_packets = parse_packets(bit_string, i, [], lambda a: a < i + total_length)
                packet = (version, type_num, sub_packets)
                # print(packet)
                packets.append(packet)
            else: # 1
                # next 11 bits are the number of sub-packets
                i, number_packets = parse_number_n_bits(bit_string, i, 11)
                # print(number_packets)
                i, sub_packets = parse_packets(bit_string, i, [], lambda a: False, number_packets)
                packet = (version, type_num, sub_packets)
                # print(version, type_num, length_type_id, number_packets, packet)
                packets.append(packet)
        if extra_parameter != None:
            packets_count -= 1
        
    return i, packets


def calculate_sum_version(packets):
    version_sum = 0
    for packet in packets:
        if isinstance(packet[2], list):
            version_sum += packet[0] + calculate_sum_version(packet[2])
        else:
            version_sum += packet[0]
    return version_sum


def calculate_part1():
    inputs = common.read_input_to_string("input//day16//input.txt")
    bit_string = decode_hexadeximal(inputs)
    # print(bit_string)
    index, packets = parse_packets(bit_string, 0, [], lambda a: a < len(bit_string))
    # print(len(packets))
    version_sum = calculate_sum_version(packets)
    print(version_sum)

# 0 = sum - any number
# 1 = product - any number
# 2 = minimum - any number
# 3 = maximum - any number
# 5 = greater than - always 2
# 6 = less than - always 2
# 7 = equal to - always 2

def do_operation(packet):
    result = 0
    if not isinstance(packet[2], list):
        result = packet[2]
    else:
        operation = packet[1]
        if operation in [5, 6, 7]:
            value1 = do_operation(packet[2][0])
            value2 = do_operation(packet[2][1])
            if operation == 5: # greater than
                if value1 > value2:
                    result = 1
                else:
                    result = 0
            elif operation == 6: # less than
                if value1 < value2:
                    result = 1
                else:
                    result = 0
            elif operation == 7: # equal to
                if value1 == value2:
                    result = 1
                else:
                    result = 0
        elif operation in [0, 1, 2, 3]:
            values = []
            for p in packet[2]: 
                value = do_operation(p)
                values.append(value)
            if operation == 0: # sum
                result = sum(values)
            elif operation == 1: # product
                partial = 1
                for v in values:
                    partial *= v
                result = partial
            elif operation == 3: # max
                result = max(values)
            elif operation == 2: # min
                result = min(values)
    return result


def calculate_part2():
    inputs = common.read_input_to_string("input//day16//input.txt")
    # inputs = "C200B40A82" # 3
    # inputs = "04005AC33890" # 54
    # inputs = "880086C3E88112" # 7
    # inputs = "CE00C43D881120" # 9
    # inputs = "D8005AC2A8F0" # 1
    # inputs = "F600BC2D8F" # 0
    # inputs = "9C005AC2F8F0" # 0
    # inputs = "9C0141080250320F1802104A08" # 1
    bit_string = decode_hexadeximal(inputs)
    index, packets = parse_packets(bit_string, 0, [], lambda a: a < len(bit_string))
    # print(packets[0])
    result = do_operation(packets[0])
    print(result)

# execute
# calculate_part1()
calculate_part2()
