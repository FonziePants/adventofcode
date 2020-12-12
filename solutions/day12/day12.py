# --- Day 12: TODO ---

class Directions:
    EAST = "E"
    WEST = "W"
    NORTH = "N"
    SOUTH = "S"
    ALL = [EAST, NORTH, WEST, SOUTH]
    
    def calculate_change(dir,val):
        x_delta = 0
        y_delta = 0

        if dir == Directions.EAST:
            x_delta += val
        elif dir == Directions.WEST:
            x_delta -= val
        elif dir == Directions.NORTH:
            y_delta += val
        elif dir == Directions.SOUTH:
            y_delta -= val
        
        return (x_delta,y_delta)

class Commands:
    LEFT = "L"      # turn left (degrees)
    RIGHT = "R"     # turn right (degrees)
    FORWARD = "F"   # move forward (distance units)

def calculate_new_direction(starting_direction, command, degrees):
    if command == Commands.FORWARD:
        return starting_direction

    dir_idx = Directions.ALL.index(starting_direction)
    idx_change = int(degrees / 90)

    if command == Commands.RIGHT:
        idx_change *= -1
        
    # print("Direction {0} has index {1}".format(starting_direction,dir_idx))
    # print("{0} degrees {1} means an index change of {2}".format(degrees, command, idx_change))
    
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

def navigate(nav_instructions,start_dir,start_coord,debug=False):
    curr_dir = start_dir
    curr_coord = start_coord

    for nav_instr in nav_instructions:
        if debug:
            print("At ({0},{1}) facing {2}".format(curr_coord[0],curr_coord[1],curr_dir))

        action = nav_instr[0]
        value = nav_instr[1]

        if action == Commands.FORWARD:
            action = curr_dir

        if action in Directions.ALL:
            delta = Directions.calculate_change(action, value)
            curr_coord = (curr_coord[0] + delta[0],curr_coord[1] + delta[1])
        else:
            curr_dir = calculate_new_direction(curr_dir, action, value)
        
    if debug:
            print("At ({0},{1}) facing {2}".format(curr_coord[0],curr_coord[1],curr_dir))
    
    return curr_coord


def calculate_part1(nav_instructions,debug=False):
    start_coord = (0,0)
    final_coord = navigate(nav_instructions, Directions.EAST, start_coord, debug)

    delta_x = start_coord[0] - final_coord[0]
    delta_y = start_coord[1] - final_coord[1]

    if delta_x < 0:
        delta_x *= -1
    if delta_y < 0:
        delta_y *= -1
        
    print("Part 1: {0}".format(delta_x + delta_y))
    return

def calculate_part2(data):
    print("Part 2: {0}".format("TODO"))
    return

def run_program(test=False, debug=False):
    file_path = "solutions\day12\day12.txt"
    if test:
        file_path = "solutions\day12\day12_test.txt"
    
    data = read_nav_instructions(file_path, debug)
    calculate_part1(data, debug)
    calculate_part2(data)

# run_program(True, True)
run_program()