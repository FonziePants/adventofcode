# [Day 11: Seating System](https://adventofcode.com/2020/day/11)
>--- Day 11: Seating System ---
>
>Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!
>
>By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).
>
>The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:
>```
>L.LL.LL.LL
>LLLLLLL.LL
>L.L.L..L..
>LLLL.LL.LL
>L.LL.LL.LL
>L.LLLLL.LL
>..L.L.....
>LLLLLLLLLL
>L.LLLLLL.L
>L.LLLLL.LL
>```
>Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:
>
>- If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
>- If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
>- Otherwise, the seat's state does not change.
>
>Floor (.) never changes; seats don't move, and nobody sits on the floor.
>
>After one round of these rules, every seat in the example layout becomes occupied:
>```
>#.##.##.##
>#######.##
>#.#.#..#..
>####.##.##
>#.##.##.##
>#.#####.##
>..#.#.....
>##########
>#.######.#
>#.#####.##
>```
>After a second round, the seats with four or more occupied adjacent seats become empty again:
>```
>#.LL.L#.##
>#LLLLLL.L#
>L.L.L..L..
>#LLL.LL.L#
>#.LL.LL.LL
>#.LLLL#.##
>..L.L.....
>#LLLLLLLL#
>#.LLLLLL.L
>#.#LLLL.##
>```
>This process continues for three more rounds:
>```
>#.##.L#.##
>#L###LL.L#
>L.#.#..#..
>#L##.##.L#
>#.##.LL.LL
>#.###L#.##
>..#.#.....
>#L######L#
>#.LL###L.L
>#.#L###.##
>#.#L.L#.##
>#LLL#LL.L#
>L.L.L..#..
>#LLL.##.L#
>#.LL.LL.LL
>#.LL#L#.##
>..L.L.....
>#L#LLLL#L#
>#.LLLLLL.L
>#.#L#L#.##
>#.#L.L#.##
>#LLL#LL.L#
>L.#.L..#..
>#L##.##.L#
>#.#L.LL.LL
>#.#L#L#.##
>..L.L.....
>#L#L##L#L#
>#.LLLLLL.L
>#.#L#L#.##
>```
>At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

I was mildly interested when I saw this puzzle...

- 😃 I get to read in data that's more interesting than integer lists!
- 🙄 I have to iterate through 2D arrays (unless I make some custom node classes), and iteration is always prone to the most annoying of problems

## Part 1
>Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
>
>Your puzzle answer was **2424**.

This part didn't require too much thought. The steps:

1. Ingest a file and store the characters in a 2D array
2. Optionally, create a class to store the character mappings in case they ever change
3. Create convenience methods for copying and printing 2D arrays
4. Create a convenience method that returns the number of occupied neighboring seats. First, it needs to check the bounds in case we are at the edge of the seating area:
```
def count_neighboring_occupied_seats(seat_map,row,col):
    occupied_seat_count = 0

    top_bound = -1
    bottom_bound = 2
    left_bound = -1
    right_bound = 2

    if row == 0:
        top_bound = 0
    if row == len(seat_map)-1:
        bottom_bound = 1
    if col == 0:
        left_bound = 0
    if col == len(seat_map[row])-1:
        right_bound = 1
```
...and then it iterates through each spot that is +/- 1 from the seat whose neighbors we're checking:
```
    for r in range(top_bound,bottom_bound):
        for c in range(left_bound,right_bound):
            # don't check yourself
            if r == 0 and c == 0:
                continue

            if seat_map[row+r][col+c] == Constants.OCCUPIED:
                occupied_seat_count += 1
```
5. Create an `execute_seating_round` method that iterates through all the spots one by one, and:
  a. If the spot is already occupied but has more than four neighbors, flips it to empty
  b. If the spot is empty and there are no neighbors, flips it to occupied
6. Make sure the above method tracks if the map is every changed from the beginning through the end of the execution
7. Lastly, run the execute method (I used a `while True` loop) until the map has not changed.

Note: I skipped step 3 at first and then was annoyed to realize my seat maps were mutating...

