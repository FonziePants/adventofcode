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
    numbers = []
    for row in data:
        numbers.append([int(n) for n in row.split()])
    return numbers

def get_history_diff(numbers):
    history = []
    for i in range(1, len(numbers)):
        history.append(numbers[i]-numbers[i-1])
    return history

def history_diff_is_zero(history):
    return min(history) == 0 == max(history)

def calc_next_value(histories):
    value = 0
    for i in range(0,len(histories)):
        value += histories[i][-1]
    return value

def calc_prev_value(histories):
    value = 0
    for i in range(len(histories)-1,-1,-1):
        value = histories[i][0] - value
    return value

def calc_histories(numbers):
    calcs = []
    for number_set in numbers:
        histories = [number_set]
        history = get_history_diff(number_set)
        histories.append(history)
        while(not history_diff_is_zero(history)):
            history = get_history_diff(history)
            histories.append(history)
        calcs.append(histories)
    return calcs

def part1(histories):
    next_values = [calc_next_value(history) for history in histories]
    return sum(next_values)

def part2(histories):
    prev_values = [calc_prev_value(history) for history in histories]
    return sum(prev_values)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day09.txt'
    
    data = read_data(file_path, debug)
    numbers = format_data(data)
    histories = calc_histories(numbers)

    if debug: 
        print(numbers)
        print(histories)

    print(part1(histories)) # 1853145119
    print(part2(histories)) # 923

run_program(False)