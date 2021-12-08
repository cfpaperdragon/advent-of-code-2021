# matrix useful functions

# a matrix is composed of 2 levels of dictionaries
# when you do matrix[y][x] you access position x,y

def create_empty(x_len, y_len, initial_value):
    matrix = {}
    for y in range(y_len):
        matrix[y] = {}
        for x in range(x_len):
            matrix[y][x] = initial_value
    return matrix


def print_matrix(matrix, function = str):
    for y in matrix.keys():
        row = ""
        for x in matrix[y].keys():
           row += function(matrix[y][x]) + " "
        print(row)


def get_value(matrix, x, y, function = None):
    if function == None:
        return matrix[y][x]
    else:
        return function(matrix[y][x])


def set_value(matrix, x, y, value, function = None):
    if function == None: 
        matrix[y][x] = value
    else:
        matrix[y][x] = function(matrix[y][x], value)


def do_operation(matrix, operation_function, condition_function, start_value):
    result = start_value
    for y in matrix.keys():
        for x in matrix.keys():
            if condition_function(get_value(matrix, x, y)):
                result = operation_function(result, get_value(matrix, x, y))
    return result

# simple tests        

def test_matrix():
    new_matrix = create_empty(3, 3, 1)
    set_value(new_matrix, 0, 0, 2)
    set_value(new_matrix, 0, 1, 2)
    print_matrix(new_matrix)
    result = do_operation(new_matrix, lambda a,b: a+b, lambda a: a > 1, 0)
    print(result)


# test_matrix()