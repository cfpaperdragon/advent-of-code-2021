# common.py
# common stuff that can be used for several days

def echo(some_text):
    print(some_text)


def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def read_input_to_function_list(filename, function):
    result = []
    with open(filename) as file:
        line = file.readline()
        while line:
            value = function(line.strip())
            line = file.readline()
            result.append(value)
    return result

def read_input_to_string(filename):
    result = ""
    with open(filename) as file:
        line = file.readline()
        while line:
            value = line.strip()
            line = file.readline()
            result += value
    return result