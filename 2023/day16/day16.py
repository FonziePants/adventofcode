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

class Coord:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return '{x},{y}'.format(x=self.x,y=self.y)

class Tile:
    def __init__(self, char) -> None:
        self.char = char
        self.energized = False
    
    def reflect(self, direction: Coord):
        self.energized = True#gcd vff <-- Ollie's first typing
        if direction.x != 0:
            if self.char in ['.','-']:
                return [direction]
            elif self.char == '|':
                return [Coord(0,1), Coord(0,-1)]
            elif self.char == '/':
                return [Coord(0,1)] if direction.x < 0 else [Coord(0,-1)]
            elif self.char == '\\':
                return [Coord(0,1)] if direction.x > 0 else [Coord(0,-1)]
        if direction.y != 0:
            if self.char in ['.','|']:
                return [direction]
            elif self.char == '-':
                return [Coord(1,0), Coord(-1,0)]
            elif self.char == '/':
                return [Coord(1,0)] if direction.y < 0 else [Coord(-1,0)]
            elif self.char == '\\':
                return [Coord(1,0)] if direction.y > 0 else [Coord(-1,0)]
        return []
        
    
    def map(self) -> str:
        return self.char
    
    def energy(self) -> str:
        return '#' if self.energized else '.'

class Beam:
    def __init__(self, coord, direction) -> None:
        self.coord = coord
        self.direction = direction
    
    def in_range(self, x, y):
        return (
            0 <= self.coord.x < x and
            0 <= self.coord.y < y
        )
    
    def __repr__(self) -> str:
        return '({c}) => {d}'.format(c=self.coord, d=self.direction)

def print_tiles(tiles, type='map'):
    for row in tiles:
        if type == 'energized':
            print(''.join([tile.energy() for tile in row]))
        else:
            print(''.join([tile.map() for tile in row]))
    print()

def format_data(data):
    tiles = []
    for row in data:
        tile_row = []
        for char in row:
            tile_row.append(Tile(char))
        tiles.append(tile_row)
    return tiles

def get_energized_count(tiles_0, startbeam, debug):
    tiles = deepcopy(tiles_0)
    x = len(tiles[0])
    y = len(tiles)
    beams = [startbeam]
    unique_steps = { str(beams[0]) }
    while (len(beams) > 0):
        new_beams = []
        added_unique_step = False
        for beam in beams:
            if beam.in_range(x, y):
                directions = tiles[beam.coord.y][beam.coord.x].reflect(beam.direction)
                for direction in directions:
                    new_beam = Beam(
                        Coord(beam.coord.x+direction.x,beam.coord.y+direction.y),
                        direction
                    )
                    if str(new_beam) not in unique_steps:
                        unique_steps.add(str(new_beam))
                        added_unique_step = True
                        new_beams.append(new_beam)
        if not added_unique_step: break
        beams = new_beams
    energized_count = 0
    for tile_row in tiles:
        for tile in tile_row:
            if tile.energized: energized_count += 1
    if debug: 
        print('{0} ENERGIZED {1}'.format(startbeam, energized_count))
        print_tiles(tiles, 'energized')
    return energized_count

def part1(tiles, debug):
    return get_energized_count(tiles, Beam(Coord(0,0), Coord(1,0)), debug)

def part2(tiles, debug):
    max_energized = 0
    for y in range(0, len(tiles)):
        rt_beam = Beam(Coord(0,y),Coord(1,0))
        lf_beam = Beam(Coord(len(tiles[0])-1,y),Coord(-1,0))
        max_energized = max(
            max_energized, 
            get_energized_count(tiles, rt_beam, debug),
            get_energized_count(tiles, lf_beam, debug)
        )
    for x in range(0, len(tiles[0])):
        dn_beam = Beam(Coord(x,0),Coord(0,1))
        up_beam = Beam(Coord(x,len(tiles)-1),Coord(0,-1))
        max_energized = max(
            max_energized, 
            get_energized_count(tiles, dn_beam, debug),
            get_energized_count(tiles, up_beam, debug)
        )
    return max_energized

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day16.txt'
    
    data = read_data(file_path, debug)
    tiles = format_data(data)

    if debug: print_tiles(tiles)

    print(part1(tiles, debug)) # 8116
    print(part2(tiles, debug)) # 8383

run_program(False)