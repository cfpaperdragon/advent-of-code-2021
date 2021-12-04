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


# simple tests        

def test_matrix():
    new_matrix = create_empty(3, 3, (0, ""))
    set_value(new_matrix, 0, 0, (0, "X"))
    print_matrix(new_matrix)
    print(get_value(new_matrix, 0, 0))


# test_matrix()