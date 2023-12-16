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
    sequence = []
    for charset in ''.join(data).split(','):
        sequence.append(charset)
    return sequence

class Lens:
    def __init__(self, label, focal_length) -> None:
        self.label = label
        self.focal_length = focal_length
    
    def __repr__(self) -> str:
        return '{0} {1}'.format(self.label, self.focal_length)

def hash_method(charset):
    value = 0
    for char in charset:
        ascii = ord(char)
        value += ascii
        value *= 17
        value %= 256
    return value

def get_commandtype(charset):
    return '-' if '-' in charset else '='

def get_label(charset, splitchar):
    return charset.split(splitchar)[0]

def get_focal_length(charset):
    return int(charset.split('=')[1])

def get_index_of_lens(box, lens_label):
    for i in range(0, len(box)):
        if box[i].label == lens_label: return i
    return -1

def part1(sequence):
    number = 0
    for charset in sequence:
        number += hash_method(charset)
    return number

def part2(sequence, debug):
    boxes = [[] for i in range(0,256)]
    for command in sequence:
        commandtype = get_commandtype(command)
        label = get_label(command, commandtype)
        box = hash_method(label)
        index = get_index_of_lens(boxes[box], label)
        if commandtype == '-':
            if index >= 0: 
                del boxes[box][index]
        elif commandtype == '=':
            focal_length = get_focal_length(command)
            if index >= 0:
                boxes[box][index].focal_length = focal_length
            else:
                boxes[box].append(Lens(label, focal_length))
    
        if debug:
            print('\nAfter {0}'.format(command))
            for i in range(0,256):
                if len(boxes[i]) > 0:
                    print('{0}: {1}'.format(i,boxes[i]))
    
    focusing_power = 0
    for b in range(0, len(boxes)):
        for l in range(0, len(boxes[b])):
            focusing_power += ((b+1)*(l+1)*boxes[b][l].focal_length)
    return focusing_power

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day15.txt'
    
    data = read_data(file_path, debug)
    sequence = format_data(data)

    if debug: print(sequence)

    print(part1(sequence)) # 495972
    print(part2(sequence, debug)) # 245223

run_program(False)