## Part 2
>--- Part Two ---
>
>As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!
>
>Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:
>```
>.......#.
>...#.....
>.#.......
>.........
>..#L....#
>....#....
>.........
>#........
>...#.....
>```
>The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:
>```
>.............
>.L.L.#.#.#.#.
>.............
>```
>The empty seat below would see no occupied seats:
>```
>.##.##.
>#.#.#.#
>##...##
>...L...
>##...##
>#.#.#.#
>.##.##.
>```
>Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.
>
>Given the same starting layout as above, these new rules cause the seating area to shift around as follows:
>```
>L.LL.LL.LL
>LLLLLLL.LL
>L.L.L..L..
>LLLL.LL.LL
>L.LL.LL.LL
>L.LLLLL.LL
>..L.L.....
>LLLLLLLLLL
>L.LLLLLL.L
>L.LLLLL.LL
>#.##.##.##
>#######.##
>#.#.#..#..
>####.##.##
>#.##.##.##
>#.#####.##
>..#.#.....
>##########
>#.######.#
>#.#####.##
>#.LL.LL.L#
>#LLLLLL.LL
>L.L.L..L..
>LLLL.LL.LL
>L.LL.LL.LL
>L.LLLLL.LL
>..L.L.....
>LLLLLLLLL#
>#.LLLLLL.L
>#.LLLLL.L#
>#.L#.##.L#
>#L#####.LL
>L.#.#..#..
>##L#.##.##
>#.##.#L.##
>#.#####.#L
>..#.#.....
>LLL####LL#
>#.L#####.L
>#.L####.L#
>#.L#.L#.L#
>#LLLLLL.LL
>L.L.L..#..
>##LL.LL.L#
>L.LL.LL.L#
>#.LLLLL.LL
>..L.L.....
>LLLLLLLLL#
>#.LLLLL#.L
>#.L#LL#.L#
>#.L#.L#.L#
>#LLLLLL.LL
>L.L.L..#..
>##L#.#L.L#
>L.L#.#L.L#
>#.L####.LL
>..#.#.....
>LLL###LLL#
>#.LLLLL#.L
>#.L#LL#.L#
>#.L#.L#.L#
>#LLLLLL.LL
>L.L.L..#..
>##L#.#L.L#
>L.L#.LL.L#
>#.LLLL#.LL
>..#.L.....
>LLL###LLL#
>#.LLLLL#.L
>#.L#LL#.L#
>```
>Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.
>
>Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?
>
>Your puzzle answer was **2208**.

At first, I was excited by the fact I could get away with reusing my `execute_seating_round` by changing the four-max-neighbor check into a `threshold` variable to be passed in, as well as by changing the method to "count occupied seats" based on a boolean parameter `only_neighbors`. Then, all I needed to do was to create that new method that calculates surrounding occupany by line of sight instead of by proximity.

I didn't read the instructions well enough the first time around and missed the requirement that you didn't need to look at the entire row or column or whatever but at the nearest seat to you -- either empty or occupied. So, I wrote an elegant solution that checked row and column indices to intuit whether or not a seat was in someone's line of sight. I was most proud of the formulas for diagonal elements:
- positive slope: `row_0 - row_1 = col_0 - col_1`
- negative slope: `row_0 + col_0 = row_1 + col_1`

When I realized the error of my ways, I had to trash my smaller, cleaner code in favor of (where "favor" is used loosely...) eight for-loops (one for each direction). Each direction for-loop looked something like this:
```
# check row (to left)
for c_index in reversed(range(0,col)):
    if seat_map[row][c_index] == Constants.OCCUPIED:
        occupied_seat_count += 1
        break
    elif seat_map[row][c_index] == Constants.EMPTY:
        break
```

Easy peasy, right? WRONG!! Because I copied and pasted and then modified each of these loops, I was bound to make a transcription error, and boy I did. This shouldn't have been a problem because ideally I would have caught the issue while testing the sample data.

Unfortunately, my bugged program _worked successfully_ on the sample data, so when I moved onto the real data and it inexplicably failed, I was at a loss for why.

Luckily, my cats' step-father had already solved the problem, so he sent me over his data and the first partially-empty iteration so that I could run his data in my program and compare the iterations. 

The discrepancy manifested at the bottom of the map. For example, the left bottom corner looked like this on the accurately executed map:
```
   0 1 2   0 1 2   0 1 2
94 L L L → # # # → L L L
95 L L L → # # # → L L L
96 L L L → # # # → L L L
97 L L L → # # # → # L L
98 L . L → # . # → # . L
```

But mine looked like this:
```
   0 1 2   0 1 2   0 1 2
94 L L L → # # # → L L L
95 L L L → # # # → # L L
96 L L L → # # # → # L L
97 L L L → # # # → # L L
98 L . L → # . # → # . L
```

At first, I started examing (0,96) as it was the first from the bottom to have an incorrect value. I compared it to the one below, and the only difference was that _it_ didn't have floor in its bottom-right, which made me assume that the problem was with my diagonal calculations. I manually reviewed that part of the code with a pencil and paper, but saw no issues.

_Then_, I considered that (0,95) _also_ was wrongly marked but _not_ (0,94) -- here, the only difference I could think of was the column. Looking at the column data, I quickly saw my mistake:
```
    # check col (below)
    for r_index in range(row+1,len(seat_map[row])):
```

I had copied my column-checking logic from my row-checking logic, and I had correctly made all of the changes besides the for-loop's range: `len(seat_map[row])` only needed to be `len(seat_map)` when iterating through rows. The reason the test data had worked was because it was a square, whereas the real data was a rectangle with different heights and widths.

I fixed this issue throughout the the 6 checks affected by it, and my code finally worked. 😌