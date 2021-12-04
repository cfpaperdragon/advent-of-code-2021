# day04
import common

def parse_numbers(number_string):
    number_list = number_string.strip().split(",")
    final_number_list = []
    for i in range(len(number_list)):
        final_number_list.append(int(number_list[i]))
    return final_number_list

# what's a bingo card
# a bingo card is a matrix 5x5 of (number, string)
# string is "" at the start of the game, "X" if it was marked

def parse_card(card_string_list):
    card = {}
    for i in range(len(card_string_list)):
        card[i] = {}
        card_line_list = card_string_list[i].split()
        for j in range(len(card_line_list)):
            card[i][j] = (int(card_line_list[j]), "")
    return card


def get_number(card, x, y):
    return card[y][x][0]

def mark_number(card, x, y):
    card[y][x] = (card[y][x][0], "X")
    # I don't know if I have to return the card here

def card_mark_number(number, card):
    for y in card.keys():
        for x in card[y].keys():
            if get_number(card, x, y) == number:
                mark_number(card, x, y)
                return



def is_marked(card, x, y):
    return card[y][x][1] == "X"


def have_line(card):
    for y in card.keys():
        count_marks = 0
        for x in card[y].keys():
            if is_marked(card, x, y):
                count_marks += 1
        if count_marks == len(card[y].keys()):
            return True
    return False


def have_column(card):
    # print_card(card, True)
    for x in card[0].keys():
        count_marks = 0
        for y in card.keys():
            if is_marked(card, x, y):
                count_marks += 1
        if count_marks == len(card.keys()):
            return True
    return False


def print_card(card, with_marks = False):
    for y in card.keys():
        row = ""
        for x in card[y].keys():
            if with_marks:
                row += str(card[y][x][0]) + "(" + str(card[y][x][1]) + ")" + " "
            else:
                row += str(card[y][x][0]) + " "
        print(row)


def print_card_list(card_list):
    for card in card_list:
        print_card(card)
        print("")


def read_bingo(filename):
    number_list = []
    cards_list = []
    with open(filename) as file:
        # 1st line are the numbers
        line = file.readline()
        number_list = parse_numbers(line)
        # 2nd line is blank
        line = file.readline()
        # 3rd line starts the card
        line = file.readline()
        card_string_list = []
        while line:
            # print("line:", line)
            # print("card_string_list:", card_string_list)
            value = line.strip()
            if len(value) == 0:
                # reached end of the card
                cards_list.append(parse_card(card_string_list))
                card_string_list = []
            else:
                card_string_list.append(value)

            line = file.readline()
        cards_list.append(parse_card(card_string_list))
    return number_list, cards_list


def bingo_loop(number_list, card_list):
    for number in number_list:
        for card in card_list:
            card_mark_number(number, card)
            if have_line(card):
                # game ends
                return number, card
            if have_column(card):
                # game ends
                return number, card


def calculate_score(card, number):
    sum_unmarked = 0
    for y in card.keys():
        for x in card.keys():
            if not is_marked(card, x, y):
                sum_unmarked += get_number(card, x, y)
    return sum_unmarked * number


def calculate_part1():
    number_list, card_list = read_bingo("input//day04//input.txt")
    # print(number_list)
    # print_card_list(card_list)
    number, card = bingo_loop(number_list, card_list)
    # print(number)
    # print_card(card)
    score = calculate_score(card, number)
    print(score)


def bingo_loop_last_to_win(number_list, card_list):
    cards = card_list
    for number in number_list:
        # print(number)
        cards_to_remove = []
        for card in cards:
            card_mark_number(number, card)
            if have_line(card) or have_column(card):
                # print_card(card, True)
                # mark card to be removed from pool of cards
                # more than one card can complete in one go
                cards_to_remove.append(card)
               
        for card in cards_to_remove:
            cards.remove(card)
            if len(cards) == 0:
                # game ends
                return number, card


def calculate_part2():
    number_list, card_list = read_bingo("input//day04//input.txt")
    # print(number_list)
    # print_card_list(card_list)
    number, card = bingo_loop_last_to_win(number_list, card_list)
    print(number)
    print_card(card, True)
    score = calculate_score(card, number)
    print(score)

# execute
# calculate_part1()
calculate_part2()