class Constants:
    inactive = "."
    active = "#"

def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        row = []
        for cube in line.rstrip():
            if cube == Constants.inactive:
                row.append(False)
            else:
                row.append(True)
        data.append(row)
    
    file.close()

    data = [data]

    if debug:
        print_3d(data)

    return data

def print_3d(data):
    z_idx = 0
    for zslice in data:
        print("Z-INDEX {0}:".format(z_idx))
        for row in zslice:
            for col in row:
                char = Constants.active if col else Constants.inactive
                print(char + " ",end="")
            print()
        z_idx += 1
    print()

def count_active(data):
    count = 0
    for z in range(len(data)):
        for y in range(len(data[z])):
            for x in range(len(data[z][y])):
                count += 1 if data[z][y][x] else 0
    return count

def count_active_neighbors(data, z, y, x,debug=False):
    active_neighbors = 0
    z_lower = -1 if z > 0 else 0
    z_upper = 1 if z < len(data)-1 else 0
    y_lower = -1 if y > 0 else 0
    y_upper = 1 if y < len(data[z])-1 else 0
    x_lower = -1 if x > 0 else 0
    x_upper = 1 if x < len(data[z][y])-1 else 0

    for z_delta in range(z_lower,z_upper+1):
        for y_delta in range(y_lower, y_upper+1):
            for x_delta in range(x_lower,x_upper+1):
                x2 = x + x_delta
                y2 = y + y_delta
                z2 = z + z_delta
                if (x == x2 and y == y2 and z == z2):
                    continue
                if data[z2][y2][x2]:
                    active_neighbors += 1
                    if debug:
                        print("True for (x={0},y={1},z={2})".format(active_neighbors,x2,y2,z2))
    if debug:
        print("{0} neighbors for (x={1},y={2},z={3})".format(active_neighbors,x,y,z))
    return active_neighbors

def expand_space(curr_data):
    next_data = []
    for i in range(len(curr_data)+2):
        next_data_zslice = []
        for j in range(len(curr_data[0])+2):
            next_data_row = [False for k in range(len(curr_data[0][0])+2)]
            next_data_zslice.append(next_data_row)
        next_data.append(next_data_zslice)

    # overwrite middle ones with curr_data
    for z in range(len(curr_data)):
        for y in range(len(curr_data[z])):
            for x in range(len(curr_data[z][y])):
                next_data[z+1][y+1][x+1] = curr_data[z][y][x]

    return next_data

def execute_cycle(curr_data,debug):
    old_data = expand_space(curr_data)
    new_data = expand_space(curr_data)

    for z in range(len(old_data)):
        for y in range(len(old_data[z])):
            for x in range(len(old_data[z][y])):
                cube = old_data[z][y][x]
                active_neighbors = count_active_neighbors(old_data, z, y, x)
                if ((cube and 
                    (active_neighbors < 2 or 
                    active_neighbors > 3)) 
                    or 
                    (not cube and 
                    active_neighbors == 3)):
                    new_data[z][y][x] = not cube

    if debug:
        print("OLD DATA:")
        print_3d(old_data)
        print("\nNEW DATA:")
        print_3d(new_data)
    
    return new_data

def calculate_part1(data,debug=False):
    for i in range(6):  
        print("CYCLE {0}".format(i)) 
        data = execute_cycle(data,debug)
    count = count_active(data)
    print("Part 1: {0} active cubes\n\n".format(count))
    return

def calculate_part2(data,debug=False):

    print("Part 2: {0}\n\n".format("TODO"))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day17\day17.txt"
    if test:
        file_path = "solutions\day17\day17_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()