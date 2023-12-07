from copy import deepcopy
import operator

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

# key = (# unique cards, max # matching cards)
hand_values = {
    (1,5): 7, # 5K
    (2,4): 6, # 4K
    (2,3): 5, # FH
    (3,3): 4, # 3K
    (3,2): 3, # 2P
    (4,2): 2, # 1P
    (5,1): 1, # HC
}

card_values = {**{
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
}, **{str(n): n for n in range(9,1,-1)}}

card_values_2 = {**card_values, 'J': 1}

def calc_hand_value(hand, wild_j):
    cards = {}
    for card in hand:
        cards[card] = cards[card]+1 if card in cards else 1
    j = cards.pop('J', 0) if wild_j else 0
    unique = len(cards)
    max_match = max([cards[c] for c in cards]) + j if unique > 0 else 5
    return hand_values[(max(unique, 1), max_match)]

def calc_order(value, hand, c_values):
    return '{hand}{high}'.format(
            hand=value,
            high=''.join([hex(c_values[c])[2:] for c in hand]),
        )

class Hand:
    def __init__(self, input) -> None:
        parts = input.split()
        self.hand = parts[0]
        self.bid = int(parts[1])
        self.value = calc_hand_value(self.hand, wild_j=False)
        self.value2 = calc_hand_value(self.hand, wild_j=True)
        self.order = calc_order(self.value, self.hand, card_values)
        self.order2 = calc_order(self.value2, self.hand, card_values_2)
    
    def __repr__(self) -> str:
        return self.hand

def format_data(data):
    hands = []
    for row in data:
        hands.append(Hand(row))
    return hands

def calculate_winnings(hands, order_key, debug):
    ranked_hands = deepcopy(hands)
    ranked_hands.sort(key=operator.attrgetter(order_key))
    if debug: print(ranked_hands)

    winnings = 0
    for i in range(0,len(ranked_hands)):
        winnings += ranked_hands[i].bid*(i+1)
    return winnings

def part1(hands, debug):
    return calculate_winnings(hands, 'order', debug)

def part2(hands, debug):
    return calculate_winnings(hands, 'order2', debug)

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day07.txt'
    
    data = read_data(file_path, debug)
    hands = format_data(data)

    if debug: print(hands)

    print(part1(hands, debug)) # 253933213
    print(part2(hands, debug)) # 253473930

run_program(debug=False)