# day00
# always use methods, can be easier to reuse code
# move common stuff to common

import common

def read_input():
    common.echo("start")

    with open("input\\day00\\input.txt") as file:
        line = file.readline()
        count = 1
        while line:
            print("Line {}: {}".format(count, line.strip()))
            value = int(line.strip())
            line = file.readline()
            count += 1

    common.echo("end")

def calculate_part1():
    read_input()
    #do other stuff

def calculate_part2():
    common.echo("part 2")
    #do other stuff