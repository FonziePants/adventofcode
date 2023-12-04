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

def format_data(data):
    cards = []
    for row in data:
        card = {'instances': 1}
        parts = row.split(': ')
        card['card'] = parts[0].split('Card ')[1]
        parts = parts[1].split(' | ')
        card['left'] = [int(n) for n in parts[0].split()]
        card['right'] = [int(n) for n in parts[1].split()]
        card['winning'] = []
        for num in card['left']:
            if num in card['right']:
                card['winning'].append(num)
        card['score'] = 2**(len(card['winning'])-1) if len(card['winning']) > 0 else 0
        cards.append(card)
    return cards

def part1(cards):
    return sum(card['score'] for card in cards)

def part2(cards):
    for i in range(0, len(cards)):
        card = cards[i]
        for j in range(1, len(card['winning'])+1):
            if i+j < len(cards):
                cards[i+j]['instances'] = cards[i+j]['instances']+card['instances']
    return sum(card['instances'] for card in cards)
    
def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day04.txt'
    
    data = read_data(file_path, debug)
    cards = format_data(data)

    print(part1(cards)) # 27059
    print(part2(cards)) # 5744979

run_program(False)