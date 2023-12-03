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

def format_data(data):
    games = []
    for line in data:
        all_pulls = line.split(": ")
        num = int(all_pulls[0].split(" ")[1])
        pulls = all_pulls[1].split("; ")
        game = {
            'num': num,
            'pulls': [],
            'max': { 'r': 0, 'g': 0, 'b': 0 },
            'power': 0,
        }
        for pull in pulls:
            rgb = { 'r': 0, 'g': 0, 'b': 0 }
            colors = pull.split(', ')
            for color in colors:
                if 'red' in color:
                    rgb['r'] = int(color.split(" ")[0])
                elif 'blue' in color:
                    rgb['b'] = int(color.split(" ")[0])
                elif 'green' in color:
                    rgb['g'] = int(color.split(" ")[0])
            if rgb['r'] > game['max']['r']: game['max']['r'] = rgb['r']
            if rgb['g'] > game['max']['g']: game['max']['g'] = rgb['g']
            if rgb['b'] > game['max']['b']: game['max']['b'] = rgb['b']
            game['pulls'].append(rgb)
        game['power'] = game['max']['r']*game['max']['g']*game['max']['b']
        games.append(game)
    return games

def part1(games):
    possible_games = []
    for game in games:
        if game['max']['r'] <= 12 and game['max']['g'] <= 13 and game['max']['b'] <= 14:
            possible_games.append(game)
    
    return sum(game['num'] for game in possible_games)

def part2(games):
    return sum(game['power'] for game in games)

def run_program(debug=False):
    file_path = "day02.txt"
    
    data = read_data(file_path, debug)
    games = format_data(data)

    print(part1(games)) # 2331
    print(part2(games)) # 71585

run_program(False)