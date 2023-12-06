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
    return data

class SeedRange:
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max
    
    def __repr__(self) -> str:
        return '({0}-{1})'.format(self.min,self.max)

def copy_range(sr: SeedRange):
    return SeedRange(min=sr.min, max=sr.max)

class SeedRule(SeedRange):
    def __init__(self, min, max, offset) -> None:
        self.min = min
        self.max = max
        self.offset = offset
    
    def result_min(self):
        return self.min + self.offset
    
    def result_max(self):
        return self.max + self.offset

    def __repr__(self) -> str:
        offset = '+{0}'.format(self.offset) if self.offset >= 0 else self.offset
        return '({0}-{1}) → {2}'.format(self.min,self.max,offset)
    
def sort_ranges(r: SeedRange):
    return r.min

def format_data(data):
    keys = {
        'seed-to-soil map:': {
            'src': 'seed', 
            'dst': 'soil'
        },
        'soil-to-fertilizer map:': {
            'src': 'soil', 
            'dst': 'fertilizer'
        },
        'fertilizer-to-water map:': {
            'src': 'fertilizer', 
            'dst': 'water'
        },
        'water-to-light map:': {
            'src': 'water', 
            'dst': 'light'
        },
        'light-to-temperature map:': {
            'src': 'light', 
            'dst': 'temperature'
        },
        'temperature-to-humidity map:': {
            'src': 'temperature', 
            'dst': 'humidity'
        },
        'humidity-to-location map:': {
            'src': 'humidity', 
            'dst': 'location'
        },
    }
    seeds = [int(n) for n in data[0].split('seeds: ')[1].split()]
    rule_map = {}
    current_key = None
    for row in data[1:]:
        if row in keys:
            current_key = row
            src = keys[current_key]['src']
            rule_map[src] = {
                'dst': keys[current_key]['dst'],
                'rules': [],
            }
        elif current_key is not None:
            parts = [int(n) for n in row.split()]
            rule_map[src]['rules'].append(SeedRule(
                min=parts[1],
                max=parts[1]+parts[2]-1,
                offset=parts[0]-parts[1],
            ))
    for src in rule_map:
        rule_map[src]['rules'].sort(key=sort_ranges)
    return seeds, rule_map

def part1(seeds, rule_map):
    seed_locations = {}
    for seed in seeds:
        key = 'seed'
        seed_value = seed
        while key != 'location':
            for rule in rule_map[key]['rules']:
                if rule.min <= seed_value <= rule.max:
                    seed_value += rule.offset
                    break
            key = rule_map[key]['dst']
        seed_locations[seed] = seed_value
    return min(seed_locations[seed] for seed in seed_locations)

def part2(seeds, rule_map):
    seed_ranges = []
    for i in range(0, int(len(seeds)/2)):
        seed_ranges.append(SeedRange(
            min=seeds[2*i],
            max=seeds[2*i]+seeds[2*i+1]-1,
        ))
    seed_ranges.sort(key=sort_ranges)

    key = 'seed'
    while key != 'location':
        new_seed_ranges = []
        for seed_range in seed_ranges:
            temp_seed_ranges = []
            updated_sr = copy_range(seed_range)
            for rule in rule_map[key]['rules']:
                if updated_sr is None:
                    break
                if rule.min <= updated_sr.min <= rule.max:
                    if updated_sr.max <= rule.max:
                        temp_seed_ranges.append(SeedRange(
                            min=updated_sr.min+rule.offset,
                            max=updated_sr.max+rule.offset,
                        ))
                        updated_sr = None
                    elif rule.max < updated_sr.max:
                        temp_seed_ranges.append(SeedRange(
                            min=updated_sr.min+rule.offset,
                            max=rule.max+rule.offset,
                        ))
                        updated_sr = SeedRange(
                            min=rule.max+1,
                            max=updated_sr.max,
                        )
                elif rule.min <= updated_sr.max <= rule.max:
                    temp_seed_ranges.append(SeedRange(
                        min=updated_sr.min,
                        max=rule.min-1,
                    ))
                    temp_seed_ranges.append(SeedRange(
                        min=rule.min+rule.offset,
                        max=updated_sr.max+rule.offset,
                    ))
                    updated_sr = None
            if updated_sr is not None:
                temp_seed_ranges.append(updated_sr)
            new_seed_ranges += temp_seed_ranges
        seed_ranges = new_seed_ranges
        seed_ranges.sort(key=sort_ranges)
        key = rule_map[key]['dst']

    return seed_ranges[0].min

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day05.txt'
    
    data = read_data(file_path, debug)
    seeds, rule_map = format_data(data)

    if debug:
        print(seeds)
        print(rule_map)

    print(part1(seeds, rule_map)) # 324724204
    print(part2(seeds, rule_map)) # 104070862

run_program(False)