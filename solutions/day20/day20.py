def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = {}
    id = -1
    buffer = []
    for line in file:
        if not line.rstrip():
            continue
        if "Tile" in line:
            # make a tile of the previous tile data
            if len(buffer) > 0:
                tile = Tile(id, buffer)
                data[id] = tile
                # clear buffer
                buffer = []
            id = int(line.split(" ")[1].rstrip()[0:-1])
        else:
            buffer.append(line.rstrip())
    
    # make a tile of the previous tile data
    if len(buffer) > 0:
        tile = Tile(id, buffer)
        data[id] = tile
    
    file.close()

    if debug:
        for tile_id in data:
            data[tile_id].print()

    return data

class Tile:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        
        self.edges = [data[0]]
        left_edge = ""
        right_edge = ""
        for i in range(len(data)):
            left_edge += data[i][0]
            right_edge += data[i][len(data)-1]
        self.edges.append(right_edge)
        self.edges.append(data[len(data)-1][::-1])
        self.edges.append(left_edge[::-1])

        self.data = self.data[1:len(self.data)-1]
        for r in range(len(self.data)):
            self.data[r] = self.data[r][1:-1]

        self.matches = [None, None, None, None]
    
    def get_modified_data(self, rotate, flip):
        modified_data = self.data.copy()

        flip_h = (rotate >= 2)
        flip_v = (rotate >= 2)

        if flip:
            flip_h = not flip_h

        # swap axes if rotating 90 or 270 degrees
        if rotate % 2 == 1:
            modified_data = []
            for c in range(len(self.data[0])):
                row = ""
                for r in reversed(range(len(self.data))):
                    row += self.data[r][c]
                modified_data.append(row)

        if flip_h:
            for r in range(len(modified_data)):
                modified_data[r] = modified_data[r][::-1]
        
        if flip_v:
            modified_data = list(reversed(modified_data))
        
        return modified_data
    
    def get_exposed_edge_count(self):
        exposed_edge_count = 4
        for match in self.matches:
            if match:
                exposed_edge_count -= 1
        return exposed_edge_count
    
    def print(self):
        print_2d("TILE {0}".format(self.id),self.data)

def print_2d(title,data):
    print(title)
    for row in data:
        print(row)
    print()

def assemble_map(tiles, starting_corner,debug):
    map = []
    unused_tile_ids = list(tiles.keys())
    first_tile_in_row = starting_corner
    current_tile = starting_corner
    rotate = 0
    rotate_row = 0
    flip = False
    flip_row = False

    # get starting tile's orientation
    for i in range(4):
        if not current_tile.matches[i] and not current_tile.matches[(i+3)%4]:
            rotate = (i+2)%4
            rotate_row = rotate
            break

    row_section = current_tile.get_modified_data(rotate, flip)
    unused_tile_ids.remove(current_tile.id)
    if debug:
            print("Adding tile {0}\n\trotate: {1}\n\tflip: {2}".format(current_tile.id,rotate,flip))

    while len(unused_tile_ids) > 0:
        new_row = False
        target = current_tile
        match_info = current_tile.matches[(rotate+3)%4] 
        if (not match_info):
            # add the row section
            for row in row_section:
                map.append(row)
            row_section = []
            # get the tile below the first tile in the row
            new_row = True
            target = first_tile_in_row
            rotate = rotate_row
            flip = flip_row
            match_info = first_tile_in_row.matches[(rotate)%4] 

        current_tile = tiles[match_info[0]]
        rotate = (rotate + match_info[1]) % 4
        if match_info[2]:
            flip = not flip

        if debug:
            print("Rotate to determine match: {0}".format((rotate - match_info[1]+4)%4))
            print("Matches for {0}: {1}".format(target.id,target.matches))
            print("Adding tile {0}\n\trotate: {1}\n\tflip: {2}".format(current_tile.id,rotate,flip))

        tile_data = current_tile.get_modified_data(rotate, flip)

        if match_info[2] and match_info[1] % 2 == 0:
            rotate += 2
            rotate %= 4

        if new_row:
            row_section = tile_data
            first_tile_in_row = current_tile
            rotate_row = rotate
            flip_row = flip
        else:
            for r in range(len(row_section)):
                row_section[r] += tile_data[r]

        unused_tile_ids.remove(current_tile.id)
    
    for row in row_section:
        map.append(row)
    
    if debug:
        print("MAP")
        for row in map:
            print(row)

    return map

def calculate_part1(tiles,debug=False): 
    for t1 in tiles:
        for t2 in tiles:
            if t1 == t2:
                continue
            tile1 = tiles[t1]
            tile2 = tiles[t2]

            for e1 in range(len(tile1.edges)):
                for e2 in range(len(tile2.edges)):
                    if (tile1.edges[e1] == tile2.edges[e2]):
                        tile1.matches[e1] = (t2,(e1-e2+4)%4,False)
                        tile2.matches[e2] = (t1,(e1-e2+4)%4,False)
                        
                    elif (tile1.edges[e1] == tile2.edges[e2][::-1]):
                        tile1.matches[e1] = (t2,(e1-e2+4)%4,True)
                        tile2.matches[e2] = (t1,(e1-e2+4)%4,True)
    
    corners_product = 1
    starting_corner = None
    for t in tiles:
        edge_count = tiles[t].get_exposed_edge_count()
        if debug:
            print("Tile {0} has {1} open edges: {2}".format(t,edge_count,tiles[t].matches))
        if edge_count == 2:
            corners_product *= t
            starting_corner = tiles[t]
    
    print("Part 1: {0}\n\n".format(corners_product))

    return (tiles, starting_corner)

def calculate_part2(data,debug=False):
    tiles = data[0]
    map = assemble_map(tiles, tiles[1951],debug)
    # map = assemble_map(tiles, data[1],debug)
    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day20\day20.txt"
    if test:
        file_path = "solutions\day20\day20_test.txt"
    
    data = read_data(file_path, debug)

    data2 = calculate_part1(data, debug)
    calculate_part2(data2, debug)

run_program(True, True)
# run_program()