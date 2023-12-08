from math import ceil

def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        sline = line.rstrip()
        data.append(sline)
        
    file.close()
    if debug: print(data)
    return data

def format_data(data):
    instructions = data[0]
    nodes = {}
    for i in range(2, len(data)):
        row = data[i]
        nodes[row[0:3]] = {
            'L': row[7:10],
            'R': row[12:15],
        }
    return instructions, nodes

def part1(instructions, nodes):
    steps = 0
    current_node = 'AAA'
    if current_node not in nodes:
        return 'impossible'
    while True:
        if current_node == 'ZZZ':
            break
        instruction = instructions[steps%len(instructions)]
        current_node = nodes[current_node][instruction]
        steps += 1
        
    return steps

def part2(instructions, nodes):
    starting_nodes = {}
    for node in nodes:
        if node[2] == 'A':
            starting_nodes[node] = {
                'min_steps': 0,
                'z_node': None,
                'z_steps': 0,
            }
    for node in starting_nodes:
        steps = 0
        current_node = node
        while True:
            instruction = instructions[steps%len(instructions)]
            steps += 1
            current_node = nodes[current_node][instruction]
            if current_node[2] == 'Z':
                starting_nodes[node]['z_node'] = current_node
                starting_nodes[node]['min_steps'] = steps
                break
    
    # turns out min_steps == z_steps so you could skip this entirely
    for node in starting_nodes:
        steps = 0
        current_node = starting_nodes[node]['z_node']
        while True:
            instruction = instructions[steps%len(instructions)]
            steps += 1
            current_node = nodes[current_node][instruction]
            if current_node == starting_nodes[node]['z_node']:
                starting_nodes[node]['z_steps'] = steps
                break
    
    # the min_steps all coincidentally require all of the instructions, so that's a common factor
    min_steps = len(instructions)
    for node in starting_nodes:
        # all of the min_steps (sans instruction length factor) are prime, so juts multiply
        min_steps *= starting_nodes[node]['min_steps']/len(instructions)
    
    return int(min_steps)

def run_program(debug=False):
    file_path = 'test2.txt' if debug else 'day08.txt'
    
    data = read_data(file_path, debug)
    instructions, nodes = format_data(data)

    if debug:
        print(instructions)
        print(nodes)

    print(part1(instructions, nodes)) # 23147
    print(part2(instructions, nodes)) # 22289513667691

run_program(False)