from math import ceil

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

pipe_types = {
    'u': ['|','L','J'],
    'd': ['|','F','7'],
    'l': ['-','J','7'],
    'r': ['-','L','F'],
}

class Square:
    def __init__(self, x, y, value) -> None:
        self.value = value
        self.x = x
        self.y = y
        self.u = self.value in pipe_types['u']
        self.d = self.value in pipe_types['d']
        self.l = self.value in pipe_types['l']
        self.r = self.value in pipe_types['r']
        self.is_pipe = False
    
    def is_start(self): return self.value == 'S'

    def is_horizontal(self): return self.l or self.r

    def forward_step(self, last_dir=None):
        if self.u and last_dir != 'd': return (self.x, self.y-1, 'u')
        elif self.d and last_dir != 'u': return (self.x, self.y+1, 'd')
        elif self.l and last_dir != 'r': return (self.x-1, self.y, 'l')
        elif self.r and last_dir != 'l': return (self.x+1, self.y, 'r')
        else: return None
    
    def __repr__(self) -> str:
        return self.value
    
    def coord_string(self) -> str:
        return '{x},{y}'.format(x=self.x, y=self.y)
    
def get_pipe_from_neighbors(pipe, map):
    pipe.l = False if pipe.x == 0 else map[pipe.y][pipe.x-1].r
    pipe.r = False if pipe.x == len(map[0]) else map[pipe.y][pipe.x+1].l
    pipe.u = False if pipe.y == 0 else map[pipe.y-1][pipe.x].d
    pipe.d = False if pipe.x == len(map) else map[pipe.y+1][pipe.x].u

def print_map(map):
    for row in map:
        print(''.join([str(s) for s in row]))

def format_data(data):
    map = []
    start = None
    for y in range(0, len(data)):
        map_row = []
        for x in range(0, len(data[y])):
            square = Square(x, y, data[y][x])
            map_row.append(square)
            if square.is_start(): 
                start = square
                start.is_pipe = True
        map.append(map_row)
    
    get_pipe_from_neighbors(start, map)

    return map, start

def part1(map, start):
    x, y, last_dir = start.forward_step()
    current_step = map[y][x]
    current_step.is_pipe = True
    step_count = 1
    while current_step.value != 'S':
        x, y, last_dir = current_step.forward_step(last_dir)
        current_step = map[y][x]
        current_step.is_pipe = True
        step_count += 1
    return ceil(step_count/2)

def part2(map, start):
    # marking as in a pipe is handled in part1
    count = 0
    x = 0
    y = 0
    while y < len(map):
        in_loop = False
        x = 0
        while x < len(map[y]):
            if map[y][x].is_pipe: 
                if map[y][x].is_horizontal():
                    start = 'u' if map[y][x].u else 'd'
                    end = start
                    while (
                        map[y][x].is_pipe 
                        and map[y][x].r
                        and x < len(map[y])
                    ):
                        x += 1
                        end = 'u' if map[y][x].u else 'd'
                    x += 1
                    if start != end: in_loop = not in_loop
                else:
                    in_loop = not in_loop
                    x += 1
                continue
            elif in_loop: 
                count += 1
                map[y][x].value = 'I'
            else: map[y][x].value = 'O'
            x += 1
        y += 1
    return count

def run_program(debug=False):
    file_path = 'test3.txt' if debug else 'day10.txt'
    
    data = read_data(file_path, debug)
    map, start = format_data(data)

    if debug: print_map(map)
    if debug: print('start = {x},{y}'.format(x=start.x, y=start.y))

    print(part1(map, start)) # 6903
    print(part2(map, start)) # 265

    if debug: print_map(map)

run_program(False)