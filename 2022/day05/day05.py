from copy import deepcopy

def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        data.append(line)
        
    file.close()
    if debug: print(data)
    return data

class Instruction:
    def __init__(self, input) -> None:
        input = input.replace('move ', '').replace('from ','').replace('to ','')
        parts = input.split()
        self.count = int(parts[0])
        self.src = int(parts[1])
        self.dst = int(parts[2])

    def __repr__(self) -> str:
        return '{0}→{1}: move {2}'.format(
            self.src,
            self.dst,
            self.count,
        )

def format_data(data):
    blank_line = 0
    while blank_line < len(data):
        if not data[blank_line].rstrip():
            break
        blank_line += 1
    stacks = {int(n): [] for n in data[blank_line-1].split()}
    line = blank_line-2
    while line >= 0:
        for num in stacks:
            crate = data[line][(num-1)*4:num*4-1]
            if not crate.rstrip():
                continue
            else:
                stacks[num].append(crate)
        line -= 1
    
    instructions = []
    for line in range(blank_line+1, len(data)):
        instructions.append(Instruction(data[line]))

    return stacks, instructions

def move_crates(original_stacks, instructions, keep_order):
    stacks = deepcopy(original_stacks)
    for i in instructions:
        crates = stacks[i.src][-i.count:]
        if not keep_order:
            crates.reverse()
        new_len = len(stacks[i.src]) - i.count
        stacks[i.src] = stacks[i.src][0:new_len]
        stacks[i.dst] = stacks[i.dst] + crates
    top_crates = ''.join([stacks[stack][-1:][0][1] for stack in stacks])
    return top_crates

def part1(stacks, instructions):
    return move_crates(stacks, instructions, False)

def part2(stacks, instructions):
    return move_crates(stacks, instructions, True)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day05.txt'
    
    data = read_data(file_path, debug)
    stacks, instructions = format_data(data)

    if debug:
        print(stacks)
        print(instructions)

    print(part1(stacks, instructions)) # FWSHSPJWM
    print(part2(stacks, instructions)) # PWPWHGFZS

run_program(False)