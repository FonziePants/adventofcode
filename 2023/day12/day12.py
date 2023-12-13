import time

def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        if not line.rstrip():
            continue
        sline = line.rstrip()
        data.append(sline)
        
    file.close()
    if debug: print(data)
    return data

def clean_springs(springs):
    # remove extra '.'s
    while '..' in springs:
        springs = springs.replace('..','.')
    # remove leading and trailing '.'s
    if springs[0] == '.': springs = springs[1:]
    if springs[-1] == '.': springs = springs[:-1]
    return springs

def deep_clean_springs_and_broken(springs, broken):
    last_broken = broken[-1]
    while springs[-last_broken:] == '#'*last_broken:
        springs = springs[:-last_broken]
        if springs[-1] in ['.', '?']:
            springs = springs[:-1]
        broken = broken[:-1]
        springs = clean_springs(springs)
        last_broken = broken[-1]
    return springs, broken

def is_match(springs, broken):
    template = ''
    for i in range(0, len(broken)):
        template += '#'*broken[i]
        if i < len(broken)-1:
            template += '.'
    return clean_springs(springs) == template

def possible_patterns(broken, unknown):
    options = []
    min_bin = (2**broken)-1
    max_bin = (2**unknown)
    for num in range(min_bin, max_bin):
        pattern = bin(num)[2:]
        pattern = '0'*(unknown-len(pattern)) + pattern
        if pattern.count('1') == broken:
            pattern = '0'*(unknown-len(pattern)) + pattern
            options.append(pattern.replace('1','#').replace('0','.'))
    return options

class SpringRow:
    def __init__(self, input: str, multiplier: int) -> None:
        parts = input.split()
        self.springs = clean_springs(parts[0]*multiplier)
        self.broken = [int(num) for i in range(0, multiplier) for num in parts[1].split(',')]
        self.springs, self.broken = deep_clean_springs_and_broken(self.springs, self.broken)
        self.broken_to_assign = sum(self.broken) - self.springs.count('#') 
        self.unknowns = self.springs.count('?')
    
    def arrangements(self):
        valid = 0
        patterns = possible_patterns(self.broken_to_assign, self.unknowns)
        for pattern in patterns:
            working_copy = self.springs
            for char in pattern:
                working_copy = working_copy.replace('?', char, 1)
            working_copy = clean_springs(working_copy)
            if is_match(working_copy, self.broken):
                valid += 1
        return valid

    def __repr__(self) -> str:
        return '{0} {1}'.format(self.springs, self.broken)

def format_data(data, multiplier):
    spring_rows = []
    for row in data:
        spring_rows.append(SpringRow(row, multiplier))
    return spring_rows

def run_part(data, multiplier, debug):
    spring_rows = format_data(data, multiplier)
    if debug: 
        print()
        for row in spring_rows:
            print(row)
        print()
    arrangements = 0
    for spring_row in spring_rows:
        start = 0
        if debug: start = time.time()
        arrangements += spring_row.arrangements()
        if debug: print('{0} seconds for {1}'.format(round(time.time()-start), spring_row))
    return arrangements

def part1(data, debug):
    return run_part(data, 1, debug)

def part2(data, debug):
    return run_part(data, 5, debug)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day12.txt'
    
    data = read_data(file_path, debug)

    print(part1(data, debug)) # 7286
    # print(part2(data, debug)) # TBD

run_program(True)