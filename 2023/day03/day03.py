def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        if not line.rstrip():
            continue
        sline = line.rstrip()
        data.append(sline)
        
    file.close()
    if debug: print(data)
    return data

def get_boundary(data, number: str, row: int, col: int):
    start_row = row-1 if row > 0 else row
    end_row = row+2 if row+1 < len(data) else row+1
    start_col = col-1 if col > 0 else col
    end_col = col+len(number)+1 if col+len(number) < len(data[row]) else col+1
    return (start_row, end_row, start_col, end_col)

def check_number(data, number: str, row: int, col: int):
    start_row, end_row, start_col, end_col = get_boundary(data, number, row, col)

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            char = data[r][c]
            if not char.isdigit() and char != '.':
                return True
            
    return False

def format_data(data):
    part_numbers = []
    number = None
    number_row = None
    number_col = None # start col
    for row in range(0, len(data)):
        for col in range(0, len(data[0])):
            if data[row][col].isdigit(): 
                if number is None:
                    number = ''
                    number_row = row
                    number_col = col
                number += data[row][col]
            elif number is not None:
                if check_number(data, number, number_row, number_col):
                    part_numbers.append({
                        'part': int(number),
                        'boundary': get_boundary(data, number, number_row, number_col)
                    })
                number = None
                number_row = None
                number_col = None

    return part_numbers

def part1(part_numbers):
    return sum(n['part'] for n in part_numbers)

def adjacent_part_numbers(row, col, part_numbers):
    adjacent = []
    for pn in part_numbers:
        sr, er, sc, ec = pn['boundary']
        if (sr <= row < er) and (sc <= col < ec):
            adjacent.append(pn['part'])
    return adjacent

def part2(data, part_numbers):
    gears = []
    for row in range(0, len(data)):
        for col in range(0, len(data[0])):
            if data[row][col] == '*':
                adjacent_parts = adjacent_part_numbers(row, col, part_numbers)
                if len(adjacent_parts) == 2:
                    gears.append(adjacent_parts)
    return sum(g[0]*g[1] for g in gears)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day03.txt'
    
    data = read_data(file_path, debug)
    part_numbers = format_data(data)

    print(part1(part_numbers)) # 520135
    print(part2(data, part_numbers)) # 72514855

run_program(False)