import re
def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []

    for line in file:
        if not line.rstrip():
            continue
        sline = line.rstrip()

        data.append(sline)
    
    file.close()

    if debug:
        print(data)

    return data

def part1(data):
    numbers = []
    regex = r"\d"
    for line in data:
        first = re.search(regex, line)
        last = re.search(regex, line[::-1])

        f_char = first.group(0) if first else ''
        l_char = last.group(0) if last else ''

        numbers.append(int('{0}{1}'.format(f_char, l_char)))
    
    return sum(n for n in numbers)

def convert_text_to_num(text):
    return text.replace('one','1').replace('two','2').replace('three','3').replace('four','4').replace('five','5').replace('six','6').replace('seven','7').replace('eight','8').replace('nine','9')

def part2(data):
    numbers = []
    for line in data:
        first = re.search(r"(\d|one|two|three|four|five|six|seven|eight|nine)", line)
        last = re.search(r"(\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)", line[::-1])

        f_char = convert_text_to_num(first.group(0) if first else '')
        l_char = convert_text_to_num(last.group(0)[::-1] if last else '')

        numbers.append(int('{0}{1}'.format(f_char, l_char)))
    
    return sum(n for n in numbers)

def run_program(debug=False):
    file_path = "day01.txt"
    
    data = read_data(file_path, debug)

    print(part1(data)) # 54916
    print(part2(data)) # 54728

run_program(False)