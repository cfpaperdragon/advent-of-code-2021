# day20
import common
import matrix as mat
# we are going to need the "infinite matrix"

def parse_initial_matrix(input_list):
    # the matrix starts at line i = 2
    matrix_len = len(input_list[2])
    matrix = mat.create_empty(matrix_len, matrix_len, (".", ".")) # value now, value next 
    for i in range(2, len(input_list)):
        string = input_list[i].strip()
        # print(string, len(string))
        for j in range(len(string)):
            mat.set_value(matrix, j, i-2, (string[j], "."))
    return matrix, 0, 0, max(matrix[0].keys()), max(matrix.keys())


def print_matrix(matrix, min_x, max_x, min_y, max_y, function = str):
    for y in range(min_y, max_y+1):
        row = ""
        for x in range(min_x, max_x + 1):
           row += function(matrix[y][x]) + " "
        print(row)


def grow_matrix(matrix, min_x, min_y, max_x, max_y, value):
    # create a new row at min_y - 1
    matrix[min_y-1] = {}
    # create a new row at max_y + 1
    matrix[max_y+1] = {}
    for x in range(min_x, max_x + 1):
        mat.set_value(matrix, x, min_y-1, value)
        mat.set_value(matrix, x, max_y+1, value)
    min_y = min_y - 1 
    max_y = max_y + 1
    # print("after growing min_y and max_y")   
    # print_matrix(matrix, min_x, max_x, min_y, max_y, lambda a: a[0])

    # create a new column at min_x - 1
    # create a new column at max_x + 1
    for y in range(min_y, max_y+1):
        mat.set_value(matrix, min_x-1, y, value)
        mat.set_value(matrix, max_x+1, y, value)
    min_x = min_x - 1
    max_x = max_x + 1
    # print("after growing min_x and max_x")
    # print_matrix(matrix, min_x, max_x, min_y, max_y, lambda a: a[0])

    return min_x, min_y, max_x, max_y

def apply_enhance(matrix, min_x, min_y, max_x, max_y, source, destiny, enhance_str, out_of_matrix_char):
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1): 
            # print(x,y)
            enhance_index_str = ""
            if y == min_y or x == min_x:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x-1, y-1, lambda a: a[source])
            if y == min_y:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x, y-1, lambda a: a[source])
            if x == max_x or y == min_y:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x+1, y-1, lambda a: a[source])
            if x == min_x:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x-1, y, lambda a: a[source])

            enhance_index_str += mat.get_value(matrix, x, y, lambda a: a[source])
            if x == max_x:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x+1, y, lambda a: a[source])
            if x == min_x or y == max_y:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x-1, y+1, lambda a: a[source])
            if y == max_y:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x, y+1, lambda a: a[source])
            if x == max_x or y == max_y:
                enhance_index_str += out_of_matrix_char
            else:
                enhance_index_str += mat.get_value(matrix, x+1, y+1, lambda a: a[source])
            enhance_index_str = enhance_index_str.replace(".", "0")
            enhance_index_str = enhance_index_str.replace("#", "1")
            # print(enhance_index_str)
            enhance_index = int(enhance_index_str, 2)
            current_value = mat.get_value(matrix, x, y, lambda a: a[source])
            enhanced_pixel = enhance_str[enhance_index]
            if source > destiny: # source = 1, destiny = 0
                new_value = (enhanced_pixel, current_value)
            else:
                new_value = (current_value, enhanced_pixel)
            # print(enhance_index, enhanced_pixel, current_value, new_value)
            mat.set_value(matrix, x, y, new_value)
            

def count_lit_pixels(matrix, min_x, max_x, min_y, max_y, index):
    total = 0
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if mat.get_value(matrix, x, y, lambda a: a[index]) == "#":
                total += 1
    return total


def calculate_part1(max_loop=2):
    inputs = common.read_input_to_function_list("input//day20//input.txt", str)
    # print(inputs)
    enhance_string = inputs[0]
    matrix, min_x, min_y, max_x, max_y = parse_initial_matrix(inputs)
    # print(min_x, min_y, max_x, max_y)
    loop = 0
    while loop < max_loop:
    
        grow_matrix(matrix, min_x-loop, min_y-loop, max_x+loop, max_y+loop, (".", "."))
        # min_x_end, min_y_end, max_x_end, max_y_end = grow_matrix(matrix, min_x_1, min_y_1, max_x_1, max_y_1, (".", "."))
        # print(min_x, min_y, max_x, max_y)
        loop += 1
        apply_enhance(matrix, min_x-loop, min_y-loop, max_x+loop, max_y+loop, 0, 1, enhance_string, ".")
    
        # print_matrix(matrix, min_x-loop, max_x+loop, min_y-loop, max_y+loop, lambda a: a[0])
        # print_matrix(matrix, min_x-loop, max_x+loop, min_y-loop, max_y+loop, lambda a: a[1])
        # enhance 2nd time
    
        grow_matrix(matrix, min_x-loop, min_y-loop, max_x+loop, max_y+loop, ("#", "#"))
        loop += 1
        apply_enhance(matrix, min_x-loop, min_y-loop, max_x+loop, max_y+loop, 1, 0, enhance_string, "#")
        # print_matrix(matrix, min_x-loop, max_x+loop, min_y-loop, max_y+loop, lambda a: a[0])
        # print_matrix(matrix, min_x_end, max_x_end, min_y_end, max_y_end, lambda a: a[1])

    print(loop)
    total = mat.do_operation(matrix, lambda a,b: a+1, lambda a: a[0] == "#", 0)
    # total = count_lit_pixels(matrix, min_x-loop, max_x+loop, min_y-loop, max_y+loop, 0)
    print(total)

def calculate_part2():
    calculate_part1(50)
    #do other stuff

# execute
# calculate_part1()
calculate_part2()