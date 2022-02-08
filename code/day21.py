# day21

def roll_dice(previous):
    if previous >= 100:
        return 1
    else:
        return previous + 1


def move(previous_pos, steps):
    new_pos = previous_pos + steps
    if new_pos > 10:
        divided = new_pos % 10
        if divided == 0:
            return 10
        else:
            return divided
    else:
        return new_pos
        
    

def calculate_part1(player1_start_pos, player2_start_pos):
    player1_pos = player1_start_pos
    player2_pos = player2_start_pos

    player1_score = 0
    player2_score = 0

    dice_counter = 0
    previous_roll = 0

    while True:
        for i in range(3):
            # print("player1 start", player1_pos, previous_roll)
            previous_roll = roll_dice(previous_roll)
            dice_counter += 1
            player1_pos = move(player1_pos, previous_roll)
            
        # print("player1 end", player1_pos, previous_roll, player1_score)
        player1_score += player1_pos

        if player1_score >= 1000:
            break

        for j in range(3):
            previous_roll = roll_dice(previous_roll)
            dice_counter += 1
            player2_pos = move(player2_pos, previous_roll)
            
        player2_score += player2_pos

        if player2_score >= 1000:
            break
        
        # print("player1:", player1_score)
        # print("player2:", player2_score)
        
    
    print("player1:", player1_score)
    print("player2:", player2_score)
    print("number of rolls:", dice_counter)
    #do other stuff
    print(min(player1_score, player2_score)*dice_counter)

def calculate_part2(player1_start_pos, player2_start_pos):
    print("boo")

# execute
# calculate_part1(4, 8)
# calculate_part1(1, 3)
calculate_part2(4, 8)