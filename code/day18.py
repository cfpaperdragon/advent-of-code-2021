# day00
import common
import uuid
import math

def get_unique_identifier():
    return str(uuid.uuid4())

# a snailfish_number is a tree
# a tree is a dictionary, each key is a node
# to identify each node we get a unique identifier (guid)
def create_snailfish_number(n, tree, parent):
    new_node = get_unique_identifier()

    if isinstance(n[0], list):
        left = create_snailfish_number(n[0], tree, new_node)
    else:
        left = n[0]

    if isinstance(n[1], list):
        right = create_snailfish_number(n[1], tree, new_node)
    else:
        right = n[1]

    tree[new_node] = (parent, left, right)
    return new_node
        

def node_to_string(tree, node):
    node_string = "["
    tree_node = tree[node]
    # check left
    if isinstance(tree_node[1], str):
        node_string += node_to_string(tree, tree_node[1])
    else:
        node_string += str(tree_node[1])
    node_string += ","
    # check right
    if isinstance(tree_node[2], str):
        node_string += node_to_string(tree, tree_node[2])
    else:
        node_string += str(tree_node[2])
    node_string += "]"
    return node_string


def snailfish_number_to_string(tree, root):
    return node_to_string(tree, root)
    

def add_snailfish_number(tree1, root1, tree2, root2):
    new_tree = {**tree1, **tree2} # wot?
    new_node = get_unique_identifier()
    # update older roots to point to this new root
    node1 = new_tree[root1]
    new_tree[root1] = (new_node, node1[1], node1[2])
    node2 = new_tree[root2]
    new_tree[root2] = (new_node, node2[1], node2[2])
    new_tree[new_node] = (None, root1, root2)
    return new_tree, new_node


def count_tree_levels(tree, root, level):
    node = tree[root]
    # left
    if isinstance(node[1], int):
        left = level + 1
    else:
        left = count_tree_levels(tree, node[1], level + 1)

    # right
    if isinstance(node[2], int):
        right = level + 1
    else:
        right = count_tree_levels(tree, node[2], level + 1)

    return max(left, right)

# returns the node where 10 was found or if none, returns None
def find_node_above_10(tree, start_node):
    node = tree[start_node]
    # left
    if isinstance(node[1], int):
        if node[1] >= 10:
            left = start_node
        else:
            left = None
    else:
        left = find_node_above_10(tree, node[1])

    # right
    if isinstance(node[2], int):
        if node[2] >= 10:
            right = start_node
        else:
            right = None
    else:
        right = find_node_above_10(tree, node[2])

    if left != None and right != None:
        return left # leftmost first
    elif left == None:
        return right
    elif right == None:
        return left

    return None


def push_left_part(tree, node_exploding, parent, value):
    # print("node_exploding", node_exploding, "parent", parent, "value", value)
    current = parent
    previous_node = node_exploding
    while tree[current][0] != None: # root condition
        # is the previous node on left or right
        if previous_node == str(tree[current][1]): #left
            # need to continue going up
            previous_node = current
            current = tree[current][0]
        else: # right
            # stop going up, need to go down
            if isinstance(tree[current][1], int):
                # need to change this one
                current_node = tree[current]
                tree[current] = (current_node[0], current_node[1] + value, current_node[2])
                return
            else:
                # first go to left, then go to right
                current = tree[current][1]
                # need to navigate further down to the right
                break

    if tree[current][0] == None: # reached root
        if previous_node == str(tree[current][1]): # left
            return # cannot push left, there's nothing to the left
        else:
            if isinstance(tree[current][1], int):
                # need to change this one
                current_node = tree[current]
                tree[current] = (current_node[0], current_node[1] + value, current_node[2])
                return
            else:
                current = tree[current][1]

    while isinstance(tree[current][2], str): # while I can, go down to the right
        current = tree[current][2]

    current_node = tree[current]
    tree[current] = (current_node[0], current_node[1], current_node[2] + value) 
    return   


