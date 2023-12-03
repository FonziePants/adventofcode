def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        sline = line.rstrip()
        data.append(sline)
        
    file.close()
    if debug: print(data)
    return data

def format_data(data):
    elves = []
    food = []
    calories = 0
    for row in data:
        if len(row) == 0:
            elves.append({
                'food': food,
                'calories': calories,
            })
            food = []
            calories = 0
        else:
            item = int(row)
            food.append(item)
            calories += item

    return elves

def part1(elves):
    return max(elf['calories'] for elf in elves)

def part2(elves):
    calorie_counts = [elf['calories'] for elf in elves]
    calorie_counts.sort(reverse=True)
    return sum(cc for cc in calorie_counts[:3])

def run_program(debug=False):
    file_path = "day01.txt"
    
    data = read_data(file_path, debug)
    elves = format_data(data)

    if debug:
        print(elves)

    print(part1(elves)) # 66719
    print(part2(elves)) # 198551

run_program(False)