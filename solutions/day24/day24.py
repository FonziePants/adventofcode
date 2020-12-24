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
    directions = ["e", "ne", "nw", "w", "sw", "se"]
    idx = directions.index(dir)
    return directions[(idx + 3)%6]

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

class HexTile:
    def __init__(self,x,y):
        self.id = get_id(x,y)
        self.location = (x,y)
        self.white_side_up = True
    
    def flip(self):
        self.white_side_up = not self.white_side_up
    
    def print(self):
        print("TILE AT ({0}): {1}".format(self.id,"WHITE" if self.white_side_up else "BLACK"))


def calculate_part1(data,debug=False):  
    tiles = {}
    starting_tile = HexTile(0,0) 
    tile = starting_tile
    tiles[tile.id] = tile
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

    black_count = 0
    for t_id in tiles:
        if not tiles[t_id].white_side_up:
            black_count += 1

    print("Part 1: {0}\n\n".format(black_count))
    return

def calculate_part2(data,debug=False):

    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day24\day24.txt"
    if test:
        file_path = "solutions\day24\day24_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()