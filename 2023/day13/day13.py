def find_mirror(pattern, mirror_axis_0=None, mirror_index_0=-1, mirror_contents_0=None):
    mirror_index = None
    mirror_contents = None
    allow_discrepancy = mirror_axis_0 is not None

    for y in range(0, len(pattern)-1):
        if mirror_axis_0 == 'y' and mirror_index_0-1 == y:
            continue
        is_mirror = True
        edge = min(y, len(pattern)-y)
        discrepancy = -1

        for i in range(0, edge+1):
            if y-i < 0 or y+i+1 >= len(pattern):
                break
            for x in range(0, len(pattern[y])):
                if pattern[y-i][x] != pattern[y+i+1][x]:
                    if allow_discrepancy and discrepancy < 0:
                        discrepancy = x
                    elif not allow_discrepancy or x != discrepancy:
                        is_mirror = False
                        break
            if not is_mirror: break
        if is_mirror:
            mirror_index = y
            mirror_contents = pattern[y]
            break
    if mirror_index is not None:
        return 'y', mirror_index+1, mirror_contents
    
    for x in range(0, len(pattern[0])-1):
        if mirror_axis_0 == 'x' and mirror_index_0-1 == x:
            continue
        is_mirror = True
        edge = min(x, len(pattern[0])-x)
        discrepancy = -1

        for i in range(0, edge+1):
            if x-i < 0 or x+i+1 >= len(pattern[0]):
                break
            for y in range(0, len(pattern)):
                if pattern[y][x-i] != pattern[y][x+i+1]:
                    if allow_discrepancy and discrepancy < 0:
                        discrepancy = y
                    elif not allow_discrepancy or y != discrepancy:
                        is_mirror = False
                        break
            if not is_mirror: break
        if is_mirror:
            mirror_index = x
            mirror_contents = ''.join([pattern[y][x] for y in range(0, len(pattern))])
            break
    if mirror_index is not None:
        return 'x', mirror_index+1, mirror_contents
    
    return None, None, None

class Pattern:
    def __init__(self, pattern) -> None:
        self.map = pattern
        self.axis, self.index, self.mirror = find_mirror(self.map)
        self.axis2, self.index2, self.mirror2 = find_mirror(self.map, self.axis, self.index, self.mirror)
    
    def value(self):
        return self.index*100 if self.axis == 'y' else self.index if self.axis == 'x' else 0
    
    def value2(self):
        return self.index2*100 if self.axis2 == 'y' else self.index2 if self.axis2 == 'x' else 0
    
    def __repr__(self) -> str:
        return '\nPT1: {a}={i} ({v}): {m}\nPT2: {a2}={i2} ({v2}): {m2}'.format(
            a=self.axis, 
            i=self.index, 
            v=self.value(), 
            m=self.mirror,
            a2=self.axis2, 
            i2=self.index2, 
            v2=self.value2(), 
            m2=self.mirror2,
        )

def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    pattern = []
    for line in file:
        if not line.rstrip():
            data.append(Pattern(pattern))
            pattern = []
        else:
            sline = line.rstrip()
            pattern.append(sline)
    
    data.append(Pattern(pattern))
        
    file.close()
    if debug: print(data)
    return data

def print_pattern(pattern: Pattern):
    print(pattern)
    for row in pattern.map:
        print(row)
    print()

def part1(patterns):
    return sum(pattern.value() for pattern in patterns)

def part2(patterns):
    return sum(pattern.value2() for pattern in patterns)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day13.txt'
    
    patterns = read_data(file_path, debug)
    if debug:
        for pattern in patterns:
            print_pattern(pattern)

    print(part1(patterns)) # 35521
    print(part2(patterns)) # 34795

run_program(False)