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

def diff_char(first, second):
    for c in first:
        if c not in second:
            return c
    return None

def get_number_map(values):
    char_map = {x:'abcdefg' for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g']}
    permutations = {x: [] for x in range(2,8)}
    for value in values:
        permutations[len(value)].append(value)
    
    for c in permutations:
        permutations[c] = list(dict.fromkeys(permutations[c]))

    # solve for a and narrow down c & f
    one = permutations[2][0]
    seven = permutations[3][0]
    char_map['a'] = diff_char(seven, one)
    for c in char_map:
        if c not in 'acf': 
            char_map[c] = char_map[c].replace(seven[0], '')
            char_map[c] = char_map[c].replace(seven[1], '')
            char_map[c] = char_map[c].replace(seven[2], '')
    char_map['c'] = one
    char_map['f'] = one

    # solve for c & f
    zson_shared = []
    for char in permutations[6][0]:
        if char in permutations[6][1] and char in permutations[6][2]:
            zson_shared.append(char)
    char_map['c'] = diff_char(one, zson_shared)
    char_map['f'] = char_map['f'].replace(char_map['c'], '')

    # solve for b, d, g, e
    for i in range(4,8):
        newnums = []
        for num in permutations[i]:
            newnums.append(num.replace(char_map['a'],'').replace(char_map['c'],'').replace(char_map['f'],''))
        permutations[i] = newnums
    three = None
    four = permutations[4][0]
    eight = permutations[7][0]
    for num in permutations[5]:
        if len(num) == 2:
            three = num
            break
    char_map['b'] = diff_char(four, three)
    char_map['d'] = four.replace(char_map['b'],'')
    char_map['g'] = three.replace(char_map['d'],'')
    char_map['e'] = eight.replace(char_map['b'],'').replace(char_map['d'],'').replace(char_map['g'],'')
    
    # flip it so we can do lookups by bad char
    return {char_map[x]: x for x in char_map}

def alphabetize(num_string):
    char_array = list(num_string)
    char_array.sort()
    return ''.join(char_array)

display_map = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}

def fix_garbage(values, char_map):
    fixed_values = []
    for value in values:
        new_value = ''
        for char in value:
            new_value += char_map[char]
        fixed_values.append(display_map[alphabetize(new_value)])
    return fixed_values

def get_number(values):
    num = 0
    for i in range(0,len(values)):
        num += values[len(values)-i-1]*(10**(i))
    return num

class Entry:
    def __init__(self, row) -> None:
        parts = row.split(' | ')
        self.signals = parts[0].split()
        self.outputs = parts[1].split()
        self.map = get_number_map(self.signals+self.outputs)
        self.output = get_number(fix_garbage(self.outputs, self.map))

def format_data(data):
    entries = []
    for row in data:
        entries.append(Entry(row))
    return entries

def part1(entries):
    count = 0
    for entry in entries:
        for output in entry.outputs:
            if len(output) in [2, 4, 3, 7]:
                count += 1
    return count

def part2(entries):
    return sum([entry.output for entry in entries])

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day08.txt'
    
    data = read_data(file_path, debug)
    entries = format_data(data)

    print(part1(entries)) # 493
    print(part2(entries)) # 1010460

run_program(False)