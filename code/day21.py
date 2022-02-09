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



def create_rolls():
    rolls_list = []
    for i in [1, 2, 3]:
        for j in [1, 2, 3]:
            for k in [1, 2, 3]:
                rolls_list.append(i+j+k)
    rolls_dict = {}
    for rolls in rolls_list:
        if rolls in rolls_dict:
            rolls_dict[rolls] += 1
        else:
            rolls_dict[rolls] = 1
    return rolls_dict


def player_play(pos, score, rolls):
    for roll in rolls:
        pos = move(pos, roll)
    score += pos
    return pos, score


def turn_play(p1_pos, p1_score, p2_pos, p2_score, p1_wins, p2_wins):
    rolls_dict = create_rolls()
    for rolls1 in rolls_dict.keys():
        for rolls2 in rolls_dict.keys():
            # print(rolls)
            # print(p1_pos, p1_score, p2_pos, p2_score, p1_wins, p2_wins)
            # player 1 play
            new_p1_pos, new_p1_score = player_play(p1_pos, p1_score, [rolls1])
            if new_p1_score >= 21:
                # print("player 1 wins")
                p1_wins += rolls_dict[rolls1]
                break

            # player 2 play
            new_p2_pos, new_p2_score = player_play(p2_pos, p2_score, [rolls2])
            if new_p2_score >= 21:
                # print("player 2 wins")
                p2_wins += rolls_dict[rolls2]
                continue

            # print(new_p1_pos, new_p1_score, new_p2_pos, new_p2_score, p1_wins, p2_wins)
            new_p1_wins, new_p2_wins = turn_play(new_p1_pos, new_p1_score, new_p2_pos, new_p2_score, p1_wins, p2_wins)
            p1_wins = new_p1_wins
            p2_wins = new_p2_wins
    # print(p1_wins, p2_wins)
    return p1_wins, p2_wins # , new_universes


def calculate_part2(player1_start_pos, player2_start_pos):
    print(create_rolls())
    p1_wins, p2_wins = turn_play(player1_start_pos, 0, player2_start_pos, 0, 0, 0)
    print(p1_wins, p2_wins)
    # print(len(new_universes))

# execute
# calculate_part1(4, 8)
# calculate_part1(1, 3)
calculate_part2(4, 8)