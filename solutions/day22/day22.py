def read_data(file_path,debug=True):
    file = open(file_path, "r")

    player1 = None
    player2 = None

    player_name = None
    player_cards = []

    for line in file:
        if not line.rstrip():
            continue

        if "Player" in line:
            # check to see if player 1 is wrapped up
            if player_name:
                player1 = Player(player_name,player_cards.copy())

            player_name = line.rstrip()[0:-1]
            player_cards = []
        else:
            player_cards.append(int(line.rstrip()))
    
    file.close()

    player2 = Player(player_name,player_cards.copy())

    if debug:
        player1.print()
        player2.print()

    return (player1,player2)

class Player:
    def __init__(self, name, cards):
        self.cards = cards
        self.name = name
    
    def has_cards(self):
        return len(self.cards) > 0
    
    def count_cards(self):
        return len(self.cards)
    
    def play_card(self):
        if len(self.cards) == 0:
            return None
        card = self.cards[0]
        self.cards = self.cards[1:]
        return card
    
    def count_score(self):
        score = 0
        for i in range(len(self.cards)):
            score += (self.cards[i] * (len(self.cards)-i))
        return score
    
    def add_cards(self,cards):
        for card in cards:
            self.cards.append(card)
    
    def get_hand_state(self):
        return self.name.replace(" ","") + ":" + ",".join(list(map(str,self.cards)))
    
    def copy(self):
        return Player(self.name, self.cards.copy())
    
    def copy_and_trim(self, size):
        cards = self.cards[0:size]
        return Player(self.name,cards)
    
    def print(self):
        print("{0}: {1}".format(self.name,self.cards))

def play_game(player1, player2, round_outcomes, debug=False):
    past_rounds = []
    winner = None

    if debug:
        print("NEW GAME")

    starting_round = player1.get_hand_state() + "|" + player2.get_hand_state()

    # check for cache hits
    if starting_round in round_outcomes:
        return round_outcomes[starting_round]

    # a "round"
    while player1.has_cards() and player2.has_cards():
        # check for infinite loop
        round = player1.get_hand_state() + "|" + player2.get_hand_state()
        if round in past_rounds:
            round_outcomes[starting_round] = player1
            return player1
        else:
            past_rounds.append(round)

        p1 = player1.play_card()
        p2 = player2.play_card()

        if debug:
            print("ROUND:\nPlayer 1: {0}\nPlayer 2: {1}\n".format(p1,p2))

        # check for recursive combat
        if player1.count_cards() >= p1 and player2.count_cards() >= p2:
            winner = play_game(player1.copy_and_trim(p1), player2.copy_and_trim(p2), round_outcomes, debug)
            if winner.name == player1.name:
                player1.add_cards([p1, p2])
            else:
                player2.add_cards([p2, p1])
        # otherwise, play normally
        elif p1 > p2:
            player1.add_cards([p1, p2])
        else:
            player2.add_cards([p2, p1])
        
        if debug:
            print("GAME CONCLUSION\n")
            player1.print()
            player2.print()
            print()

    winner = player1 if player1.has_cards() else player2

    # add outcome to cache to save time later
    round_outcomes[starting_round] = winner

    return winner

def calculate_part1(player1, player2, debug=False):   
    while player1.has_cards() and player2.has_cards():
        p1 = player1.play_card()
        p2 = player2.play_card()

        if p1 > p2:
            player1.add_cards([p1, p2])
        else:
            player2.add_cards([p2, p1])
        
        if debug:
            player1.print()
            player2.print()
    
    winner = player1 if player1.has_cards() else player2

    print("Part 1: {0}\n\n".format(winner.count_score()))
    return

def calculate_part2(player1, player2, debug=False):
    winner = play_game(player1, player2, {}, debug)

    print("Part 2: {0}\n\n".format(winner.count_score()))
    return 

def run_program(test=False, debug=False):
    file_path = "solutions\day22\day22.txt"
    if test:
        file_path = "solutions\day22\day22_test.txt"
    
    data = read_data(file_path, debug)
    player1 = data[0]
    player2 = data[1]
    calculate_part1(player1.copy(), player2.copy(), debug)
    calculate_part2(player1.copy(), player2.copy(), debug)

# run_program(True, True)
run_program()