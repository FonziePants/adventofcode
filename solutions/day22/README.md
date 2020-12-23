# [Day 15: Rambunctious Recitation](https://adventofcode.com/2020/day/15)
>--- Day 22: Crab Combat ---
>
>It only takes a few hours of sailing the ocean on a raft for boredom to sink in. Fortunately, you brought a small deck of space cards! You'd like to play a game of Combat, and there's even an opponent available: a small crab that climbed aboard your raft before you left.
>
>Fortunately, it doesn't take long to teach the crab the rules.
>
>Before the game starts, split the cards so each player has their own deck (your puzzle input). Then, the game consists of a series of rounds: both players draw their top card, and the player with the higher-valued card wins the round. The winner keeps both cards, placing them on the bottom of their own deck so that the winner's card is above the other card. If this causes a player to have all of the cards, they win, and the game ends.
>
>For example, consider the following starting decks:
>```
>Player 1:
>9
>2
>6
>3
>1
>
>Player 2:
>5
>8
>4
>7
>10
>```
>This arrangement means that player 1's deck contains 5 cards, with 9 on top and 1 on the bottom; player 2's deck also contains 5 cards, with 5 on top and 10 on the bottom.
>
>The first round begins with both players drawing the top card of their decks: 9 and 5. Player 1 has the higher card, so both cards move to the bottom of player 1's deck such that 9 is above 5. In total, it takes 29 rounds before a player has all of the cards:
>```
>-- Round 1 --
>Player 1's deck: 9, 2, 6, 3, 1
>Player 2's deck: 5, 8, 4, 7, 10
>Player 1 plays: 9
>Player 2 plays: 5
>Player 1 wins the round!
>
>-- Round 2 --
>Player 1's deck: 2, 6, 3, 1, 9, 5
>Player 2's deck: 8, 4, 7, 10
>Player 1 plays: 2
>Player 2 plays: 8
>Player 2 wins the round!
>
>-- Round 3 --
>Player 1's deck: 6, 3, 1, 9, 5
>Player 2's deck: 4, 7, 10, 8, 2
>Player 1 plays: 6
>Player 2 plays: 4
>Player 1 wins the round!
>
>-- Round 4 --
>Player 1's deck: 3, 1, 9, 5, 6, 4
>Player 2's deck: 7, 10, 8, 2
>Player 1 plays: 3
>Player 2 plays: 7
>Player 2 wins the round!
>
>-- Round 5 --
>Player 1's deck: 1, 9, 5, 6, 4
>Player 2's deck: 10, 8, 2, 7, 3
>Player 1 plays: 1
>Player 2 plays: 10
>Player 2 wins the round!
>
>...several more rounds pass...
>
>-- Round 27 --
>Player 1's deck: 5, 4, 1
>Player 2's deck: 8, 9, 7, 3, 2, 10, 6
>Player 1 plays: 5
>Player 2 plays: 8
>Player 2 wins the round!
>
>-- Round 28 --
>Player 1's deck: 4, 1
>Player 2's deck: 9, 7, 3, 2, 10, 6, 8, 5
>Player 1 plays: 4
>Player 2 plays: 9
>Player 2 wins the round!
>
>-- Round 29 --
>Player 1's deck: 1
>Player 2's deck: 7, 3, 2, 10, 6, 8, 5, 9, 4
>Player 1 plays: 1
>Player 2 plays: 7
>Player 2 wins the round!
>
>
>== Post-game results ==
>Player 1's deck: 
>Player 2's deck: 3, 2, 10, 6, 8, 5, 9, 4, 7, 1
>```
>Once the game ends, you can calculate the winning player's score. The bottom card in their deck is worth the value of the card multiplied by 1, the second-from-the-bottom card is worth the value of the card multiplied by 2, and so on. With 10 cards, the top card is worth the value on the card multiplied by 10. In this example, the winning player's score is:
>```
>   3 * 10
>+  2 *  9
>+ 10 *  8
>+  6 *  7
>+  8 *  6
>+  5 *  5
>+  9 *  4
>+  4 *  3
>+  7 *  2
>+  1 *  1
>= 306
>```
>So, once the game ends, the winning player's score is 306.

