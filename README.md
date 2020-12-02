# adventofcode
## What is this?
This is a repository that contains code for solving the [Advent of Code 2020 challenges](https://adventofcode.com/2020/day/1).

## Setup
To set up Python in a Windows 10 VS Code environment, [follow these instructions](https://code.visualstudio.com/docs/python/python-tutorial).

## The challenges

### Day 1
I chose to use Python because I haven't used it in 16 years (2004!!) and everybody seems to love it these days. Turns out, I still dislike loosely typed languages. Additionally, the fact that the built-in `sort()` method mutates the object it's used on instead of returning a copy also threw me for a loop. [Thank goodness for stackoverflow and the time and head-bangings it saves](https://stackoverflow.com/questions/7301110/why-does-return-list-sort-return-none-not-the-list).

I wavered between using a dictionary/hashmap data structure, where I could calculate the expected addend and do a lookup, versus iterating through loops and risking worst-case O(n<sup>2</sup>) performance. Ultimately, I opted for the loops if only because I was re-learning Python on the fly and I wanted to go to bed on time.

The general approach I took was as follows:
- Sort the inputs (as one should usually do in these kinds of problems...)
- Start a loop that increments from the front
- Nest a loop that decrements from the back
- Break the loop if we're already below 2020 (because all the decrementing-from-the-back is just a waste of time at that point)
- Return the product if we get two numbers that sum to 2020

The downside of this approach is obviously the runtime -- worst case scenario, the list is full of a bunch of close, high numbers. The upside of this approach revealed itself for part 2, where we were asked to find _three entries_ that sum up to 2020. It was easy to modify my approach to have a third nested loop (yikes @ performance) with a few checks to avoid going through the loops unnecessarily; for example:
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