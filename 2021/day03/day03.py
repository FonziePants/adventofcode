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

def format_data(data):
    return data

def binary_to_decimal(bit_count, bit_array):
    dec = 0
    for i in range(0, bit_count):
        dec += (int(bit_array[i]) * (2**(bit_count-i-1)))
    return dec

def get_values(data, debug):
    row_count = len(data)
    bit_count = max(len(row) for row in data)
    zero_counts = [0 for i in range(0, bit_count)]
    for row in data:
        for i in range(0, bit_count):
            if row[i] == '0':
                zero_counts[i] = zero_counts[i] + 1
    
    # part 1
    gr_array = [1 if zero_count > row_count/2 else 0 for zero_count in zero_counts]
    gr = binary_to_decimal(bit_count, gr_array)
    er = (2**(bit_count))-(1+gr)

    # part 2
    og_rows = data.copy()
    for i in range(0, bit_count):
        wip_og_rows = []
        mean_bit = (
            1 if sum(int(row[i]) for row in og_rows) >= len(og_rows)/2 
            else 0
        )
        if debug:
            print(og_rows)
            print('{i}: {v}'.format(i=i, v=mean_bit))
        for row in og_rows:
            if int(row[i]) == mean_bit:
                wip_og_rows.append(row)
        og_rows = wip_og_rows.copy()
        if len(wip_og_rows) <= 1:
            break

    cs_rows = data.copy()
    for i in range(0, bit_count):
        wip_cs_rows = []
        mean_bit = (
            1 if sum(int(row[i]) for row in cs_rows) >= len(cs_rows)/2 
            else 0
        )
        if debug:
            print(cs_rows)
            print('{i}: {v}'.format(i=i, v=mean_bit))
        for row in cs_rows:
            if int(row[i]) != mean_bit:
                wip_cs_rows.append(row)
        cs_rows = wip_cs_rows.copy()
        if len(wip_cs_rows) <= 1:
            break
            
    o2r = binary_to_decimal(bit_count, og_rows[0])
    co2sr = binary_to_decimal(bit_count, cs_rows[0])

    return {
        'gamma_rating': gr,
        'epsilon_rating': er,
        'power_consumption': gr*er,
        'o2_generator_rating': o2r,
        'co2_scrubber_rating': co2sr,
        'life_support_rating': o2r*co2sr,
    }

def part1(values):
    return values['power_consumption']

def part2(values):
    return values['life_support_rating']

def run_program(debug=False):
    file_path = "test.txt" if debug else "day03.txt"
    
    data = read_data(file_path, debug)
    data = format_data(data)

    values = get_values(data, debug)
    print(values)
    print(part1(values)) # 2583164
    print(part2(values)) # 2784375

run_program(False)