# [Day 1: Report Repair](https://adventofcode.com/2020/day/1)
> --- Day 1: Report Repair ---
>
> After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.
>
> The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.
>
> To save your vacation, you need to get all fifty stars by December 25th.
>
> Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

I chose to use Python because I haven't used it in 16 years (2004!!) and everybody seems to love it these days. Turns out, I still dislike dynamically typed languages. Additionally, the fact that the built-in `sort()` method mutates the object it's used on instead of returning a copy also threw me for a loop. [Thank goodness for stackoverflow and the time and head-bangings it saves](https://stackoverflow.com/questions/7301110/why-does-return-list-sort-return-none-not-the-list).

## Part 1
> Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.
>
> Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
>
> For example, suppose your expense report contained the following:
>
>- 1721
>- 979
>- 366
>- 299
>- 675
>- 1456
>
> In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.
>
> Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
>
> Your puzzle answer was **633216**.

I wavered between using a dictionary/hashmap data structure, where I could calculate the expected addend and do a lookup, versus iterating through loops and risking worst-case O(n<sup>2</sup>) performance. Ultimately, I opted for the loops if only because I was re-learning Python on the fly and I wanted to go to bed on time.

The general approach I took was as follows:
- Sort the inputs (as one should usually do in these kinds of problems...)
- Start a loop that increments from the front
- Nest a loop that decrements from the back
- Break the loop if we're already below 2020 (because all the decrementing-from-the-back is just a waste of time at that point)
- Return the product if we get two numbers that sum to 2020

The downside of this approach is obviously the runtime -- worst case scenario, the list is full of a bunch of close, high numbers. The upside of this approach revealed itself for part 2, where we were asked to find _three entries_ that sum up to 2020. 

## Part 2
> --- Part Two ---
>
> The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.
>
> Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.
>
> In your expense report, what is the product of the three entries that sum to 2020?
>
> Your puzzle answer was **68348924**.

It was easy to modify my approach to have a third nested loop (yikes @ performance) with a few checks to avoid going through the loops unnecessarily; for example:
- Skip the middle loop if the first two loops already sum above 2020
- Break out of both the second and third loops if the sums drop below 2020 (because in this case you'll need to increment the lowest value no matter what)
- Determine the range for the most-nested loop by always putting its range between the indices of the first and second loop so that we can prevent double-counting

There's probably a few edge cases I didn't account for (like the upper bound going below the lower bound), but _c'est la vie_.

**UPDATE:** My spouse guilted me into rewriting this for performance (or rather, he showed me his super fast C version which made me jealous). I improved the runtime by replacing the middle loop with a lookup. The changes were as follows:
- Create a dictionary ([super easy, it turns out -- thanks stackoverflow](https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary)) that includes keys for all the entries where their values are the number of times those entries appear in the list
- Replace the middle loop with a check to calculate the desired addend by adding the current lower and upper values and subtracting those from 2020
- Check to see if the desired addend is in the dictionary -- if so, return the product
- Remove superfluous checks

I think the lesson here is to be mildly competitive and to marry someone in the same field as you who will make you always strive to write better code. 