from math import ceil, floor
from typing import List

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

class Race:
    def __init__(self, time, dist) -> None:
        self.time = int(time)
        self.dist = int(dist)
    
    def __repr__(self) -> str:
        return '{d}mm in {t}ms'.format(
            d=self.dist,
            t=self.time,
        )
    
    def min_hold_time(self):
        value = (self.time - ((self.time**2)-4*self.dist)**(0.5))/2
        if value%1 == 0:
            value += 1
        return ceil(value)
    
    def max_hold_time(self):
        value = (self.time + ((self.time**2)-4*self.dist)**(0.5))/2
        if value%1 == 0:
            value -= 1
        return floor(value)
    
    def ways_to_win(self):
        return self.max_hold_time() - self.min_hold_time() + 1

def format_data(data, bad_kerning=False):
    times = data[0].split('Time:')[1].split()
    dists = data[1].split('Distance:')[1].split()
    if bad_kerning:
        return Race(''.join(times), ''.join(dists))
    else:
        races = []
        for i in range(0, len(times)):
            races.append(Race(times[i], dists[i]))
        return races

def part1(data):
    races = format_data(data, False)
    ways_to_win_multiplied = 1
    for race in races:
        ways_to_win_multiplied *= race.ways_to_win()
    return ways_to_win_multiplied

def part2(data):
    race = format_data(data, True)
    return race.ways_to_win()

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day06.txt'
    
    data = read_data(file_path, debug)

    print(part1(data)) # 293046
    print(part2(data)) # 35150181

run_program(False)