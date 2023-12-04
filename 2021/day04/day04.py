from copy import deepcopy

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
    numbers = [int(n) for n in data[0].split(',')]
    boards = []
    row = 2
    while row < len(data):
        board = []
        for i in range (0,5):
            board.append([int(n) for n in data[row+i].split()])
        boards.append(board)
        row += 6
    return numbers, boards

def check_score(numbers, board):
    scored_board = deepcopy(board)
    for number in numbers:
        for r in range(0,5):
            for c in range(0,5):
                if board[r][c] == number:
                    scored_board[r][c] = None
    bingo = False
    for r in range(0,5):
        bingo = True
        for c in range(0,5):
            if scored_board[r][c] is not None:
                bingo = False
                break
        if bingo:
            break
    if not bingo:
        for c in range(0,5):
            bingo = True
            for r in range(0,5):
                if scored_board[r][c] is not None:
                    bingo = False
                    break
            if bingo:
                break
    if not bingo: return -1
    last_num = numbers[-1]
    num_sum = 0
    for row in scored_board:
        for col in row:
            if col is not None:
                num_sum += col
    return last_num * num_sum
    

def part1(numbers, boards):
    for n in range(0, len(numbers)):
        for board in boards:
            score = check_score(numbers[:n+1],board)
            if score > 0:
                return score

def part2(numbers, boards):
    winning_boards = []
    for n in range(0, len(numbers)):
        for b in range(0, len(boards)):
            if b in winning_boards:
                continue
            score = check_score(numbers[:n+1],boards[b])
            if score > 0:
                winning_boards.append(b)
                if len(winning_boards) == len(boards):
                    return score

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day04.txt'
    
    data = read_data(file_path, debug)
    numbers, boards = format_data(data)

    print(part1(numbers, boards)) # 41668
    print(part2(numbers, boards)) # 10478

run_program(False)