def push_right_part(tree, node_exploding, parent, value):
    # print("node_exploding", node_exploding, "parent", parent, "value", value)
    current = parent
    previous_node = node_exploding
    while tree[current][0] != None: # root condition
        # print(current, tree[current])
        # is the previous node on left or right
        if previous_node == str(tree[current][2]): #right
            # need to continue going up
            previous_node = current
            current = tree[current][0]
        else: # left
            # stop going up, need to go down
            if isinstance(tree[current][2], int):
                # need to change this one
                current_node = tree[current]
                # print(current_node)
                tree[current] = (current_node[0], current_node[1], current_node[2] + value)
                return
            else:
                # first go to right, then go to left
                current = tree[current][2]
                # need to navigate further down to the left
                break

    if tree[current][0] == None: # reached root
        if previous_node == str(tree[current][2]): # right
            return # cannot push right, there's nothing to the right
        else:
            if isinstance(tree[current][2], int):
                # need to change this one
                current_node = tree[current]
                # print(current_node)
                tree[current] = (current_node[0], current_node[1], current_node[2] + value)
                return
            else:
                current = tree[current][2]

    while isinstance(tree[current][1], str): # while I can, go down to the left
        current = tree[current][1]

    # print(tree[current])
    current_node = tree[current]
    tree[current] = (current_node[0], current_node[1] + value, current_node[2])
    return 

    
# receives the node to explode
# must push left to left and right to right
# must update parent with 0 instead of the node
# at the end, the node poofs
def explode_node(tree, node):
    node_to_explode = tree[node]
    parent = node_to_explode[0]
    left_part = node_to_explode[1]
    right_part = node_to_explode[2]
    push_left_part(tree, node, parent, left_part) # go to parent to find left part
    push_right_part(tree, node, parent, right_part) # go to parent to find right part
    # update parent
    parent_node = tree[parent]
    # is the node on the right or left of parent?
    if node == str(parent_node[1]):
        tree[parent] = (parent_node[0], 0, parent_node[2])
    else:
        tree[parent] = (parent_node[0], parent_node[1], 0)
    tree.pop(node)
    return True


def explode_snailfish_number(tree, node, level):
    tree_node = tree[node]
    # print(level, node, tree_node)
    if level == 4:
        # first check left
        if isinstance(tree_node[1], str):
            # print("left")
            # print("explode", tree[tree_node[1]])
            return explode_node(tree, tree_node[1])
        # then check right
        elif isinstance(tree_node[2], str): 
            # print("right")
            # print("explode", tree[tree_node[2]])
            return explode_node(tree, tree_node[2])
    else:
         # first check left
        if isinstance(tree_node[1], str):
            result = explode_snailfish_number(tree, tree_node[1], level+1)
            if result:
                return result
        # then check right
        if isinstance(tree_node[2], str): 
            result = explode_snailfish_number(tree, tree_node[2], level+1)
            if result:
                return result

    return False


# receives the node where the value needed to split exists
# indicates if is the one on the left or the right
def split_node(tree, node, isleft):
    new_node = get_unique_identifier()
    if isleft:
        value = tree[node][1]
        tree[new_node] = (node, math.floor(value/2), math.ceil(value/2))
        tree[node] = (tree[node][0], new_node, tree[node][2])
    else:
        value = tree[node][2]
        tree[new_node] = (node, math.floor(value/2), math.ceil(value/2))
        tree[node] = (tree[node][0], tree[node][1], new_node)
    return True


# detects nodes to split and splits them
def split_snailfish_number(tree, start_node):
    node = tree[start_node]
    # print(start_node, node)
    # left
    if isinstance(node[1], int):
        if node[1] >= 10:
            # print("split", tree[start_node], "left")
            left = split_node(tree, start_node, True)
        else:
            left = False
    else:
        left = split_snailfish_number(tree, node[1])
    if left:
        return left

    # right
    if isinstance(node[2], int):
        if node[2] >= 10:
            # print("split", tree[start_node], "right")
            right = split_node(tree, start_node, False)
        else:
            right = False
    else:
        right = split_snailfish_number(tree, node[2])
    if right:
        return right

    return left or right


