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

class Coord:
    def __init__(self, input) -> None:
        parts = input.split(',')
        self.x = int(parts[0])
        self.y = int(parts[1])
    
    def __repr__(self) -> str:
        return '{0},{1}'.format(self.x, self.y)

class Line:
    def __init__(self, input) -> None:
        parts = input.split(' -> ')
        self.start = Coord(parts[0])
        self.end = Coord(parts[1])
    
    def x_match(self):
        return self.start.x if self.start.x == self.end.x else None
    
    def y_match(self):
        return self.start.y if self.start.y == self.end.y else None
    
    def x_range(self):
        incr = -1 if self.start.x > self.end.x else 1
        return range(self.start.x, self.end.x+incr,incr)
    
    def y_range(self):
        incr = -1 if self.start.y > self.end.y else 1
        return range(self.start.y, self.end.y+incr,incr)

    def __repr__(self) -> str:
        return '{0} → {1}'.format(self.start, self.end)

def pretty_print(map):
    print()
    for row in map:
        print(''.join([str(val) for val in row]))
    print()

def format_data(data):
    lines = []
    for row in data:
        lines.append(Line(row))
    return lines

def get_map(lines):
    max_x = max(max(line.start.x, line.end.x) for line in lines)
    max_y = max(max(line.start.y, line.end.y) for line in lines)
    map = []
    for i in range(0, max_y+1):
        map.append([0]*(max_x+1))
    return map

def part1(lines, debug):
    map = get_map(lines)

    for line in lines:
        if line.x_match():
            for y in line.y_range():
                map[y][line.x_match()] += 1
        elif line.y_match():
            for x in line.x_range():
                map[line.y_match()][x] += 1

    if debug:
        pretty_print(map)
    
    count = 0
    for row in map:
        for cell in row:
            if cell >= 2:
                count += 1
    return count

def part2(lines, debug):
    map = get_map(lines)

    for line in lines:
        if line.x_match():
            for y in line.y_range():
                map[y][line.x_match()] += 1
        elif line.y_match():
            for x in line.x_range():
                map[line.y_match()][x] += 1
        else:
            y = line.start.y
            for x in line.x_range():
                map[y][x] += 1
                y += 1 if line.start.y < line.end.y else -1

    if debug:
        pretty_print(map)
    
    count = 0
    for row in map:
        for cell in row:
            if cell >= 2:
                count += 1
    return count

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day05.txt'
    
    data = read_data(file_path, debug)
    lines = format_data(data)

    if debug:
        print(lines)

    print(part1(lines, debug)) # 5373
    print(part2(lines, debug)) # 21514

run_program(False)