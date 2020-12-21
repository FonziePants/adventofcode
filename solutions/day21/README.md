# [Day 21: Allergen Assessment](https://adventofcode.com/2020/day/21)
>--- Day 21: Allergen Assessment ---
>
>You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your journey.
>
>You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in a language you do understand. You should be able to use this information to determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.
>
>You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's ingredients list followed by some or all of the allergens the food contains.
>
>Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.
>
>For example, consider the following list of foods:
>```
>mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
>trh fvjkl sbzzf mxmxvkd (contains dairy)
>sqjhc fvjkl (contains soy)
>sqjhc mxmxvkd sbzzf (contains fish)
>```
>The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward: dairy and fish.

The past two days' Part 2s have been frustrating, and I'm actually closing in on the leaderboard, so I decided to do Day 21 before completing those. By jumping on this right away, I managed to complete both parts before my two leaderboard opponents (but have no fear -- I'm still in last place 😭).

## Part 1
>The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list. In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.
>
>Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?
>
>Your puzzle answer was **2020**.

I think everyone gets different puzzle answers, so I felt special that mine was the year. I thought today's was a lot like the Day 16 puzzle (ticket translations) where we had to collect possible pairings and whiddle them down by process of elimination.

### Recipe class and data types
While the data relationships were simple (at most one allergen per ingredient, and vice versa), the `Recipe` required having both an ingredient and allergen list. Accordingly, I made a simple class which performed the line-parsing logic in its constructor:
```
class Recipe:
    def __init__(self,line):
        parts = line.split(" (contains ")
        allergens = parts[1][0:-1].split(", ")
        
        self.ingredients = parts[0].split(" ")
        self.allergens = parts[1][0:-1].split(", ")

        self.ingredients.sort()
        self.allergens.sort()
```

For the ingredient-allergen pairings, I decided to create two maps, `ingredients` and `allergens`, which effectively store the same information (a key in `ingredients` is the ingredient name and its value is the corresponding allergen if it's been identified or otherwise `None`, and vice versa for `allergens`). I figured this would make it easier for me later to perform my process of elimination with instant lookups versus having to iterate through arrays and perform matching.

### Process of elimination

First, I created an `allergen_ingredient_map` dictionary where the key is the allergen and the value is the array of candidate ingredients. The steps to construct this were as follows:

1. **Create an `allergen_recipe_map`** (where key = allergen, value = collection of recipes with allergen) to make ingredient-gathering easier.
```
allergen_recipe_map = {}
for allergen in allergens:
    # find all recipes with the allergen
    recipes_with_allergen = []
    for recipe in recipes:
        if recipe.contains_allergen(allergen):
            recipes_with_allergen.append(recipe)
    allergen_recipe_map[allergen] = recipes_with_allergen
```

2. **Create initial lists of all possible ingredients per allergen**. In the same allergen for-loop as above:
```
# find all candidate ingredients that may have said allergen
possible_ingredients = recipes_with_allergen[0].ingredients.copy()
for r in range(1,len(recipes_with_allergen)):
    new_possible_ingredients = []
    for ingredient in possible_ingredients:
        if ingredient in recipes_with_allergen[r].ingredients and not ingredients[ingredient]:
            new_possible_ingredients.append(ingredient)
    possible_ingredients = new_possible_ingredients
```

3. **For any allergen that results in only one possible ingredient during the first pass, update the original `allergens` and `ingredients` dictionaries!** But make sure _not_ to add it to the `allergen_ingredient_map`, because that data structure is only for allergens whose ingredients are still unknown.
```
if len(possible_ingredients) == 1:
    ingredient = possible_ingredients[0]
    ingredients[ingredient] = allergen
    allergens[allergen] = ingredient
```

4. **Otherwise, add the potential ingredient list to the `allergen_ingredient_map`**, which will be whiddled down later.
```
else:
    allergen_ingredient_map[allergen] = possible_ingredients
```

5. **Repeat steps 2 & 3 (while also excluding any already-claimed ingredients) until the number of unidentified allergen-ingredient pairs drops down to zero**.
```
# go through again and remove duplicates
    while len(allergen_ingredient_map) > 0:
        new_allergen_ingredient_map = {}
        for allergen in allergen_ingredient_map:
            possible_ingredients = []
            for ingredient in allergen_ingredient_map[allergen]:
                # don't add already-claimed ingredients
                if not ingredients[ingredient]:
                    possible_ingredients.append(ingredient)
            if len(possible_ingredients) == 1:
                ingredient = possible_ingredients[0]
                ingredients[ingredient] = allergen
                allergens[allergen] = ingredient
            else:
                new_allergen_ingredient_map[allergen] = possible_ingredients
        allergen_ingredient_map = new_allergen_ingredient_map
```

### The solution
The final answer to Part 1 was as simple as looping through each ingredient and incrementing a counter for each time a recipe contains it.
```
good_ingredients_appearances = 0
    for ingredient in ingredients:
        if ingredients[ingredient]:
            continue

        for recipe in recipes:
            if recipe.contains_ingredient(ingredient):
                good_ingredients_appearances += 1
```

## Part 2
>--- Part Two ---
>
>Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient contains which allergen.
>
>In the above example:
>```
>mxmxvkd contains dairy.
>sqjhc contains fish.
>fvjkl contains soy.
>```
>Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.
>
>Time to stock your raft with supplies. What is your canonical dangerous ingredient list?
>
>Your puzzle answer was **bcdgf,xhrdsl,vndrb,dhbxtb,lbnmsr,scxxn,bvcrrfbr,xcgtv**.

After two puzzle days where I felt Parts 2 were much more complex than Parts 1, I was super excited to find that today's Part 2 was extremely simple. Because I already had stored the allergen-ingredient pairs in simple dictionaries, alphabetizing the ingredient list was extremely trivial.

1. **Alphabetize allergens**. I put the `allergens` keys in a list and ran it through `.sort()`. Easy peasy.
```
# alphabetize allergens
alphabetical_allergens = list(allergens.keys())
alphabetical_allergens.sort()
```

2. **List out ingredients with respect to alphabetized allergens**. I looped through the above sorted list and created a new list ingredient by ingredient.
```
# alphabetize ingredients
alphabetical_ingredients = []
for allergen in alphabetical_allergens:
    alphabetical_ingredients.append(allergens[allergen])
```

3. **Format it**. One line in Python, that's it.
```
",".join(alphabetical_ingredients
```

😎