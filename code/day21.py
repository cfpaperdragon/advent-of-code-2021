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


def turn_play(game_state_dict):
    rolls_dict = create_rolls()
    game_state_dict_result = {}
    for game_state in game_state_dict.keys():

        # player 1 rolls
        for rolls1 in rolls_dict.keys():
            
            # player 2 rolls
            for rolls2 in rolls_dict.keys():

                new_p1_pos, new_p1_score = player_play(game_state[0], game_state[1], [rolls1])

                new_p2_pos, new_p2_score = player_play(game_state[2], game_state[3], [rolls2])

                if new_p1_score >= 21:
                    new_game_state = (new_p1_pos, new_p1_score, new_p2_pos, new_p2_score, True, 1)
                    if new_game_state in game_state_dict_result:
                        game_state_dict_result[new_game_state] += game_state_dict[game_state]*(rolls_dict[rolls1]*rolls_dict[rolls2]) # add these universes to the next
                    else:
                        game_state_dict_result[new_game_state] = game_state_dict[game_state]*(rolls_dict[rolls1]*rolls_dict[rolls2])
                    break # because no need to continue this branch

                if new_p2_score >= 21:
                    new_game_state = (new_p1_pos, new_p1_score, new_p2_pos, new_p2_score, True, 2)
                    if new_game_state in game_state_dict_result:
                        game_state_dict_result[new_game_state] += game_state_dict[game_state]*(rolls_dict[rolls1]*rolls_dict[rolls2]) # add these universes to the next
                    else:
                        game_state_dict_result[new_game_state] = game_state_dict[game_state]*(rolls_dict[rolls1]*rolls_dict[rolls2])
                    continue

                new_game_state = (new_p1_pos, new_p1_score, new_p2_pos, new_p2_score, False, 0)
                if new_game_state in game_state_dict_result:
                    game_state_dict_result[new_game_state] += game_state_dict[game_state]*(rolls_dict[rolls1]*rolls_dict[rolls2]) # add these universes to the next
                else:
                    game_state_dict_result[new_game_state] = game_state_dict[game_state]*(rolls_dict[rolls1]*rolls_dict[rolls2])

    return game_state_dict_result


def calculate_part2(player1_start_pos, player2_start_pos):
    game_state_dict = {}
    # 0 = player1 pos
    # 1 = player1 score
    # 2 = player2 pos
    # 3 = player2 score
    # 4 = Is final state
    # 5 = player that won (in final state)
    initial_game_state = (player1_start_pos, 0, player2_start_pos, 0, False, 0)
    game_state_dict[initial_game_state] = 1
    game_state_dict_result = turn_play(game_state_dict)
    game_state_dict_final = {}
    # filter game results that reached a final state
    counter = 1
    while counter < 20:
        counter += 1
        game_state_dict_filtered = {}
        for game_state in game_state_dict_result:
            if game_state[4]:
                if game_state in game_state_dict_final:
                    game_state_dict_final[game_state] += game_state_dict_result[game_state]
                else:
                    game_state_dict_final[game_state] = game_state_dict_result[game_state]
            else:
                game_state_dict_filtered[game_state] = game_state_dict_result[game_state]

        print(len(game_state_dict_result), len(game_state_dict_filtered))
        game_state_dict_result = turn_play(game_state_dict_filtered)
    
    print(len(game_state_dict_final))
    player1_wins = 0
    player2_wins = 0
    for game_state in game_state_dict_final:
        if game_state[5] == 1:
            player1_wins += game_state_dict_final[game_state]
        else:
            player2_wins += game_state_dict_final[game_state]

    print(player1_wins, player2_wins)

    # print(len(new_universes))
    # scratch all that
    # let's create states and iterate over the states
    # since the states repeat themselves, keep them in a dictionary, counting the number of universes in that state
    # every round, iterate over the states without a winner - there aren't that many rounds

# execute
# calculate_part1(4, 8)
# calculate_part1(1, 3)
# calculate_part2(4, 8)
calculate_part2(1, 3)