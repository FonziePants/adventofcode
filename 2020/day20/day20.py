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

def read_sea_monster():
    file = open("seamonster.txt", "r")

    monster = []

    for line in file:
        if not line.rstrip():
            continue
        monster.append(line[:-1])
    
    file.close()

    return monster

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

        self.top_index = -1
        self.flip_h = False
        self.flip_v = False
    
    def get_right_neighbor(self):
        if self.top_index < 0:
            return None
        
        index = self.top_index + 3 if self.flip_h else self.top_index + 1
        return self.matches[index%4]
    
    def get_bottom_neighbor(self):
        if self.top_index < 0:
            return None
        
        index = self.top_index if self.flip_v else self.top_index + 2
        return self.matches[index%4]

    def get_top_neighbor(self):
        if self.top_index < 0:
            return None
        
        index = self.top_index + 2 if self.flip_v else self.top_index
        return self.matches[index%4]
    
    def get_modified_data(self):
        modified_data = self.data.copy()

        rotate = (4 - self.top_index) % 4

        flip_h = self.flip_h
        flip_v = self.flip_v

        for i in range(rotate):
            modified_data = rotate_map(modified_data)

        if flip_h:
            for r in range(len(modified_data)):
                modified_data[r] = modified_data[r][::-1]
        
        if flip_v:
            modified_data = flip_map(modified_data)
        
        print_2d(self.id,modified_data)
        
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

def rotate_map(map):
    new_map = []
    for c in range(0,len(map[0])):
        row = ""
        for r in reversed(range(0,len(map))):
            row += map[r][c]
        new_map.append(row)

    return new_map

def flip_map(map):
    return list(reversed(map))

def assemble_map(tiles, starting_corner,debug):
    map = []
    unused_tile_ids = list(tiles.keys())
    used_tile_ids = []
    first_tile_in_row = starting_corner
    current_tile = starting_corner

    # get starting tile's orientation
    for i in range(4):
        if not current_tile.matches[i] and not current_tile.matches[(i+3)%4]:
            current_tile.top_index = i
            current_tile.flip = False
            break

    row_section = current_tile.get_modified_data()
    unused_tile_ids.remove(current_tile.id)
    used_tile_ids.append(current_tile.id)
    if debug:
            print("Adding tile {0}\n\ttop:   {1}\n\tflip h: {2}\n\tflip v: {3}\n\tmatches: {4}\n".format(current_tile.id, current_tile.top_index, current_tile.flip_h, current_tile.flip_v, current_tile.matches))

    while len(unused_tile_ids) > 0:
        new_row = False
        flip_h = current_tile.flip_h
        flip_v = current_tile.flip_v
        match_info = current_tile.get_right_neighbor()
        if (not match_info):
            # add the row section
            for row in row_section:
                map.append(row)
            row_section = []
            flip_h = first_tile_in_row.flip_h
            flip_v = first_tile_in_row.flip_v
            # get the tile below the first tile in the row
            new_row = True
            match_info = first_tile_in_row.get_bottom_neighbor()

        previous_tile = current_tile
        current_tile = tiles[match_info[0]]

        if new_row:
            top_index = match_info[1]
            if match_info[2]:
                flip_h = not flip_h
            current_tile.flip_h = flip_h
            current_tile.top_index = (top_index)%4
        else:
            left_index = match_info[1]
            if (match_info[2] and not previous_tile.flip_h) or (not match_info[2] and previous_tile.flip_h):
                flip_v = not flip_v
            current_tile.flip_v = flip_v
            current_tile.top_index = (left_index + 1)%4

        if debug:
            print("Adding tile {0}\n\ttop:   {1}\n\tflip h: {2}\n\tflip v: {3}\n\tmatches: {4}\n\tlogic:   {5}\n".format(current_tile.id, current_tile.top_index, current_tile.flip_h, current_tile.flip_v, current_tile.matches, match_info))

        tile_data = current_tile.get_modified_data()

        if new_row:
            row_section = tile_data
            first_tile_in_row = current_tile
        else:
            for r in range(len(row_section)):
                row_section[r] += tile_data[r]

        unused_tile_ids.remove(current_tile.id)
        used_tile_ids.append(current_tile.id)
    
    for row in row_section:
        map.append(row)
    
    if debug:
        print(used_tile_ids)
        print("MAP")
        for row in map:
            print(row)

    return map

def match_monster(map,monster):
    monster_count = 0
    for map_row in range(0,len(map)-len(monster)):
        for map_col in range(0,len(map[0])-len(monster[0])):
            new_map = map.copy()
            found_monster = True
            for monster_row in range(0,len(monster)):
                for monster_col in range(0,len(monster[0])):
                    if monster[monster_row][monster_col] != "#":
                        continue
                    elif map[map_row+monster_row][map_col+monster_col] != "#":
                        found_monster = False
                        break
                    row = map_row+monster_row
                    col = map_col+monster_col
                    map_string = new_map[row]
                    new_map[row] = map_string[0:col] + "🐉" + map_string[col+1:]
                if not found_monster:
                    break
            if found_monster:
                map = new_map
                monster_count += 1
    return (map,monster_count)

def calculate_part1(tiles,debug=False): 
    for t1 in tiles:
        for t2 in tiles:
            if t1 == t2:
                continue
            tile1 = tiles[t1]
            tile2 = tiles[t2]

            for e1 in range(len(tile1.edges)):
                for e2 in range(len(tile2.edges)):
                    if (tile1.edges[e1] == tile2.edges[e2][::-1]):
                        tile1.matches[e1] = (t2,e2,False)
                        tile2.matches[e2] = (t1,e1,False)
                    elif (tile1.edges[e1] == tile2.edges[e2]):
                        tile1.matches[e1] = (t2,e2,True)
                        tile2.matches[e2] = (t1,e1,True)  
    
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
    map = assemble_map(tiles, data[1], debug)
    monster = read_sea_monster()
    monster_count = 0

    for j in range(0,2):
        for i in range(0,4):
            round = match_monster(map,monster)
            map = round[0]
            monster_count += round[1]
            if debug:
                print_2d("MAP {0}".format((i+1)+(4*j)),map)
            map = rotate_map(map)
        map = flip_map(map)

    if debug:
        print("{0} monsters!! 🐉".format(monster_count))
    
    water_count = 0
    for row in map:
        water_count += row.count("#")

    print("Part 2: {0}\n\n".format(water_count))
    return 

def run_program(test=False, debug=False):
    file_path = "day20.txt"
    if test:
        file_path = "day20_test.txt"
    
    data = read_data(file_path, debug)

    data2 = calculate_part1(data, debug)
    calculate_part2(data2, debug)

# run_program(True, True)
run_program(False,True)