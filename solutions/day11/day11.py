# --- Day 11: Seating System ---

class Constants:
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"

def read_initial_seat_map(file_path,debug=True):
    file = open(file_path, "r")

    seat_map = []

    for line in file:
        if not line.rstrip():
            continue
        seat_map.append(list(line.rstrip()))
    
    file.close()
    
    if debug:
        print_seat_map(seat_map)

    return seat_map

def print_seat_map(seat_map):
    for row in seat_map:
        row_s = ""
        for col in row:
            row_s += col + " "
        print(row_s)

def count_neighboring_occupied_seats(seat_map,row,col):
    occupied_seat_count = 0

    top_bound = -1
    bottom_bound = 2
    left_bound = -1
    right_bound = 2

    if row == 0:
        top_bound = 0
    if row == len(seat_map)-1:
        bottom_bound = 1
    if col == 0:
        left_bound = 0
    if col == len(seat_map[row])-1:
        right_bound = 1
    
    for r in range(top_bound,bottom_bound):
        for c in range(left_bound,right_bound):
            # don't check yourself
            if r == 0 and c == 0:
                continue

            if seat_map[row+r][col+c] == Constants.OCCUPIED:
                occupied_seat_count += 1

    return occupied_seat_count

def copy_seat_map(seat_map):
    new_seat_map = []
    for row in seat_map:
        new_seat_map.append(row.copy())
    return new_seat_map

def execute_seating_round(seat_map,debug):
    new_seat_map = copy_seat_map(seat_map)
    seat_changed = False

    for row in range(len(seat_map)):
        for col in range(len(seat_map[row])):
            spot = seat_map[row][col]

            if spot == Constants.FLOOR:
                continue

            occupied_neighbors = count_neighboring_occupied_seats(seat_map,row,col)
            if spot == Constants.EMPTY and occupied_neighbors == 0:
                new_seat_map[row][col] = Constants.OCCUPIED
                seat_changed = True
            elif spot == Constants.OCCUPIED and occupied_neighbors >= 4:
                new_seat_map[row][col] = Constants.EMPTY
                seat_changed = True

    if debug:
        print("SEATING ROUND EXECUTED")
        print_seat_map(new_seat_map)

    if not seat_changed:
        return False
    
    return new_seat_map

def calculate_part1(seat_map,debug):
    old_seat_map = copy_seat_map(seat_map)
    new_seat_map = copy_seat_map(seat_map)

    while(True):
        new_seat_map = execute_seating_round(old_seat_map, debug)

        if not new_seat_map:
            occupied_seat_count = count_occupied_seats(old_seat_map)
            print("Part 1: {0} occupied seats".format(occupied_seat_count))
            return
        
        old_seat_map = copy_seat_map(new_seat_map)

def count_occupied_seats(seat_map):
    occupied_seat_count = 0
    for row in seat_map:
        for col in row:
            if col == Constants.OCCUPIED:
                occupied_seat_count += 1

    return occupied_seat_count

def run_program(test=False, debug=False):
    file_path = "solutions\day11\day11_real.txt"
    if test:
        file_path = "solutions\day11\day11_test.txt"
    
    seat_map = read_initial_seat_map(file_path, debug)
    calculate_part1(seat_map,debug)

# run_program(True, True)
run_program()