My instinct on this one was to create a `Player` class that would keep track of the hand mutations and handle repeat transformations and logic with convenience methods. Thus:
```
class Player:
    def __init__(self, name, cards):
        self.cards = cards
        self.name = name
    
    def has_cards(self):
        return len(self.cards) > 0
    
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
    
    def print(self):
        print("{0}: {1}".format(self.name,self.cards))
```

## Part 1
>Play the small crab in a game of Combat using the two decks you just dealt. What is the winning player's score?
>
>Your puzzle answer was **33434**.

The logic here was pretty simple:
1. **Loop while both of the players still have cards in their hand**, as determined by the aforementioned `Player.has_cards()` convenience method
```
while player1.has_cards() and player2.has_cards():
```

2. **Grab the top cards from each player's hand** using the convenience method `Player.play_card()`, which handles mutating the deck.
```
    p1 = player1.play_card()
    p2 = player2.play_card()
```

3. **Add the cards in the correct order to the round-winner's hand**.
```
    if p1 > p2:
            player1.add_cards([p1, p2])
        else:
            player2.add_cards([p2, p1])
```

4. **The winner will be the only player with cards left at the end**, and the `Player.count_score()` convenience method makes finding Part 1's answer a breeze.
```
winner = player1 if player1.has_cards() else player2

print("Part 1: {0}\n\n".format(winner.count_score()))
```

