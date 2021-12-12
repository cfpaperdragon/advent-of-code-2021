# day12
import common
import matrix as mat

# my graph will be a matrix
def create_graph(input_list):
    # first get a list of all nodes
    nodes = []
    connections = []
    for i in input_list:
       node_list = i.split("-")
       connections.append((node_list[0], node_list[1]))
       if node_list[0] not in nodes:
           nodes.append(node_list[0])
       if node_list[1] not in nodes:
           nodes.append(node_list[1])
    graph = {}
    for nodeY in nodes:
        graph[nodeY] = {}
        for nodeX in nodes:
            graph[nodeY][nodeX] = 0
    
    for connection in connections:
        graph[connection[0]][connection[1]] = 1
        graph[connection[1]][connection[0]] = 1
        
    return graph

def print_graph(graph):
    # first row print keys
    key_rows = "|".rjust(7)
    for key in graph.keys():
        key_rows += key.ljust(6)
    print(key_rows)
    for keyY in graph.keys():        
        row = keyY.ljust(6) + "|"
        for keyX in graph.keys():
            row += str(graph[keyY][keyX]).ljust(6) 
        print(row)


def can_repeat_small_cave(path):
    lowercase_nodes = {}
    for node in path:
        if node.islower():
            if node in lowercase_nodes.keys():
                return False
            else:
                lowercase_nodes[node] = 1
                continue
    return True


def calculate_paths(graph, start_node, part2=False):
    paths = []
    # a path is made of the list of the nodes visited so far, where the last node
    # when we start, there is only one path
    paths.append([start_node])
    # this list will save unique paths that have reached the end
    complete_paths = []

    # while there are paths to complete
    while len(paths) > 0:
        new_paths = []
        for path in paths:
            current_node = path[-1]
            for node in graph[current_node].keys():
                if graph[current_node][node] == 1: # reachable
                    if node == "start": # can never go back to start
                        continue
                    if node in path and node.islower():
                        if not part2: 
                            continue # cannot go to small cave more than once
                        else:
                            if not can_repeat_small_cave(path):
                                continue
                    copy_path = path.copy()
                    copy_path.append(node)

                    if node == "end":
                        complete_paths.append(copy_path)
                    else:
                        new_paths.append(copy_path)
        paths = new_paths
    return complete_paths


def calculate_part1():
    inputs = common.read_input_to_function_list("input//day12//input.txt", str)
    graph = create_graph(inputs)
    print_graph(graph)
    complete_paths = calculate_paths(graph, "start")
    # for p in complete_paths:
    #     print(p)
    print(len(complete_paths))

def calculate_part2():
    inputs = common.read_input_to_function_list("input//day12//input.txt", str)
    graph = create_graph(inputs)
    print_graph(graph)
    complete_paths = calculate_paths(graph, "start", True)
    # for p in complete_paths:
    #     print(p)
    print(len(complete_paths))

# execute
# calculate_part1()
calculate_part2()