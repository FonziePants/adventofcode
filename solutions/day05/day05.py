# --- Day 5: Binary Boarding ---
# You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.

# You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.

# Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

# For example, consider just the first seven characters of FBFBBFFRLR:

# Start by considering the whole range, rows 0 through 127.
# F means to take the lower half, keeping rows 0 through 63.
# B means to take the upper half, keeping rows 32 through 63.
# F means to take the lower half, keeping rows 32 through 47.
# B means to take the upper half, keeping rows 40 through 47.
# B keeps rows 44 through 47.
# F keeps rows 44 through 45.
# The final F keeps the lower of the two, row 44.
# The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

# For example, consider just the last 3 characters of FBFBBFFRLR:

# Start by considering the whole range, columns 0 through 7.
# R means to take the upper half, keeping columns 4 through 7.
# L means to take the lower half, keeping columns 4 through 5.
# The final R keeps the upper of the two, column 5.
# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.

# Here are some other boarding passes:

# BFFFBBFRRR: row 70, column 7, seat ID 567.
# FFFBBBFRRR: row 14, column 7, seat ID 119.
# BBFFBBFRLL: row 102, column 4, seat ID 820.
# As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?

class SeatAssignment:
    def __init__(self, row=-1, col=-1):
        self.row = row
        self.col = col
        self.seat_id = -1

        if (self.row > 0 and self.col > 0):
            self.seat_id = self.row * 8 + self.col
    
    def print(self):
        print("Seat Assignment is row " + str(self.row) + ", col " + str(self.col) + ", seat ID " + str(self.seat_id))

def convert_binary_int_to_decimal(binary_num):
    return convert_binary_str_to_decimal(str(binary_num))

def convert_binary_str_to_decimal(binary_str):
    decimal_num = 0
    for i in reversed(range(len(binary_str))):
        binary_dgt = binary_str[i]
        if not binary_dgt.isdigit():
            print("WARNING: The input string had an invalid format: " + binary_str)
            return -1
        decimal_num += (2**(len(binary_str)-1-i))*int(binary_dgt)
    print("The binary number " + binary_str + " is equal to " + str(decimal_num) + " in decimal")
    return decimal_num

def parse_seat_assignment(seat_assignment):
    #verify it's the correct format
    if len(seat_assignment) != 10:
        print("WARNING: The seating assignment is the wrong length. It should be 10 characters, but it has " + str(len(seat_assignment)) + " characters instead.")
        return SeatAssignment()
    
    row_str = seat_assignment[0:7].replace("F","0").replace("B","1")
    row = convert_binary_str_to_decimal(row_str)

    col_str = seat_assignment[7:].replace("L","0").replace("R","1")
    col = convert_binary_str_to_decimal(col_str)

    return SeatAssignment(row,col)

def ingest_boarding_tickets(input_file):
    file = open(input_file, "r")

    seats = []
    for line in file:
        seats.append(parse_seat_assignment(line.rstrip()))
    
    file.close()

    return seats

def find_highest_seat(seats):
    highest_seat = SeatAssignment()
    for seat in seats:
        if seat.seat_id > highest_seat.seat_id:
            highest_seat = seat
    return highest_seat

find_highest_seat(ingest_boarding_tickets("solutions\day05\day05_real.txt")).print()