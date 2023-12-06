from copy import deepcopy

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

def total_fish(fish_per_day):
    total = 0
    for day in fish_per_day:
        total += fish_per_day[day]
    return total

def format_data(data):
    fish_per_day = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
    }
    fishies = [int(n) for n in data[0].split(',')]
    for fish in fishies:
        fish_per_day[fish] = fish_per_day[fish]+1
    return fish_per_day

def fish_after_x_days(orig_fish_per_day, days, debug):
    fish_per_day = deepcopy(orig_fish_per_day)
    for day in range(0,days):
        d = day%7
        mature_fish = fish_per_day[7]
        fish_per_day[7] = fish_per_day[8]
        fish_per_day[8] = fish_per_day[d] # new fish
        fish_per_day[d] = fish_per_day[d] + mature_fish
        if debug:
            print('Day {0}: {1} fish -- {2}'.format(
                day,
                total_fish(fish_per_day),
                fish_per_day,
            ))

    return total_fish(fish_per_day)

def part1(fish_per_day, debug):
    return fish_after_x_days(fish_per_day, 80, debug)

def part2(fish_per_day, debug):
    return fish_after_x_days(fish_per_day, 256, debug)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day06.txt'
    
    data = read_data(file_path, debug)
    fish_per_day = format_data(data)

    if debug:
        print(fish_per_day)

    print(part1(fish_per_day, debug)) # 379414
    print(part2(fish_per_day, debug)) # 1705008653296

run_program(False)