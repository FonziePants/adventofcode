def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        data.append(line.rstrip())
    
    file.close()

    if debug:
        print(data)

    return data

def convert_to_binary(dec_num):
    bin_num = ""
    remainder = dec_num
    while remainder > 0:
        bin_dgt = "0"
        if remainder % 2 == 1:
            bin_dgt = "1"
            remainder -= 1
        bin_num = bin_dgt + bin_num
        remainder = int(remainder/2)
    return bin_num

def convert_to_decimal(bin_num):
    dec_num = 0
    for i in reversed(range(len(bin_num))):
        bin_dgt = int(bin_num[i])
        dec_num += (2**(len(bin_num)-1-i))*bin_dgt
    return dec_num

def apply_mask(mask,bin_num,pt2=False):
    while len(bin_num) < len(mask):
        bin_num = "0" + bin_num
    bin_list = list(bin_num)
    mask_list = list(mask)
    for i in range(len(mask_list)):
        if mask_list[i] == "X" and not pt2:
            continue
        elif mask_list[i] == "0" and pt2:
            continue
        bin_list[i] = mask_list[i]
    return "".join(bin_list).strip()


def calculate_part1(data,debug=False):   
    memory = {}
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    for line in data:
        if "mask" in line:
            mask = line[6:]
        else:
            parts = line.split("] = ") 
            address = parts[0][4:]
            dec_val = int(parts[1])
            bin_val = convert_to_binary(dec_val)
            bin_val = apply_mask(mask, bin_val)
            dec_val = convert_to_decimal(bin_val)
            memory[address] = dec_val
    
    sum = 0
    for address in memory:
        sum += memory[address]

    print("Part 1: {0}\n\n".format(sum))
    return

def generate_addresses(base_address):
    addresses = [base_address]
    idx = -1
    while idx < len(base_address)-1:
        idx += 1
        if base_address[idx] != "X":
            continue
        new_addresses = []
        for address in addresses:
            add_list = list(address)
            for b in range(0,2):
                add_list[idx] = str(b)
                new_addresses.append("".join(add_list))
        addresses = new_addresses
            
    return addresses

def calculate_part2(data,debug=False):
    memory = {}
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    for line in data:
        if "mask" in line:
            mask = line[6:]
        else:
            parts = line.split("] = ") 
            value = int(parts[1])
            dec_address = int(parts[0][4:])
            bin_address = convert_to_binary(dec_address)
            bin_address = apply_mask(mask, bin_address, True)
            addresses = generate_addresses(bin_address)
            for address in addresses:
                memory[address] = value
    
    sum = 0
    for address in memory:
        sum += memory[address]

    print("Part 2: {0}\n\n".format(sum))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day14\day14.txt"
    if test:
        file_path = "solutions\day14\day14_test.txt"
    
    data = read_data(file_path, debug)

    calculate_part1(data, debug)
    calculate_part2(data, debug)

# run_program(True, False)
run_program()