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


def calculate_height(start_velocity):
    # max height is when velocity y reaches 0
    # vy = vy0 - N
    step = start_velocity[1]
    height = start_velocity[1] * step - ((step*step) - step)/2
    return height


def simulate(start_velocity, target, step):
    count_steps = 0
    position = (0, 0)
    velocity = start_velocity
    # print("step:", count_steps, "position:", position, "velocity:", velocity)
    while count_steps < step:
        count_steps += 1
        position = calculate_position(position, velocity)
        velocity = calculate_velocity(velocity)
        # print("step:", count_steps, "position:", position, "velocity:", velocity)
        # check if it is on target
        if position[0] >= target[0] and position[0] <= target[1] and position[1] >= target[2] and position[1] <= target[3]:
            return True, count_steps
        # check if is over target and return False
        if position[0] >= target[1] or position[1] <= target[2]:
            return False, count_steps
    return False, count_steps
        


def calculate_part1(target_x0, target_x1, target_y0, target_y1, max_x, max_y, max_steps):
    # example: target area: x=20..30, y=-10..-5
    # target_x0 = 20
    # target_x1 = 30
    # target_y0 = -10
    # target_y1 = -5

    start_velocities_hit_target = []

    for x in range(1, max_x):
        for y in range(target_y0, max_y):
            start_velocity = (x, y)
            hit_target, step = simulate(start_velocity, (target_x0, target_x1, target_y0, target_y1), max_steps)
            # print("Hit target:", hit_target, "Steps:", step, "velocity:", start_velocity)
            if hit_target:
                height = calculate_height(start_velocity)
                start_velocities_hit_target.append((start_velocity, height))

    print(len(start_velocities_hit_target))
    velocity, max_height = max(start_velocities_hit_target, key=lambda item: item[1])
    print(velocity, max_height)

def calculate_part2():
    print("part 2")
    #do other stuff

# execute
# target area: x=211..232, y=-124..-69
# calculate_part1(20, 30, -10, -5, 100, 100, 100)
calculate_part1(211, 232, -124, -69, 400, 300, 100000)
