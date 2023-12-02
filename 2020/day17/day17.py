class Constants:
    inactive = "."
    active = "#"

def read_data(file_path,part2,debug=True):
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

    if part2:
        data = [data]
        if debug:
            print_4d(data)
    elif debug:
        print_3d(data)

    return data

def print_4d(data,part2=False):
    w_idx = 0
    for wslice in data:
        z_idx = 0
        for zslice in wslice:
            print("Z-INDEX {0}, W-INDEX {1}:".format(z_idx,w_idx))
            for row in zslice:
                for col in row:
                    char = Constants.active if col else Constants.inactive
                    print(char + " ",end="")
                print()
            z_idx += 1
        w_idx += 1
    print()

def print_3d(data,part2=False):
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

def count_active(data,part2=False):
    if part2:
        return count_active_4d(data)
    count = 0
    for z in range(len(data)):
        for y in range(len(data[z])):
            for x in range(len(data[z][y])):
                count += 1 if data[z][y][x] else 0
    return count

def count_active_4d(data,part2=False):
    count = 0
    for w in range(len(data)):
        for z in range(len(data[w])):
            for y in range(len(data[w][z])):
                for x in range(len(data[w][z][y])):
                    count += 1 if data[w][z][y][x] else 0
    return count

def count_active_neighbors_4d(data, w, z, y, x):
    active_neighbors = 0
    w_lower = -1 if w > 0 else 0
    w_upper = 1 if w < len(data)-1 else 0
    z_lower = -1 if z > 0 else 0
    z_upper = 1 if z < len(data[w])-1 else 0
    y_lower = -1 if y > 0 else 0
    y_upper = 1 if y < len(data[w][z])-1 else 0
    x_lower = -1 if x > 0 else 0
    x_upper = 1 if x < len(data[w][z][y])-1 else 0

    for w_delta in range(w_lower,w_upper+1):
        for z_delta in range(z_lower,z_upper+1):
            for y_delta in range(y_lower, y_upper+1):
                for x_delta in range(x_lower,x_upper+1):
                    x2 = x + x_delta
                    y2 = y + y_delta
                    z2 = z + z_delta
                    w2 = w + w_delta
                    if (w == w2 and x == x2 and y == y2 and z == z2):
                        continue
                    if data[w2][z2][y2][x2]:
                        active_neighbors += 1
                       
    return active_neighbors

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

    return active_neighbors

def expand_space_2(curr_data):
    next_data = []
    for i in range(len(curr_data)+2):
        next_data_wslice = []
        for j in range(len(curr_data[0])+2):
            next_data_zslice = []
            for k in range(len(curr_data[0][0])+2):
                next_data_row = [False for l in range(len(curr_data[0][0][0])+2)]
                next_data_zslice.append(next_data_row)
            next_data_wslice.append(next_data_zslice)
        next_data.append(next_data_wslice)

    # overwrite middle ones with curr_data
    for w in range(len(curr_data)):
        for z in range(len(curr_data[w])):
            for y in range(len(curr_data[w][z])):
                for x in range(len(curr_data[w][z][y])):
                    next_data[w+1][z+1][y+1][x+1] = curr_data[w][z][y][x]

    return next_data

def expand_space(curr_data,part2=False):
    if part2:
        return expand_space_2(curr_data)

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

def execute_cycle(curr_data,part2=False,debug=False):
    old_data = expand_space(curr_data,part2)
    new_data = expand_space(curr_data,part2)

    if part2:
        for w in range(len(old_data)):
            for z in range(len(old_data[w])):
                for y in range(len(old_data[w][z])):
                    for x in range(len(old_data[w][z][y])):
                        cube = old_data[w][z][y][x]
                        active_neighbors = count_active_neighbors_4d(old_data, w, z, y, x)
                        if ((cube and 
                            (active_neighbors < 2 or 
                            active_neighbors > 3)) 
                            or 
                            (not cube and 
                            active_neighbors == 3)):
                            new_data[w][z][y][x] = not cube
    else:
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
        if part2:
            print_4d(old_data)
        else:
            print_3d(old_data)
        print("\nNEW DATA:")
        if part2:
            print_4d(new_data)
        else:
            print_3d(new_data)
    
    return new_data

def calculate(data,part2=False,debug=False):
    for i in range(6):  
        print("CYCLE {0}".format(i)) 
        data = execute_cycle(data,part2,debug)
    count = count_active(data,part2)
    part = "2" if part2 else "1"
    print("Part {0}: {1} active cubes\n\n".format(part,count))
    return

def run_program(test=False, debug=False):
    file_path = "day17.txt"
    if test:
        file_path = "day17_test.txt"
    
    data = read_data(file_path, False, debug)
    calculate(data, False, debug)

    data = read_data(file_path, True, debug)
    calculate(data, True, debug)

# run_program(True, False)
run_program()