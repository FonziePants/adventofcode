from copy import deepcopy
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

class XY:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return '{x},{y}'.format(x=self.x,y=self.y)

def format_data(data):
    map_size = XY(len(data[0]),len(data))
    cube_rocks = {y: {
        x: False for x in range(0, map_size.x)
    } for y in range(0, map_size.y)}
    round_rocks = []
    for y in range(0, map_size.y):
        for x in range(0, map_size.x):
            if data[y][x] == 'O':
                round_rocks.append(XY(x, y))
            elif data[y][x] == '#':
                cube_rocks[y][x] = True
    return map_size, cube_rocks, round_rocks

def print_map(map_size, cube_rocks, round_rocks):
    map = [['.' for x in range(0,map_size.x)] for y in range(0,map_size.y)]
    for rr in round_rocks:
        map[rr.y][rr.x] = 'O'
    for y in range(0, map_size.y):
        for x in range(0, map_size.x):
            if cube_rocks[y][x]: map[y][x] = '#'
    for row in map:
        print(''.join(row))

def calc_load(map_size, round_rocks):
    load = 0
    for rr in round_rocks:
        load += map_size.y - rr.y
    return load

def tilt_latitudinally(cube_rocks, round_rocks, north):
    new_round_rocks = []
    new_cube_rocks = deepcopy(cube_rocks)
    for rr in round_rocks:
        new_y = rr.y
        y_range = range(rr.y-1,-1,-1) if north else range(0,rr.y,1)
        for y in y_range:
            if new_cube_rocks[y][rr.x]: break
            new_y = y
        new_rr = XY(rr.x,new_y)
        new_round_rocks.append(new_rr)
        new_cube_rocks[new_rr.y][new_rr.x] = True
    return new_round_rocks

def tilt_longitudinally(cube_rocks, round_rocks, east):
    new_round_rocks = []
    new_cube_rocks = deepcopy(cube_rocks)
    for rr in round_rocks:
        new_x = rr.x
        x_range = range(rr.x-1,-1,-1) if east else range(0,rr.x,1)
        for x in x_range:
            if new_cube_rocks[x][rr.x]: break
            new_x = x
        new_rr = XY(new_x,rr.y)
        new_round_rocks.append(new_rr)
        new_cube_rocks[new_rr.y][new_rr.x] = True
    return new_round_rocks

def part1(map_size, cube_rocks, round_rocks):
    new_round_rocks = tilt_latitudinally(cube_rocks, round_rocks, True)
    return calc_load(map_size, new_round_rocks)

def part2(map_size, cube_rocks, round_rocks):
    new_round_rocks = deepcopy(round_rocks)
    for i in range(0, 1000000000):
        print('Round {0}'.format(i))
        new_round_rocks = tilt_latitudinally(cube_rocks, new_round_rocks, True)
        new_round_rocks = tilt_longitudinally(cube_rocks, new_round_rocks, False)
        new_round_rocks = tilt_latitudinally(cube_rocks, new_round_rocks, False)
        new_round_rocks = tilt_longitudinally(cube_rocks, new_round_rocks, True)
    return calc_load(map_size, new_round_rocks)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day14.txt'
    
    data = read_data(file_path, debug)
    map_size, cube_rocks, round_rocks = format_data(data)

    if debug:
        print_map(map_size, cube_rocks, round_rocks)

    print(part1(map_size, cube_rocks, round_rocks)) # 106186
    print(part2(map_size, cube_rocks, round_rocks)) # TBD

run_program(True)