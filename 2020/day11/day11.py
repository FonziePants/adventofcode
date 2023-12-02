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

def count_line_of_sight_occupied_seats(seat_map,row,col,debug=False):
    occupied_seat_count = 0

    # check row (to left)
    for c_index in reversed(range(0,col)):
        if seat_map[row][c_index] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[row][c_index] == Constants.EMPTY:
            break
    
    # check row (to right)
    for c_index in range(col+1,len(seat_map[row])):
        if seat_map[row][c_index] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[row][c_index] == Constants.EMPTY:
            break

    # check col (above)
    for r_index in reversed(range(0,row)):
        if seat_map[r_index][col] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[r_index][col] == Constants.EMPTY:
            break
    
    # check col (below)
    for r_index in range(row+1,len(seat_map)):
        if seat_map[r_index][col] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[r_index][col] == Constants.EMPTY:
            break

    # check inverse diagonal
    for r_index in reversed(range(0,row)):
        c_index = row + col - r_index
        if c_index < 0 or c_index >= len(seat_map[row]):
            continue

        if seat_map[r_index][c_index] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[r_index][c_index] == Constants.EMPTY:
            break

    for r_index in range(row+1,len(seat_map)):
        c_index = row + col - r_index
        if c_index < 0 or c_index >= len(seat_map[row]):
            continue
        if seat_map[r_index][c_index] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[r_index][c_index] == Constants.EMPTY:
            break

    # check direct diagonal
    for r_index in reversed(range(0,row)):
        c_index = col - row + r_index
        if c_index < 0 or c_index >= len(seat_map[row]):
            continue
        if seat_map[r_index][c_index] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[r_index][c_index] == Constants.EMPTY:
            break

    for r_index in range(row+1,len(seat_map)):
        c_index = col - row + r_index
        if c_index < 0 or c_index >= len(seat_map[row]):
            continue
        if seat_map[r_index][c_index] == Constants.OCCUPIED:
            occupied_seat_count += 1
            break
        elif seat_map[r_index][c_index] == Constants.EMPTY:
            break

    return occupied_seat_count

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

def execute_seating_round(seat_map,tolerance=4,only_neighbors=True,debug=False):
    new_seat_map = copy_seat_map(seat_map)
    seat_changed = False

    for row in range(len(seat_map)):
        for col in range(len(seat_map[row])):
            spot = seat_map[row][col]

            if spot == Constants.FLOOR:
                continue

            occupied_neighbors = 0
            if only_neighbors:
                occupied_neighbors = count_neighboring_occupied_seats(seat_map,row,col)
            else:
                occupied_neighbors = count_line_of_sight_occupied_seats(seat_map,row,col,debug)

            if spot == Constants.EMPTY and occupied_neighbors == 0:
                new_seat_map[row][col] = Constants.OCCUPIED
                seat_changed = True
            elif spot == Constants.OCCUPIED and occupied_neighbors >= tolerance:
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
        new_seat_map = execute_seating_round(old_seat_map, 4, True, debug)

        if not new_seat_map:
            occupied_seat_count = count_occupied_seats(old_seat_map)
            print("Part 1: {0} occupied seats".format(occupied_seat_count))
            return
        
        old_seat_map = copy_seat_map(new_seat_map)

def calculate_part2(seat_map,debug):
    old_seat_map = copy_seat_map(seat_map)
    new_seat_map = copy_seat_map(seat_map)

    counter = 0
    while(True):
        new_seat_map = execute_seating_round(old_seat_map, 5, False, debug)

        if not new_seat_map:
            occupied_seat_count = count_occupied_seats(old_seat_map)
            print("Part 2: {0} occupied seats".format(occupied_seat_count))
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
    file_path = "day11_real.txt"
    if test:
        file_path = "day11_test.txt"
    
    seat_map = read_initial_seat_map(file_path, debug)
    calculate_part1(seat_map,debug)
    calculate_part2(seat_map, debug)

# run_program(True, True)
run_program()