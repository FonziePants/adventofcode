class Tile:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        
        self.edges = [data[0]]
        left_edge = []
        right_edge = []
        for i in range(len(data)):
            left_edge.append(data[i][0])
            right_edge.append(data[i][len(data)-1])
        self.edges.append("".join(right_edge))
        self.edges.append(data[len(data)-1])
        self.edges.append("".join(left_edge))

        self.matches = [None, None, None, None]
    
    def get_exposed_edge_count(self):
        exposed_edge_count = 4
        for match in self.matches:
            if match:
                exposed_edge_count -= 1
        return exposed_edge_count
    
    def print(self):
        print("TILE {0}".format(self.id))
        for row in self.data:
            print(row)
        print()

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
                        tile1.matches[e1] = t2
                        tile2.matches[e2] = t1
                    elif (tile1.edges[e1] == tile2.edges[e2][::-1]):
                        tile1.matches[e1] = -t2
                        tile2.matches[e2] = -t1
    
    corners = []
    corners_product = 1
    for t in tiles:
        edge_count = tiles[t].get_exposed_edge_count()
        if debug:
            print("Tile {0} has {1} open edges: {2}".format(t,edge_count,tiles[t].matches))
        if edge_count == 2:
            corners.append(tiles[t])
            corners_product *= t
    
    print("Part 1: {0}\n\n".format(corners_product))
    return

def calculate_part2(data,debug=False):

    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day20\day20.txt"
    if test:
        file_path = "solutions\day20\day20_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()