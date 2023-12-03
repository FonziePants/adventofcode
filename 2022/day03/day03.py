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

alphabet = 'abcdefghijklmnopqrstuvwxyz'
priorities = alphabet + alphabet.upper()

def format_data(data):
    rucksacks = []
    for row in data:
        count = int(len(row)/2)
        one = row[0:count]
        two = row[count:]
        matched_item = None
        for item in one:
            if item in two:
                matched_item = item
                break
        rucksacks.append({
            'bag': row,
            'one': one,
            'two': two,
            'item': matched_item,
            'value': priorities.index(matched_item)+1,
        })
    return rucksacks

def part1(rucksacks):
    return sum(rucksack['value'] for rucksack in rucksacks)

def part2(rucksacks):
    group_count = int(len(rucksacks)/3)
    groups = []
    for i in range(0, group_count):
        rs1 = rucksacks[i*3]
        rs2 = rucksacks[i*3+1]
        rs3 = rucksacks[i*3+2]
        for item in rs1['bag']:
            if item in rs2['bag'] and item in rs3['bag']:
                groups.append({
                    'item': item,
                    'value': priorities.index(item)+1,
                    'rucksacks': [rs1, rs2, rs3],
                })
                break

    return sum(group['value'] for group in groups)

def run_program(debug=False):
    file_path = "test.txt" if debug else "day03.txt"
    
    data = read_data(file_path, debug)
    data = format_data(data)

    if debug:
        print(data)

    print(part1(data)) # 7581
    print(part2(data)) # 2525

run_program(False)