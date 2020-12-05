# [Day 5: Binary Boarding](https://adventofcode.com/2020/day/4)
>--- Day 5: Binary Boarding ---
>
>You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.
>
>You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.
>
>Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".
>
>The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.
>
>For example, consider just the first seven characters of FBFBBFFRLR:
>
>Start by considering the whole range, rows 0 through 127.
>- F means to take the lower half, keeping rows 0 through 63.
>- B means to take the upper half, keeping rows 32 through 63.
>- F means to take the lower half, keeping rows 32 through 47.
>- B means to take the upper half, keeping rows 40 through 47.
>- B keeps rows 44 through 47.
>- F keeps rows 44 through 45.
>- The final F keeps the lower of the two, row 44.
>
>The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.
>
>For example, consider just the last 3 characters of FBFBBFFRLR:
>
>- Start by considering the whole range, columns 0 through 7.
>- R means to take the upper half, keeping columns 4 through 7.
>- L means to take the lower half, keeping columns 4 through 5.
>- The final R keeps the upper of the two, column 5.
>
>So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
>
>Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.
>
>Here are some other boarding passes:
>
>- BFFFBBFRRR: row 70, column 7, seat ID 567.
>- FFFBBBFRRR: row 14, column 7, seat ID 119.
>- BBFFBBFRLL: row 102, column 4, seat ID 820.

I felt that today's challenge was a little more straightforward than the previous few because it required less formatting of the input file and largely came down to manipulating binary numbers.

I started by creating a method that converts a binary integer or string into a decimal integer. I suspected there is probably an easy python method or module that would have done this for me, but it's always fun to write your own stuff, especially for a hobby project like this. In creating this method, I learned that [python has an exponent operator](https://www.educative.io/edpresso/calculating-the-exponential-value-in-python), `**`, which is pretty neat!

Next, I created a `SeatAssignment` class that takes a row and column value and then calculates a seat ID accordingly. It also has a print convenience method which I used for verifying everything was in working order.

Then, I created a method that converts a structured 10-character seat string into a SeatAssignment instance. In the string, the first 7 characters are `F` or `B` representing the front or back rows of the plane and the last 3 characters are `R` or `L` representing the right and left seats in a specific row (i.e. the column). I did a simple character to replace to convert these characters to `0`s and `1`s and used my binary methods to get the equivalent decimal values for the rows and columns. All pretty straightforward.

Last of my preparation, I created a method to ingest an input file, parse each line into a seat assignment using the aforementioned method, and return a list of these seat assignments. At this point, I was ready to take off ✈

## Part 1
>As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
>
>Your puzzle answer was **922**.

For part 1, all I had to do was find the highest seat ID, so I wrote a method that loops through a list of seat assignments and keeps track of the highest seat is sees in a variable declared outside of the loop.

```
def find_highest_seat(seats):
    highest_seat = SeatAssignment()
    for seat in seats:
        if seat.seat_id > highest_seat.seat_id:
            highest_seat = seat
    return highest_seat
```
## Part 2
>--- Part Two ---
>
>Ding! The "fasten seat belt" signs have turned on. Time to find your seat.
>
>It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.
>
>Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.
>
>What is the ID of your seat?
>
>Your puzzle answer was **747**.

About ten years ago, I interviewed for a software internship and was asked to find the missing number in a set of numbers. If I remember correctly, I had approached this by sorting the set and by looking to see which sequential elements had a difference greater than 1. My interviewer challenged me to solve the problem by only going through the set once -- that is, to not bother sorting. He tried to give me hints like, "it's a property of the set itself." I was _so_ confused... by property, did he mean primeness? Factors? Even or odd? When I inevitably gave up, he told me that by "property of the set" he had meant "sum." To this day, I still feel annoyed that this was an interview question because:
- There is rarely only one right way to solve an engineering problem, and I don't think anyone not thinking of summing a set reflects on anyone's ability to solve typical engineering problems in acceptably performant ways.
- The summation solution itself has a pitfall: it will only work if a _single_ element in a sequence is missing. However, in most real-world scenarios, you should expect to detect and/or handle any number of missing data. So yes, the summation approach might be the most performant for that specific problem, but it doesn't extend to other related use cases in the way that sorting and using a dictionary/map would be able to.
- I stand by my opinion that his "property" ✌hint✌ was confusing and pretty much guaranteed my thought process went in the wrong direction. Summation is manipulation of a set's data -- calling it a property, while accurate, is misleading.

Needless to say, I did not get the job offer. _C'est la vie._

All that being said, though... I will never not think of this interview when asked to find a missing number in a set, so you can probably guess how I solved the problem of finding the only empty seat in a packed plane problem...

First, similarly to what I did in part 1, I stored the lowest and highest seats in a couple variables and iterated through the set of seats to find the correct values. Additionally, I had a counter for `seat_sum` (shocker, amirite?) and incremented this with the seat ID for each seat I iterated through.

Then, I looped from the lowest seat ID to the highest seat ID and summed up those seat IDs in a `total_seat_sum` variable.

Finally, I inferred the missing seat ID by looking at their difference: 
```
return total_seat_sum - seat_sum
```