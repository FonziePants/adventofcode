def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        if not line.rstrip():
            continue
        sline = line.rstrip()
        data.append(sline)
        
    file.close()
    data = [int(num) for num in data[0].split(',')]
    data.sort()
    if debug: print(data)
    return data

def part1(crab_spots, debug):
    position = crab_spots[int(len(crab_spots)/2)]
    moves = 0
    for crab_spot in crab_spots:
        moves += abs(position-crab_spot)
    return moves

def calc_fuel_costs(crab_spots):
    hi = max(crab_spots)
    fuel_costs = {}
    for dist in range(0, hi+1):
        fuel_costs[dist] = fuel_costs[dist-1]+dist if dist > 0 else 0
    return fuel_costs

def part2(crab_spots, debug):
    fuel_costs = calc_fuel_costs(crab_spots)
    print(fuel_costs)
    lowest_fuel = 1000000000000
    best_position = None
    for position in range(0, max(crab_spots)+1):
        fuel = 0
        for crab_spot in crab_spots:
            dist = abs(crab_spot-position)
            fuel += fuel_costs[dist]
        if debug:
            print('{0}: {1}'.format(position, fuel))
        if fuel < lowest_fuel:
            best_position = position
            print('best: {0} @ {1}'.format(best_position, fuel))
        lowest_fuel = min(fuel, lowest_fuel)
    return lowest_fuel

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day07.txt'
    
    crab_spots = read_data(file_path, debug)

    print(part1(crab_spots, debug)) # 345197
    print(part2(crab_spots, debug)) # 96361606

run_program(False)