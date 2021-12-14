# day04
import common
from datetime import datetime

def parse_inputs(input_list):
    template = input_list[0]
    rules = {}
    for i in range(2, len(input_list)):
        rule_parts = input_list[i].split("->")
        rule = (rule_parts[0].strip(), rule_parts[1].strip())
        rules[rule[0]] = rule[1]

    return template, rules


def apply_template(template, rules, number_steps):
    count = 0
    polymer = template
    while count < number_steps:
        count += 1
        # print(count)
        new_polymer = []
        for i in range(1, len(polymer)):
            pair = polymer[i-1:i+1]
            if pair in rules.keys():
                new_element = rules[pair]
            if len(new_polymer) == 0:
                new_polymer.append(pair[0])
            new_polymer.append(new_element)
            new_polymer.append(pair[1])
        polymer = "".join(new_polymer)
    return polymer


def count_elements(polymer, elements_count):
    for i in range(len(polymer)):
        element = polymer[i]
        if element in elements_count.keys():
            elements_count[element] += 1
        else:
            elements_count[element] = 1
    return elements_count


def calculate_part1(num_steps = 10):
    inputs = common.read_input_to_function_list("input//day14//example.txt", str)
    # print(inputs)
    template, rules = parse_inputs(inputs)
    # print(template)
    # print(rules)
    polymer = apply_template(template, rules, num_steps)
    elements_count = count_elements(polymer, {})
    print(elements_count)
    print(max(elements_count.values()) - min(elements_count.values()))


def calculate_part2():
    inputs = common.read_input_to_function_list("input//day14//input.txt", str)
    # print(inputs)
    template, rules = parse_inputs(inputs)
    # print(template)
    # print(rules)
    cache = {}
    for rule in rules.keys():
        print(rule)
        polymer_part = apply_template(rule, rules, 20)
        # only save the middle part
        cache[rule] = count_elements(polymer_part[1:], {})
    # print(cache)
    polymer_20_step = apply_template(template, rules, 20)
    # made_from_parts = "N" + cache["NN"] + cache["NC"] + cache["CB"]
    # polymer = apply_template(template, rules, 4)
    # print(polymer == made_from_parts)
    elements_count = count_elements(template[0], {})
    for i in range(1, len(polymer_20_step)):
            pair = polymer_20_step[i-1:i+1]
            if pair in cache.keys():
                counted_elements = cache[pair]
            for key in counted_elements.keys():
                if key in elements_count.keys():
                    elements_count[key] += counted_elements[key]
                else:
                    elements_count[key] = counted_elements[key]
    print(elements_count)
    print(max(elements_count.values()) - min(elements_count.values()))

# execute
# calculate_part1()
# calculate_part2()

# I'd like to redo it the right way.
# meaning, count the pairs and then count the letters
# it is similar of what I did but for all steps
# when using pairs, only count the last char of each pair plus the first char

def apply_template_count_pairs(template, rules, number_steps):
    count = 0
    pairs = {}
    # initialize pairs
    for i in range(1, len(template)):
        pair = template[i-1:i+1]
        if pair in pairs.keys():
            pairs[pair] += 1
        else:
            pairs[pair] = 1
    while count < number_steps:
        count += 1
        new_pairs = {}
        for pair in pairs.keys():
            number_of_pairs = pairs[pair]
            new_element = rules[pair]
            new_pair_1 = pair[0] + new_element
            new_pair_2 = new_element + pair[1]
            if new_pair_1 in new_pairs.keys():
                new_pairs[new_pair_1] += number_of_pairs
            else:
                new_pairs[new_pair_1] = number_of_pairs

            if new_pair_2 in new_pairs.keys():
                new_pairs[new_pair_2] += number_of_pairs
            else:
                new_pairs[new_pair_2] = number_of_pairs
        pairs = new_pairs
    return pairs

def count_elements_with_pairs(pairs):
    elements = {}
    for p in pairs.keys():
        element = p[1] # only last character
        if element in elements.keys():
            elements[element] += pairs[p]
        else:
            elements[element] = pairs[p]
    return elements


def calculate_the_good_way(steps=10):
    inputs = common.read_input_to_function_list("input//day14//input.txt", str)
    template, rules = parse_inputs(inputs)
    pairs = apply_template_count_pairs(template, rules, steps)
    # print(pairs)
    elements = count_elements_with_pairs(pairs)
    # add the first character
    elements[template[0]] += 1
    # print(elements)
    print(max(elements.values()) - min(elements.values()))


before = datetime.now()

# calculate_the_good_way(10)
calculate_the_good_way(40)
after = datetime.now()

print("execution time", after - before)