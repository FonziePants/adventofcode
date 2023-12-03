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

opponent_map = {
    'A': 'Rock',
    'B': 'Paper',
    'C': 'Scissors',
}
shape_score = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3,
}

def get_score(opponent, yourplay):
    if opponent == yourplay:
        return 3
    elif (
        (opponent == 'Scissors' and yourplay == 'Rock')
        or (opponent == 'Rock' and yourplay == 'Paper')
        or (opponent == 'Paper' and yourplay == 'Scissors')
    ):
        return 6
    else:
        return 0

def part1(data):
    yourplay_map = {
        'X': 'Rock',
        'Y': 'Paper',
        'Z': 'Scissors',
    }
    rounds = []
    for row in data:
        parts = row.split(" ")
        opponent = opponent_map[parts[0]]
        yourplay = yourplay_map[parts[1]]
        shapescore = shape_score[yourplay]
        outcomescore = get_score(opponent, yourplay)
        totalscore = shapescore + outcomescore
        rounds.append({
            'opponent': opponent,
            'yourplay': yourplay,
            'shapescore': shapescore,
            'outcomescore': outcomescore,
            'totalscore': totalscore,
        })
    return sum(round['totalscore'] for round in rounds)

def part2(data):
    logic = [shape for shape in shape_score]
    yourplay_map = {
        'X': -1, # lose
        'Y': 0,  # draw
        'Z': 1,  # win
    }
    rounds = []
    for row in data:
        parts = row.split(" ")
        opponent = opponent_map[parts[0]]
        yourplay = yourplay_map[parts[1]]
        yourshape = shape_score[opponent] + yourplay - 1
        if yourshape < 0:
            yourshape += 3
        elif yourshape > 2:
            yourshape -= 3
        yourshape = logic[yourshape]
        shapescore = shape_score[yourshape]
        outcomescore = get_score(opponent, yourshape)
        totalscore = shapescore + outcomescore
        rounds.append({
            'opponent': opponent,
            'yourplay': yourshape,
            'shapescore': shapescore,
            'outcomescore': outcomescore,
            'totalscore': totalscore,
        })
    return sum(round['totalscore'] for round in rounds)

def run_program(debug=False):
    file_path = "test.txt" if debug else "day02.txt"
    
    data = read_data(file_path, debug)

    print(part1(data)) # 15523
    print(part2(data)) # 15702

run_program(False)