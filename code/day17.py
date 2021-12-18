# day17

def drag_function(x):
    if x > 0:
        return x - 1
    elif x < 0:
        return x + 1
    else: # x == 0
        return 0


def calculate_position(position, velocity):
    x = position[0] + velocity[0]
    y = position[1] + velocity[1]
    return (x, y)


def calculate_velocity(velocity):
    x = drag_function(velocity[0])
    y = velocity[1] - 1
    return (x, y)


def simulate(start_velocity, target, step):
    count_steps = 0
    position = (0, 0)
    velocity = start_velocity
    print("step:", count_steps, "position:", position, "velocity:", velocity)
    while count_steps < step:
        count_steps += 1
        position = calculate_position(position, velocity)
        velocity = calculate_velocity(velocity)
        print("step:", count_steps, "position:", position, "velocity:", velocity)
        


def calculate_part1():
    # example: target area: x=20..30, y=-10..-5
    target_x0 = 20
    target_x1 = 30
    target_y0 = -10
    target_y1 = -5

    start_velocity_example = (6, 9)

    simulate(start_velocity_example, (target_x0, target_x1, target_y0, target_y1), 20)

    # 1. I want that velocity x reaches 0 in the target area
    # 2. velocity y reaches 0 at the highest point



def calculate_part2():
    print("part 2")
    #do other stuff

# execute
calculate_part1()
# calculate_part2()