## Part 2
>--- Part Two ---
>
>You lost to the small crab! Fortunately, crabs aren't very good at recursion. To defend your honor as a Raft Captain, you challenge the small crab to a game of Recursive Combat.
>
>Recursive Combat still starts by splitting the cards into two decks (you offer to play with the same starting decks as before - it's only fair). Then, the game consists of a series of rounds with a few changes:
>
>- Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1. Previous rounds from other games are not considered. (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
>- Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing the top card of their deck as normal.
>- If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing a new game of Recursive Combat (see below).
>- Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.
>
>As in regular Combat, the winner of the round (even if they won the round by winning a sub-game) takes the two cards dealt at the beginning of the round and places them on the bottom of their own deck (again so that the winner's card is above the other card). Note that the winner's card might be the lower-valued of the two cards if they won the round due to winning a sub-game. If collecting cards by winning the round causes a player to have all of the cards, they win, and the game ends.
>
>Here is an example of a small game that would loop forever without the infinite game prevention rule:
>```
>Player 1:
>43
>19
>
>Player 2:
>2
>29
>14
>```
>During a round of Recursive Combat, if both players have at least as many cards in their own decks as the number on the card they just dealt, the winner of the round is determined by recursing into a sub-game of Recursive Combat. (For example, if player 1 draws the 3 card, and player 2 draws the 7 card, this would occur if player 1 has at least 3 cards left and player 2 has at least 7 cards left, not counting the 3 and 7 cards that were drawn.)
>
>To play a sub-game of Recursive Combat, each player creates a new deck by making a copy of the next cards in their deck (the quantity of cards copied is equal to the number on the card they drew to trigger the sub-game). During this sub-game, the game that triggered it is on hold and completely unaffected; no cards are removed from players' decks to form the sub-game. (For example, if player 1 drew the 3 card, their deck in the sub-game would be copies of the next three cards in their deck.)
>
>Here is a complete example of gameplay, where Game 1 is the primary game of Recursive Combat:
>```
>=== Game 1 ===
>
>-- Round 1 (Game 1) --
>Player 1's deck: 9, 2, 6, 3, 1
>Player 2's deck: 5, 8, 4, 7, 10
>Player 1 plays: 9
>Player 2 plays: 5
>Player 1 wins round 1 of game 1!
>
>-- Round 2 (Game 1) --
>Player 1's deck: 2, 6, 3, 1, 9, 5
>Player 2's deck: 8, 4, 7, 10
>Player 1 plays: 2
>Player 2 plays: 8
>Player 2 wins round 2 of game 1!
>
>-- Round 3 (Game 1) --
>Player 1's deck: 6, 3, 1, 9, 5
>Player 2's deck: 4, 7, 10, 8, 2
>Player 1 plays: 6
>Player 2 plays: 4
>Player 1 wins round 3 of game 1!
>
>-- Round 4 (Game 1) --
>Player 1's deck: 3, 1, 9, 5, 6, 4
>Player 2's deck: 7, 10, 8, 2
>Player 1 plays: 3
>Player 2 plays: 7
>Player 2 wins round 4 of game 1!
>
>-- Round 5 (Game 1) --
>Player 1's deck: 1, 9, 5, 6, 4
>Player 2's deck: 10, 8, 2, 7, 3
>Player 1 plays: 1
>Player 2 plays: 10
>Player 2 wins round 5 of game 1!
>
>-- Round 6 (Game 1) --
>Player 1's deck: 9, 5, 6, 4
>Player 2's deck: 8, 2, 7, 3, 10, 1
>Player 1 plays: 9
>Player 2 plays: 8
>Player 1 wins round 6 of game 1!
>
>-- Round 7 (Game 1) --
>Player 1's deck: 5, 6, 4, 9, 8
>Player 2's deck: 2, 7, 3, 10, 1
>Player 1 plays: 5
>Player 2 plays: 2
>Player 1 wins round 7 of game 1!
>
>-- Round 8 (Game 1) --
>Player 1's deck: 6, 4, 9, 8, 5, 2
>Player 2's deck: 7, 3, 10, 1
>Player 1 plays: 6
>Player 2 plays: 7
>Player 2 wins round 8 of game 1!
>
>-- Round 9 (Game 1) --
>Player 1's deck: 4, 9, 8, 5, 2
>Player 2's deck: 3, 10, 1, 7, 6
>Player 1 plays: 4
>Player 2 plays: 3
>Playing a sub-game to determine the winner...
>
>=== Game 2 ===
>
>-- Round 1 (Game 2) --
>Player 1's deck: 9, 8, 5, 2
>Player 2's deck: 10, 1, 7
>Player 1 plays: 9
>Player 2 plays: 10
>Player 2 wins round 1 of game 2!
>
>-- Round 2 (Game 2) --
>Player 1's deck: 8, 5, 2
>Player 2's deck: 1, 7, 10, 9
>Player 1 plays: 8
>Player 2 plays: 1
>Player 1 wins round 2 of game 2!
>
>-- Round 3 (Game 2) --
>Player 1's deck: 5, 2, 8, 1
>Player 2's deck: 7, 10, 9
>Player 1 plays: 5
>Player 2 plays: 7
>Player 2 wins round 3 of game 2!
>
>-- Round 4 (Game 2) --
>Player 1's deck: 2, 8, 1
>Player 2's deck: 10, 9, 7, 5
>Player 1 plays: 2
>Player 2 plays: 10
>Player 2 wins round 4 of game 2!
>
>-- Round 5 (Game 2) --
>Player 1's deck: 8, 1
>Player 2's deck: 9, 7, 5, 10, 2
>Player 1 plays: 8
>Player 2 plays: 9
>Player 2 wins round 5 of game 2!
>
>-- Round 6 (Game 2) --
>Player 1's deck: 1
>Player 2's deck: 7, 5, 10, 2, 9, 8
>Player 1 plays: 1
>Player 2 plays: 7
>Player 2 wins round 6 of game 2!
>The winner of game 2 is player 2!
>
>...anyway, back to game 1.
>Player 2 wins round 9 of game 1!
>
>-- Round 10 (Game 1) --
>Player 1's deck: 9, 8, 5, 2
>Player 2's deck: 10, 1, 7, 6, 3, 4
>Player 1 plays: 9
>Player 2 plays: 10
>Player 2 wins round 10 of game 1!
>
>-- Round 11 (Game 1) --
>Player 1's deck: 8, 5, 2
>Player 2's deck: 1, 7, 6, 3, 4, 10, 9
>Player 1 plays: 8
>Player 2 plays: 1
>Player 1 wins round 11 of game 1!
>
>-- Round 12 (Game 1) --
>Player 1's deck: 5, 2, 8, 1
>Player 2's deck: 7, 6, 3, 4, 10, 9
>Player 1 plays: 5
>Player 2 plays: 7
>Player 2 wins round 12 of game 1!
>
>-- Round 13 (Game 1) --
>Player 1's deck: 2, 8, 1
>Player 2's deck: 6, 3, 4, 10, 9, 7, 5
>Player 1 plays: 2
>Player 2 plays: 6
>Playing a sub-game to determine the winner...
>
>=== Game 3 ===
>
>-- Round 1 (Game 3) --
>Player 1's deck: 8, 1
>Player 2's deck: 3, 4, 10, 9, 7, 5
>Player 1 plays: 8
>Player 2 plays: 3
>Player 1 wins round 1 of game 3!
>
>-- Round 2 (Game 3) --
>Player 1's deck: 1, 8, 3
>Player 2's deck: 4, 10, 9, 7, 5
>Player 1 plays: 1
>Player 2 plays: 4
>Playing a sub-game to determine the winner...
>
>=== Game 4 ===
>
>-- Round 1 (Game 4) --
>Player 1's deck: 8
>Player 2's deck: 10, 9, 7, 5
>Player 1 plays: 8
>Player 2 plays: 10
>Player 2 wins round 1 of game 4!
>The winner of game 4 is player 2!
>
>...anyway, back to game 3.
>Player 2 wins round 2 of game 3!
>
>-- Round 3 (Game 3) --
>Player 1's deck: 8, 3
>Player 2's deck: 10, 9, 7, 5, 4, 1
>Player 1 plays: 8
>Player 2 plays: 10
>Player 2 wins round 3 of game 3!
>
>-- Round 4 (Game 3) --
>Player 1's deck: 3
>Player 2's deck: 9, 7, 5, 4, 1, 10, 8
>Player 1 plays: 3
>Player 2 plays: 9
>Player 2 wins round 4 of game 3!
>The winner of game 3 is player 2!
>
>...anyway, back to game 1.
>Player 2 wins round 13 of game 1!
>
>-- Round 14 (Game 1) --
>Player 1's deck: 8, 1
>Player 2's deck: 3, 4, 10, 9, 7, 5, 6, 2
>Player 1 plays: 8
>Player 2 plays: 3
>Player 1 wins round 14 of game 1!
>
>-- Round 15 (Game 1) --
>Player 1's deck: 1, 8, 3
>Player 2's deck: 4, 10, 9, 7, 5, 6, 2
>Player 1 plays: 1
>Player 2 plays: 4
>Playing a sub-game to determine the winner...
>
>=== Game 5 ===
>
>-- Round 1 (Game 5) --
>Player 1's deck: 8
>Player 2's deck: 10, 9, 7, 5
>Player 1 plays: 8
>Player 2 plays: 10
>Player 2 wins round 1 of game 5!
>The winner of game 5 is player 2!
>
>...anyway, back to game 1.
>Player 2 wins round 15 of game 1!
>
>-- Round 16 (Game 1) --
>Player 1's deck: 8, 3
>Player 2's deck: 10, 9, 7, 5, 6, 2, 4, 1
>Player 1 plays: 8
>Player 2 plays: 10
>Player 2 wins round 16 of game 1!
>
>-- Round 17 (Game 1) --
>Player 1's deck: 3
>Player 2's deck: 9, 7, 5, 6, 2, 4, 1, 10, 8
>Player 1 plays: 3
>Player 2 plays: 9
>Player 2 wins round 17 of game 1!
>The winner of game 1 is player 2!
>
>
>== Post-game results ==
>Player 1's deck: 
>Player 2's deck: 7, 5, 6, 2, 4, 1, 10, 8, 9, 3
>```
>After the game, the winning player's score is calculated from the cards they have in their original deck using the same rules as regular Combat. In the above game, the winning player's score is 291.
>
>Defend your honor as Raft Captain by playing the small crab in a game of Recursive Combat using the same two decks as before. What is the winning player's score?
>
>Your puzzle answer was **31657**.

The make-a-copy-of-your-hand and the limit-the-hand-size-based-on-the-dealt-card twists necessitated a few more convenience methods on my `Player` class:

- A `count_cards` method to determine how much to truncate the hands for recrusive games
```
def count_cards(self):
    return len(self.cards)
```

- A `get_hand_state` method that was used to (A) prevent infinite loops and to (B) build out a cache to shorten the runtime
```
def get_hand_state(self):
    return self.name.replace(" ","") + ":" + ",".join(list(map(str,self.cards)))
```

- And a couple of `copy` methods to handle not mutating the Players themselves when kicking off recursive games
```
def copy(self):
    return Player(self.name, self.cards.copy())

def copy_and_trim(self, size):
        cards = self.cards[0:size]
        return Player(self.name,cards)
```

In my `run_program` method, I now passed in _copies_ of my `Player` instances to prevent mutation between the parts:
```
calculate_part1(player1.copy(), player2.copy(), debug)
calculate_part2(player1.copy(), player2.copy(), debug)
```

Then, I moved the game logic to its own method `play_game` so that I could call it recursively:
```
def calculate_part2(player1, player2, debug=False):
    winner = play_game(player1, player2, {}, debug)

    print("Part 2: {0}\n\n".format(winner.count_score()))
    return 
```

This `play_game` method had the same while-players-have-cards loop as Part 1:
```
while player1.has_cards() and player2.has_cards():
```

However, its first order of business was to check for an infinite loop:
```
    # check for infinite loop
    round = player1.get_hand_state() + "|" + player2.get_hand_state()
    if round in past_rounds:
        return player1
    else:
        past_rounds.append(round)
```

Then, as in Part 1, it played the top cards:
```
    p1 = player1.play_card()
    p2 = player2.play_card()
```

However, before checking which card is higher, it first checks to see if the card counts mandate a recursive round. Otherwise, it follows normal gameplay:
```
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
```

And then as before, if the while-loop completes, it declares the winner to be whoever still has cards:
```
winner = player1 if player1.has_cards() else player2
```

I got a little caught up at first on where to include the no-infinite-loop check because my initial plan, which was to not pass the list along to recursive checks, _did_ result in the right answer for the sample data but the real data seemed to run _forever_, which worried me that I may have hit an infinite loop. However, after playing around a little and re-reading the problem more carefully (noting their deliberate uses of "game" and "round"), I realized my first instinct was correct.

So why was the real answer taking so long?

To try and speed things up, I added a caching check at the beginning of each _game_. I created a dictionary which I _did_ pass between recursive games where the key was the starting round and the value was the ultimate winner of this round. 

I updated my `play_game` method to take a `round_outcomes` parameter, and at the beginning of this method I added:
```
starting_round = player1.get_hand_state() + "|" + player2.get_hand_state()

# check for cache hits
if starting_round in round_outcomes:
    return round_outcomes[starting_round]
```

Then, at the infinite-loop conditional block and at the end of the method, I added an entry to this cache:
```
if round in past_rounds:
    round_outcomes[starting_round] = player1
    return player1
```
```
# add outcome to cache to save time later
round_outcomes[starting_round] = winner
```

A little debugging confirmed that this caching _was_ being hit regularly, and I was happy to see that I got the Part 2 answer in a matter of seconds (that is, _much_ more quickly) with this new caching added.