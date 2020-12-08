# [Day 7: Handy Haversacks](https://adventofcode.com/2020/day/7)
>--- Day 7: Handy Haversacks ---
>
>You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.
>
>Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!
>
>For example, consider the following rules:
>```
>light red bags contain 1 bright white bag, 2 muted yellow bags.
>dark orange bags contain 3 bright white bags, 4 muted yellow bags.
>bright white bags contain 1 shiny gold bag.
>muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
>shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
>dark olive bags contain 3 faded blue bags, 4 dotted black bags.
>vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
>faded blue bags contain no other bags.
>dotted black bags contain no other bags.
>```
>These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

I read today's problem aloud this morning while my partner and I waited for a COVID test. As I sat in the car, lamenting that it takes two hours to get a test for a disease that has been well-established for about 9 months already, I considered different approaches. At first I thought that, with bags having parent and child bags, maybe this would call for a tree or a graph? And then I considered how much I love instant lookups and how much I hate thinking about iterators and decided I would make a custom class that knows its parent's ID and its children's IDs but that I would store all unique instances of this class in a dictionary for easy lookup. Basically:

- Define a `Bag` class where its ID is its `color` (e.g. `shiny gold`)
- Store the bag's children in a dictionar where the keys are the colors (e.g. `dark olive`, `vibrant plum`) and the values are their counts (e.g. `1`, `2`)
- Store the bag's _possible_ direct parents in an array (e.g. `bright white`, `muted yellow`)
- Outside of the `Bag` class, store a dictionary where the keys are the bag colors and the values are an instance of `Bag`; this would ensure that I only have one definition and set of rules per bag color and that I can look-up a bag's rules with its color key and not need to iterate through any collections

Again, designing a data model to store the input data before thinking too much about the problem to solve helped ensure that I wouldn't cut corners to knock out Part 1 at the expense of solving the TBD Part 2.

```
class Bag:
    def __init__(self, color=None):
        self.color = color
        self.inner_bags = {}
        self.outer_bags = []
    
    def add_rule(self, inner_bag_color, num_contained):
        self.inner_bags[inner_bag_color] = num_contained
    
    def add_outer_bag(self, outer_bag_color):
        if outer_bag_color not in self.outer_bags:
            self.outer_bags.append(outer_bag_color)
```

To populate the aforementioned dictionary, I parsed the file line by line and did the following:

- Stripped each line of punctuation and replaced all instances of `"bags"` with `"bag"` so that I wouldn't need to worry about pluralization
- Split the string into two, using `" bag contain"` as the separator so that the first half would be the color of the parent bag and the second half would be a set of rules
- If the parent bag color was not already a key in the bag dictionary, I added it
- For the second half, I split the string again by `" bag"` and treated each segment as its own rule
- I created a method to parse out an integer and then I pulled the child bag color from the remaining part of the string
- For each of these child bag colors, I created the bag instance and added it to the dictionary if it wasn't already there, and then I added it as a child to the parent bag and I added the parent bag as a parent to it

## Part 1
>You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
>
>In the above rules, the following options would be available to you:
>
>- A bright white bag, which can hold your shiny gold bag directly.
>- A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
>- A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
>- A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
>
>So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
>
>How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
>
>Your puzzle answer was **124**.

Besides dealing with a bug that ate up an hour of my time, this part of the problem was straightforward. Because any instance of my `Bag` class knew who its possible parents were, all I needed to do was:
- Write a method that takes the full bag list and the color bag for which I wanted a unique ancestor count
- Pull the possible parents for that bag
- For each of these possible parents, add it to my possible-ancestor-list (i.e. `unique_outer_bags`) and then repeat the same process for all of _its_ possible ancestors
- Stop when I ran out of ancestors that weren't already in the possible-parents-list and then turn the size of that collection as the answer

### The Bug 🐛
In my file parsing, I used a custom `Bag.print()` method to print out a Bag's children and possible parents:
```
def print(self):
    print("{0} BAGS HAVE {1} INNER BAGS AND {2} OUTER BAGS:"
            .format(self.color.upper(), 
                    len(self.inner_bags), 
                    len(self.outer_bags)))
    print("  INNER BAGS:")
    for inner_bag in self.inner_bags:
        print("    - {0} {1}".format(self.inner_bags[inner_bag], inner_bag))

    print("  OUTER BAGS:")
    for outer_bag in self.outer_bags:
        print("    - {0}".format(outer_bag))
```

In doing so, I discovered that all of the bag colors listed the same exact inner and outer bags. 

At first I thought, oh, I must be storing them in the same memory slot, but a print revealed that each Bag instance had its own slot. Then I thought, maybe I'm mutating the wrong object when I try to add the rules? However, even when I had my spouse look at my code, neither of us could see where that could be happening. At last, I realized that my constructor was taking default values for the inner and outer bag collections, and these were the two properties that (A) were being shared across instances and (B) were never being passed into the constructor anyway. Removing these fixed the issue, which leads me to believe that the syntax I used to declare these default values was reusing the same empty array and empty dictionary for each new class instance.

I changed this:
```
class Bag:
    def __init__(self, color=None, inner_bags={}, outer_bags=[]):
        self.color = color
        self.inner_bags = inner_bags
        self.outer_bags = outer_bags
```

...to this:
```
class Bag:
    def __init__(self, color=None):
        self.color = color
        self.inner_bags = {}
        self.outer_bags = []
```

This fixed my issue (luckily), but I will never get that troubleshooting time back (and I ended up last in the leaderboard again 😭).

## Part 2
>--- Part Two ---
>
>It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!
>
>Consider again your shiny gold bag and the rules from the above example:
>```
>faded blue bags contain 0 other bags.
>dotted black bags contain 0 other bags.
>vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
>dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
>```
>So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!
>
>Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!
>
>Here's another example:
>```
>shiny gold bags contain 2 dark red bags.
>dark red bags contain 2 dark orange bags.
>dark orange bags contain 2 dark yellow bags.
>dark yellow bags contain 2 dark green bags.
>dark green bags contain 2 dark blue bags.
>dark blue bags contain 2 dark violet bags.
>dark violet bags contain no other bags.
>```
>In this example, a single shiny gold bag must contain 126 other bags.
>
>How many individual bags are required inside your single shiny gold bag?
>
>Your puzzle answer was **34862**.

I planned to avoid recursion but then gave up. For this one, I wrote a recursive method that did the following:

- Took a bag color and the bag dictionary from which to look up that bag's definition
- Returned `0` if the bag had zero children
- Otherwise, it summed for each child bag:
  - The total number of descendants for that child bag (as calculated by calling this recursive method on said child bag)... plus `1` for the child bag itself...
  - ...Multiplied by the number of that child bag were required by the parent
- Returned this sum

And voila! Worked like a charm. The method spit out `34862` in less than a second.

Had the performance been worse with the recursion, I would have updated it to do the following:

- Store the `total_descendant` count as a property on the `Bag` class
- If the getter was called but the property was `None`, I'd run this recursive method to get the value, assign it to the property, and then return it
- Only call this `get_total_descendant_count()` method on the bag's direct children

With this approach, I could have avoided recalculating descendants every time by storing it after that first time. However, because my performance was already snappy, I didn't bother with this optimization.

...And with that, this problem was _in the bag_ 😎