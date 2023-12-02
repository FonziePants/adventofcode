class Node:
    def __init__(self,value,prev,next):
        self.value = value
        self.prev = prev
        self.next = next

class LinkedList:
    def __init__(self,starting,max):
        self.nodes = {}
        self.start = None
        highest = -1
        prev = None
        for character in starting:
            num = int(character)
            if num > highest:
                highest = num
            node = Node(num,prev,None)
            if self.start == None:
                self.start = node
            if prev:
                prev.next = node
            self.nodes[num] = node
            prev = node
        
        for i in range(highest,max):
            node = Node(i+1,prev,None)
            if prev:
                prev.next = node
            self.nodes[node.value] = node
            prev = node
        
        prev.next = self.start
        self.start.prev = prev
    
def pop_three(prev):
    first = prev.next
    third = first.next.next
    fourth = third.next
    prev.next = fourth
    fourth.prev = prev
    third.next = None
    return first

def insert_three(prev,first):
    third = first.next.next
    fourth = prev.next
    third.next = fourth
    fourth.prev = third
    prev.next = first
    first.prev = prev

def round(data,lowest, highest):
    pickup = data[1:4]
    data = data[0] + data[4:]
    destination = int(data[0])-1

    while str(destination) not in data:
        destination -= 1
        if destination < lowest:
            destination = highest
    
    index = data.index(str(destination)) + 1
    if index >= len(data):
        data += pickup
    else:
        data = data[0:index] + pickup + data[index:]
    
    data = data[1:] + data[0]
    
    return data

def calculate_part1(data,debug=False): 
    rounds = 100 
    highest = -1
    lowest = 100
    for c in data:
        n = int(c)
        if n > highest:
            highest = n
        elif n < lowest:
            lowest = n

    for i in range(rounds):
        print("{0}: {1}\n\n".format(i+1,data))
        data = round(data,lowest,highest)
    
    for i in range(rounds):
        data = data[-1:] + data[0:-1]

    print("Part 1: {0}\n\n".format(data))
    return

def calculate_part2(data,debug=False):
    rounds = 10000000
    max = 1000000
    
    data = LinkedList(data,max)
    
    node = data.start
    for i in range(rounds):
        popped = pop_three(node)
        dest = node.value-1

        if dest == 0:
            dest = max

        values = [popped.value, popped.next.value, popped.next.next.value]
        while dest in values:
            dest -= 1

            if dest < 1:
                dest = max
        
        prev = data.nodes[dest]
        insert_three(prev,popped)

        node = node.next
    
    one = data.nodes[1]
    answer = one.next.value * one.next.next.value
    print("{0} x {1} = {2}".format(one.next.value,one.next.next.value,answer))

    print("Part 2: {0}\n\n".format(answer))
    return 

def run_program(test=False):
    data = "215694783"
    if test:
        data = "389125467"

    calculate_part1(data)
    calculate_part2(data)

# run_program(True)
run_program()