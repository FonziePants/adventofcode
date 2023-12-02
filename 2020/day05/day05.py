# --- Day 5: Binary Boarding ---

class SeatAssignment:
    def __init__(self, row=-1, col=-1):
        self.row = row
        self.col = col
        self.seat_id = -1

        if (self.row >= 0 and self.col >= 0):
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

# use for part 1
def find_highest_seat(seats):
    highest_seat = SeatAssignment()
    for seat in seats:
        if seat.seat_id > highest_seat.seat_id:
            highest_seat = seat
    return highest_seat

# use for part 2
def find_missing_seat(seats):
    lowest_seat = SeatAssignment(1000,0) #impossibly high seat
    highest_seat = SeatAssignment()
    seat_sum = 0
    for seat in seats:
        if (seat.seat_id > -1):
            seat_sum += seat.seat_id
        if seat.seat_id > highest_seat.seat_id:
            highest_seat = seat
        if seat.seat_id < lowest_seat.seat_id:
            lowest_seat = seat
    
    print("The lowest seat is " + str(lowest_seat.seat_id))
    print("The highest seat is " + str(highest_seat.seat_id))

    total_seat_sum = 0
    for i in range(lowest_seat.seat_id, highest_seat.seat_id+1):
        total_seat_sum += i
    
    return total_seat_sum - seat_sum

# part 1
# find_highest_seat(ingest_boarding_tickets("day05_real.txt")).print()

# part 2
missing_seat = find_missing_seat(ingest_boarding_tickets("day05_real.txt"))
print("The missing seat is " + str(missing_seat))