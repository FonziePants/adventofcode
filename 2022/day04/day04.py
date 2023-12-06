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

class SectionRange:
    def __init__(self, input) -> None:
        parts = input.split('-')
        self.min=int(parts[0])
        self.max=int(parts[1])
    
    def __repr__(self) -> str:
        return '{0}-{1}'.format(
            self.min,
            self.max,
        )

class Pair:
    def __init__(self, input) -> None:
        parts = input.split(',')
        self.range1 = SectionRange(parts[0])
        self.range2 = SectionRange(parts[1])
    
    def __repr__(self) -> str:
        return '{0} / {1}'.format(
            self.range1,
            self.range2,
        )
    
    def one_contains_other(self):
        return (
            self.range1.min <= self.range2.min <= self.range2.max <= self.range1.max
            or self.range2.min <= self.range1.min <= self.range1.max <= self.range2.max
        )
    
    def ranges_overlap(self):
        return (
            self.range1.min <= self.range2.min <= self.range1.max
            or self.range1.min <= self.range2.max <= self.range1.max
            or self.range2.min <= self.range1.min <= self.range2.max
            or self.range2.min <= self.range1.max <= self.range2.max
        )


def format_data(data):
    pairs = []
    for row in data:
        pairs.append(Pair(row))
    return pairs

def part1(pairs):
    count = 0
    for pair in pairs:
        if pair.one_contains_other():
            count += 1
    return count

def part2(pairs):
    count = 0
    for pair in pairs:
        if pair.ranges_overlap():
            count += 1
    return count

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day04.txt'
    
    data = read_data(file_path, debug)
    pairs = format_data(data)

    if debug:
        print(pairs)

    print(part1(pairs)) # 532
    print(part2(pairs)) # 854

run_program(False)