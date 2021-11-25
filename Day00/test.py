import sys

# Add the parent folder path to the sys.path list
sys.path.append('../Common/')

# Now you can import your module
# pylint: disable=import-error
import common

common.echo("start")

with open("input\\input.txt") as file:
    line = file.readline()
    count = 1
    while line:
        print("Line {}: {}".format(count, line.strip()))
        value = int(line.strip())
        line = file.readline()
        count += 1

common.echo("end")