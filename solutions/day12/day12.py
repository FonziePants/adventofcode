# --- Day 12: Rain Risk ---

class Directions:
    EAST = "E"
    WEST = "W"
    NORTH = "N"
    SOUTH = "S"
    ALL = [EAST, NORTH, WEST, SOUTH]
    
def calculate_change(dir,val):        
    return calculate_complex_change(dir,(0,val))

def calculate_complex_change(dir,waypoint):
    x_delta = 0
    y_delta = 0
    waypt_x = waypoint[0]
    waypt_y = waypoint[1]

    if dir == Directions.EAST:
        x_delta += waypt_y
        y_delta -= waypt_x
    elif dir == Directions.WEST:
        x_delta -= waypt_y
        y_delta += waypt_x
    elif dir == Directions.NORTH:
        x_delta += waypt_x
        y_delta += waypt_y
    elif dir == Directions.SOUTH:
        x_delta -= waypt_x
        y_delta -= waypt_y

    return (x_delta,y_delta)

class Commands:
    LEFT = "L"      # turn left (degrees)
    RIGHT = "R"     # turn right (degrees)
    FORWARD = "F"   # move forward (distance units)

def convert_direction(ref_dir, target_dir):
    idx_change = (Directions.ALL.index(ref_dir) + 3)
    idx_adjusted = (Directions.ALL.index(target_dir) - idx_change) % len(Directions.ALL)
    return Directions.ALL[idx_adjusted]


def calculate_new_direction(starting_direction, command, degrees):
    if command == Commands.FORWARD:
        return starting_direction

    dir_idx = Directions.ALL.index(starting_direction)
    idx_change = int(degrees / 90)

    if command == Commands.RIGHT:
        idx_change *= -1
    
    dir_idx += idx_change
    dir_idx %= len(Directions.ALL)

    return Directions.ALL[dir_idx]

def read_nav_instructions(file_path,debug=True):
    file = open(file_path, "r")

    nav_instructions = []

    for line in file:
        if not line.rstrip():
            continue
        direction = line[0]
        amount = int(line.rstrip()[1:])
        nav_instructions.append((direction,amount))
    
    file.close()
    
    if debug:
        print(nav_instructions)

    return nav_instructions

def navigate(nav_instructions,start_dir,start_coord,waypt_offset=None,debug=False):
    curr_dir = start_dir
    curr_coord = start_coord
    curr_waypt = None

    if waypt_offset:
        curr_waypt = (curr_coord[0] + waypt_offset[0],curr_coord[1] + waypt_offset[1])

    for nav_instr in nav_instructions:
        if debug:
            if curr_waypt:
                print("Wypt at ({0},{1}) facing {2}".format(curr_waypt[0],curr_waypt[1],curr_dir))
                print("Ship at ({0},{1})".format(curr_coord[0],curr_coord[1]))
            else:
                print("At ({0},{1}) facing {2}".format(curr_coord[0],curr_coord[1],curr_dir))
            print("\nCommand: {0} {1}".format(nav_instr[0],nav_instr[1]))

        action = nav_instr[0]
        value = nav_instr[1]

        if action == Commands.FORWARD:
            if curr_waypt:
                delta = calculate_complex_change(curr_dir, curr_waypt)
                curr_coord = (curr_coord[0] + (value*delta[0]),curr_coord[1] + (value*delta[1]))
                continue

            action = curr_dir

        if action in Directions.ALL:
            if curr_waypt:
                delta = calculate_change(convert_direction(curr_dir,action), value)
                curr_waypt = (curr_waypt[0] + delta[0],curr_waypt[1] + delta[1])
            else:
                delta = calculate_change(action, value)
                curr_coord = (curr_coord[0] + delta[0],curr_coord[1] + delta[1])
        else:
            curr_dir = calculate_new_direction(curr_dir, action, value)
        
    if debug:
            if curr_waypt:
                print("Wypt at ({0},{1}) facing {2}".format(curr_waypt[0],curr_waypt[1],curr_dir))
                print("Ship at ({0},{1})".format(curr_coord[0],curr_coord[1]))
            else:
                print("At ({0},{1}) facing {2}".format(curr_coord[0],curr_coord[1],curr_dir))
    
    return curr_coord

def calculate_part1(nav_instructions,debug=False):
    start_coord = (0,0)
    final_coord = navigate(nav_instructions, Directions.EAST, start_coord, None, debug)

    delta_x = start_coord[0] - final_coord[0]
    delta_y = start_coord[1] - final_coord[1]

    if delta_x < 0:
        delta_x *= -1
    if delta_y < 0:
        delta_y *= -1
    
    manhattan_dist = delta_x + delta_y
    print("Part 1: {0}\n\n".format(manhattan_dist))
    return manhattan_dist

def calculate_part2(nav_instructions,debug=False):
    start_coord = (0,0)
    waypt_offset = (10,1)
    final_coord = navigate(nav_instructions, Directions.NORTH, start_coord, waypt_offset, debug)

    delta_x = start_coord[0] - final_coord[0]
    delta_y = start_coord[1] - final_coord[1]

    if delta_x < 0:
        delta_x *= -1
    if delta_y < 0:
        delta_y *= -1
        
    manhattan_dist = delta_x + delta_y
    print("Part 2: {0}\n\n".format(manhattan_dist))
    return manhattan_dist

def run_program(test=False, debug=False):
    file_path = "solutions\day12\day12.txt"
    if test:
        file_path = "solutions\day12\day12_test.txt"
    
    data = read_nav_instructions(file_path, debug)
    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, True)
run_program()