def reduce_snailfish_number(tree, root_node):
    # first we need to explode
    while True:
        # print(eval(snailfish_number_to_string(tree, root_node)))
        levels = count_tree_levels(tree, root_node, 0)
        if levels > 4:
            # print("explode")
            explode_snailfish_number(tree, root_node, 1)
            continue
        if find_node_above_10(tree, root_node):
            # print("split")
            split_snailfish_number(tree, root_node)
            continue
        break


def add_all(tree_list):
    tree_item = tree_list[0]
    tree = tree_item[0]
    root_node = tree_item[1]
    for i in range(1, len(tree_list)):
        tree_item = tree_list[i]
        tree, root_node = add_snailfish_number(tree, root_node, tree_item[0], tree_item[1])
        # print(eval(snailfish_number_to_string(tree, root_node)))
        reduce_snailfish_number(tree, root_node)
        # print(eval(snailfish_number_to_string(tree, root_node)))
    return tree, root_node


def convert_to_trees(number_list):
    trees = []
    for n in number_list:
        # print(n)
        snailfish_tree = {}
        root_node = create_snailfish_number(n, snailfish_tree, None)
        trees.append((snailfish_tree, root_node))
        # print(eval(snailfish_number_to_string(snailfish_tree, root_node)))
        # levels = count_tree_levels(snailfish_tree, root_node, 0)
        # print(levels)
        # node = find_node_above_10(snailfish_tree, root_node)
        # print(node)
        # print(snailfish_tree[node])
    return trees


def calculate_magnitude(tree, node):
    tree_node = tree[node]
    # get left
    if isinstance(tree_node[1], int):
        left = tree_node[1]
    else: 
        left = calculate_magnitude(tree, tree_node[1])

    # get right
    if isinstance(tree_node[2], int):
        right = tree_node[2]
    else:
        right = calculate_magnitude(tree, tree_node[2])

    return 3 * left + 2 * right



def calculate_part1():
    inputs = common.read_input_to_function_list("input//day18//input.txt", eval)
    trees = convert_to_trees(inputs)
    # tree = trees[0]
    # print(eval(snailfish_number_to_string(tree[0], tree[1])))
    # levels = count_tree_levels(tree[0], tree[1], 0)
    # print(levels)
    # explode_snailfish_number(tree[0], tree[1], 1)
    # split_snailfish_number(tree[0], tree[1])
    # print(eval(snailfish_number_to_string(tree[0], tree[1])))
    result = add_all(trees)
    # print(result)
    print(eval(snailfish_number_to_string(result[0], result[1])))

    # magnitude_example = eval("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
    # tree = {}
    # root = create_snailfish_number(magnitude_example, tree, None)
    magnitude = calculate_magnitude(result[0], result[1])
    print(magnitude)
   

def calculate_part2():
    inputs = common.read_input_to_function_list("input//day18//input.txt", eval)
    trees = convert_to_trees(inputs)
    magnitudes = []
    for i in range(len(trees)):
        for j in range(1, len(trees)):
            tree1 = trees[i]
            # print(eval(snailfish_number_to_string(tree1[0], tree1[1])))
            tree2 = trees[j]
            # print(eval(snailfish_number_to_string(tree2[0], tree2[1])))
            tree, root_node = add_snailfish_number(tree1[0], tree1[1], tree2[0], tree2[1])
            # print(eval(snailfish_number_to_string(tree, root_node)))
            reduce_snailfish_number(tree, root_node)
            # print(eval(snailfish_number_to_string(tree, root_node)))
            magnitude = calculate_magnitude(tree, root_node)
            # print(magnitude)
            magnitudes.append(magnitude)
            # trade order
            tree, root_node = add_snailfish_number(tree2[0], tree2[1], tree1[0], tree1[1])
            # print(eval(snailfish_number_to_string(tree, root_node)))
            reduce_snailfish_number(tree, root_node)
            # print(eval(snailfish_number_to_string(tree, root_node)))
            magnitude = calculate_magnitude(tree, root_node)
            # print(magnitude)
            magnitudes.append(magnitude)
    print(max(magnitudes))
    

# execute
# calculate_part1()
calculate_part2()