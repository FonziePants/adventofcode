# --- Day 7: Handy Haversacks ---

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
    
    def is_innermost(self):
        return len(self.inner_bags) == 0
    
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



def read_file(input_file):
    file = open(input_file, "r")

    bag_dict = {}

    for line in file:
        # skip if the line is empty
        if not line.rstrip():
            print("WARNING: empty line")
            continue

        # don't worry about pluralization or punctuation
        cleaned_line = (line.rstrip()
                            .lower()
                            .replace("bags","bag")
                            .replace(".","")
                            .replace(",",""))
        
        line_halves = cleaned_line.split(" bag contain")

        if len(line_halves) < 2:
            print("WARNING: line was malformatted")
            continue

        outer_bag_color = line_halves[0]
        if outer_bag_color not in bag_dict:
            bag_dict[outer_bag_color] = Bag(outer_bag_color)
        
        if "no other" in line_halves[1]:
            continue

        for rule in (line_halves[1]).split(" bag"):
            if not rule.rstrip():
                continue

            count = parse_first_int(rule)
            inner_bag_color = rule.replace(" {0} ".format(count),"")

            if inner_bag_color not in bag_dict:
                new_bag = Bag(inner_bag_color)
                bag_dict[inner_bag_color] = new_bag

            bag_dict[inner_bag_color].add_outer_bag(outer_bag_color)
            bag_dict[outer_bag_color].add_rule(inner_bag_color, count)

    file.close()

    return bag_dict

def parse_first_int(string_with_int):
    segments = string_with_int.split()
    for segment in segments:
        number = 0
        multiplier = 1
        for char in reversed(segment):
            if not char.isdigit():
                break
            number += int(char) * multiplier
            multiplier *= 10
        return number

def count_unique_outer_bag_colors(bag_dict, inner_bag_color):
    unique_outer_bags = []
    outer_bags_to_check = bag_dict[inner_bag_color].outer_bags

    while(True):
        if len(outer_bags_to_check) == 0:
            break

        outer_bags = outer_bags_to_check
        outer_bags_to_check = []
        for outer_bag in outer_bags:
            # add the outer bag if it hasn't been already
            if outer_bag not in unique_outer_bags:
                unique_outer_bags.append(outer_bag)

            # check if any outer bag's have their own outer bags to check
            for outer_outer_bag in bag_dict[outer_bag].outer_bags:
                if outer_outer_bag not in unique_outer_bags:
                    outer_bags_to_check.append(outer_outer_bag)
    
    print("A {0} bag can be inside {1} different bag types.".format(inner_bag_color, len(unique_outer_bags)))
    return len(unique_outer_bags)

def recursively_get_inner_bag_count(bag_dict, parent_bag_color):
    if bag_dict[parent_bag_color].is_innermost():
        return 0
    
    bag_count = 0
    for inner_bag_color in bag_dict[parent_bag_color].inner_bags:
        count_for_color = bag_dict[parent_bag_color].inner_bags[inner_bag_color]
        inner_bags_for_color = recursively_get_inner_bag_count(bag_dict, inner_bag_color)
        bag_count += count_for_color * (inner_bags_for_color + 1)

    return bag_count

def count_required_inner_bags(bag_dict, bag_color):
    count = recursively_get_inner_bag_count(bag_dict, bag_color)
    print("A {0} bag have {1} inner bags.".format(bag_color, count))
    return count

bag_dict = read_file("day07_real.txt")

# for color in bag_dict:
#     bag_dict[color].print()

count_unique_outer_bag_colors(bag_dict, "shiny gold")
count_required_inner_bags(bag_dict, "shiny gold")