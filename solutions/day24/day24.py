ALL_DIRECTIONS = ["e", "ne", "nw", "w", "sw", "se"]

def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        data.append(line.replace("e","e ").replace("w","w ").rstrip().split(" "))
    
    file.close()

    if debug:
        print(data)

    return data

def get_opposite_direction(dir):
    idx = ALL_DIRECTIONS.index(dir)
    return ALL_DIRECTIONS[(idx + 3)%6]

def get_coordinates(dir):
    x=0
    y=0

    if "e" in dir:
        x += 1
    elif "w" in dir:
        x -= 1
    
    if len(dir) == 1:
        x *= 2
    
    if "n" in dir:
        y += 1
    elif "s" in dir:
        y -= 1
    
    return (x,y)

def get_id(x,y):
    return "{0},{1}".format(x,y)

def get_x_y(id):
    x = int(id.split(",")[0])
    y = int(id.split(",")[1])
    return (x,y)

def get_adjacent_ids(id):
    neighbors = []

    coord = get_x_y(id)
    for dir in ALL_DIRECTIONS:
        delta = get_coordinates(dir)
        neighbors.append(get_id(coord[0]+delta[0],coord[1]+delta[1]))

    return neighbors

def get_bounds(tiles):
    upper_bound = 0
    lower_bound = 0
    left_bound = 0
    right_bound = 0

    map = []

    for t_id in tiles:
        coord = get_x_y(t_id)
        if coord[0] < left_bound:
            left_bound = coord[0]
        if coord[0] > right_bound:
            right_bound = coord[0]
        if coord[1] < lower_bound:
            lower_bound = coord[1]
        if coord[1] > upper_bound:
            upper_bound = coord[1]
    
    return (range(left_bound-2,right_bound+2),range(lower_bound-2,upper_bound+2))

def print_tiles(tiles):
    bounds = get_bounds(tiles)
    map = []
    
    for y in list(reversed(bounds[1])):
        row = " "
        for x in bounds[0]:
            id = get_id(x,y)
            if (x+y)%2 == 1:
                row += "  "
            elif id in tiles:
                if tiles[id].white_side_up:
                    row += "o "
                else:
                    row += "# "
            else:
                row += "_ "
        map.append(row)
    
    for row in map:
        print(row)
    
    return  

class HexTile:
    def __init__(self,x,y):
        self.id = get_id(x,y)
        self.location = (x,y)
        self.white_side_up = True
    
    def flip(self):
        self.white_side_up = not self.white_side_up
    
    def print(self):
        print("TILE AT ({0}): {1}".format(self.id,"WHITE" if self.white_side_up else "BLACK"))

def count_black_tiles(tiles):
    black_count = 0
    for t_id in tiles:
        if not tiles[t_id].white_side_up:
            black_count += 1
    return black_count

def calculate_part1(data,tiles,debug=False):  
    for instruction in data:
        x = 0
        y = 0
        for dir in instruction:
            delta = get_coordinates(dir)
            x += delta[0]
            y += delta[1]

        id = get_id(x,y)
        if id not in tiles:
            tiles[id] = HexTile(x,y)
        tiles[id].flip()
        
        if debug:
            print(instruction)
            tiles[id].print()
            print()
    
    if debug:
        for t_id in tiles:
            tiles[t_id].print()

    black_count = count_black_tiles(tiles)

    print("Part 1: {0}\n\n".format(black_count))
    return

def calculate_part2(data,tiles,debug=False):
    black_count = count_black_tiles(tiles)
    for day in range(0,100):
        tiles_to_flip = []
        bounds = get_bounds(tiles)
        for x in bounds[0]:
            for y in bounds[1]:
                if (x+y)%2 != 0:
                    continue
                t_id = get_id(x,y)
                neighbors = get_adjacent_ids(t_id)
                bnc = 0
                for n_id in neighbors:
                    if n_id not in tiles:
                        n_xy = get_x_y(n_id)
                    elif not tiles[n_id].white_side_up:
                        bnc += 1
                if t_id not in tiles:
                    tiles[t_id] = HexTile(x,y)
                tile = tiles[t_id]
                if (    (tile.white_side_up     and bnc == 2)
                    or  (not tile.white_side_up and bnc == 0)
                    or  (not tile.white_side_up and bnc > 2)):
                    tiles_to_flip.append(t_id)
        for t_id in tiles_to_flip:
            tiles[t_id].flip()
        black_count = count_black_tiles(tiles)
        if debug:
            print("Day {0}: {1}".format(day+1,black_count))

    print("Part 2: {0}\n\n".format(black_count))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day24\day24.txt"
    if test:
        file_path = "solutions\day24\day24_test.txt"
    
    data = read_data(file_path, debug)
    tiles = {}

    calculate_part1(data, tiles, debug)
    calculate_part2(data, tiles, debug)

# run_program(True, True)
run_program()