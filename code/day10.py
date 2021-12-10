# day10
import common

def parse_line(input_str):
    # print(input_str)
    chunk_stack = []
    chunk_closers = {}
    chunk_closers[")"] = ("(", 3)
    chunk_closers["]"] = ("[", 57)
    chunk_closers["}"] = ("{", 1197)
    chunk_closers[">"] = ("<", 25137)
    for c in input_str:
        # print(c, "-", chunk_stack)
        if c in "([{<":
            chunk_stack.insert(0, c)
        elif c in list(chunk_closers.keys()):
            if chunk_stack[0] == chunk_closers[c][0]:
                chunk_stack.pop(0)
            else:
                # invalid character
                # print("invalid", c, chunk_stack)
                return chunk_closers[c][1]
    return 0


def reparse_line(input_str):
    # print(input_str)
    chunk_stack = []
    chunk_closers = {}
    chunk_closers[")"] = ("(", 3)
    chunk_closers["]"] = ("[", 57)
    chunk_closers["}"] = ("{", 1197)
    chunk_closers[">"] = ("<", 25137)
    for c in input_str:
        # print(c, "-", chunk_stack)
        if c in "([{<":
            chunk_stack.insert(0, c)
        elif c in list(chunk_closers.keys()):
            if chunk_stack[0] == chunk_closers[c][0]:
                chunk_stack.pop(0)
    # print(chunk_stack)
    close_chars = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">"
    }
    chars_to_complete = []
    for c in chunk_stack:
        if c in list(close_chars.keys()):
            chars_to_complete.append(close_chars[c])
    return chars_to_complete


def parse_corrupted_chunks(input_list):
    total = 0
    for input_str in input_list:
        total += parse_line(input_str)
    return total


def discard_corrupted_chunks(input_list):
    incomplete_chunks = []
    for input_str in input_list:
            if parse_line(input_str) == 0:
                incomplete_chunks.append(input_str)
    return incomplete_chunks

# ): 1 point.
# ]: 2 points.
# }: 3 points.
# >: 4 points.
def calculate_score(remaining):
    score_values = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }
    total = 0
    for r in remaining:
        if r in list(score_values.keys()):
            total *= 5
            total += score_values[r]

    return total


def parse_incomplete_chunks(input_list):
    scores = []
    for input_str in input_list:
        remaining = reparse_line(input_str)
        # print(input_str, "".join(remaining))
        partial = calculate_score(remaining)
        scores.append(partial)
    return scores    

def calculate_part1():
    inputs = common.read_input_to_function_list("input//day10//input.txt", str)
    total = parse_corrupted_chunks(inputs)
    print(total)


def calculate_part2():
    inputs = common.read_input_to_function_list("input//day10//input.txt", str)
    incomplete_chunks = discard_corrupted_chunks(inputs)
    # print(incomplete_chunks)
    scores = parse_incomplete_chunks(incomplete_chunks)
    scores.sort()
    mid_index = int(len(scores)/2)
    print(scores[mid_index])

# execute
# calculate_part1()
calculate_part2()