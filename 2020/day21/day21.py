def read_data(file_path,debug=True):
    file = open(file_path, "r")

    recipes = []
    ingredients = {}
    allergens = {}

    for line in file:
        if not line.rstrip():
            continue

        recipe = Recipe(line.rstrip())
        recipes.append(recipe)

        for ingredient in recipe.ingredients:
            if ingredient not in ingredients:
                ingredients[ingredient] = None
        
        for allergen in recipe.allergens:
            if allergen not in allergens:
                allergens[allergen] = None
    
    file.close()

    if debug:
        for recipe in recipes:
            recipe.print()
        print("INGREDIENTS: {0}".format(ingredients))
        print("ALLERGENS: {0}".format(allergens))

    return (recipes, ingredients, allergens)

class Recipe:
    def __init__(self,line):
        parts = line.split(" (contains ")
        
        self.ingredients = parts[0].split(" ")
        self.allergens = parts[1][0:-1].split(", ")

        self.ingredients.sort()
        self.allergens.sort()
    
    def contains_ingredient(self,ingredient):
        return ingredient in self.ingredients
    
    def contains_allergen(self,allergen):
        return allergen in self.allergens
    
    def print(self):
        print("RECIPE\n\tINGREDIENTS:")
        for ingredient in self.ingredients:
            print("\t\t" + ingredient)
        print("\tALLERGENS:")
        for allergen in self.allergens:
            print("\t\t" + allergen)
        print()

def calculate_part1(recipes, ingredients, allergens, debug=False):   
    allergen_recipe_map = {}
    allergen_ingredient_map = {}

    # initialize dictionaries with first pass trimming
    for allergen in allergens:
        # find all recipes with the allergen
        recipes_with_allergen = []
        for recipe in recipes:
            if recipe.contains_allergen(allergen):
                recipes_with_allergen.append(recipe)
        allergen_recipe_map[allergen] = recipes_with_allergen

        # find all candidate ingredients that may have said allergen
        possible_ingredients = recipes_with_allergen[0].ingredients.copy()
        for r in range(1,len(recipes_with_allergen)):
            new_possible_ingredients = []
            for ingredient in possible_ingredients:
                if ingredient in recipes_with_allergen[r].ingredients and not ingredients[ingredient]:
                    new_possible_ingredients.append(ingredient)
            possible_ingredients = new_possible_ingredients
        
        if len(possible_ingredients) == 1:
            ingredient = possible_ingredients[0]
            ingredients[ingredient] = allergen
            allergens[allergen] = ingredient
        else:
            allergen_ingredient_map[allergen] = possible_ingredients

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
    
    if debug:
        print("\nINGREDIENTS: {0}".format(ingredients))
        print("ALLERGENS: {0}".format(allergens))
    
    good_ingredients_appearances = 0
    for ingredient in ingredients:
        if ingredients[ingredient]:
            continue

        for recipe in recipes:
            if recipe.contains_ingredient(ingredient):
                good_ingredients_appearances += 1

    print("Part 1: {0}\n\n".format(good_ingredients_appearances))
    return

def calculate_part2(recipes, ingredients, allergens, debug=False):
    # alphabetize allergens
    alphabetical_allergens = list(allergens.keys())
    alphabetical_allergens.sort()

    # alphabetize ingredients
    alphabetical_ingredients = []
    for allergen in alphabetical_allergens:
        alphabetical_ingredients.append(allergens[allergen])
    
    if debug:
        print("Unformatted canonical dangerous ingredient list: {0}".format(alphabetical_ingredients))

    print("Part 2: {0}\n\n".format(",".join(alphabetical_ingredients)))
    return 

def run_program(test=False, debug=False):
    file_path = "day21.txt"
    if test:
        file_path = "day21_test.txt"
    
    data = read_data(file_path, debug)

    recipes = data[0]
    ingredients = data[1]
    allergens = data[2]

    calculate_part1(recipes, ingredients, allergens, debug)
    calculate_part2(recipes, ingredients, allergens, debug)

# run_program(True, True)
run_program()