class CustomsFormAnswers:
    def __init__(self, answer_list=[]):
        self.answer_list = answer_list
        self.response_dict = {}
        self.num_respondents = 0

        # for each group member's answer, update the response dict
        for answer in answer_list:
            self.num_respondents += 1
            # for each specific answer, increment the question's yes count
            for question in answer:
                yes_count = 1
                if question in self.response_dict.keys():
                    yes_count += self.response_dict[question]
                self.response_dict[question] = yes_count
    
    def get_any_yes_count(self):
        return len(self.response_dict)
    
    def get_all_yes_count(self):
        all_yes_count = 0
        for key in self.response_dict:
            if self.response_dict[key] == self.num_respondents:
                all_yes_count += 1
        return all_yes_count
    
    def print(self):
        print("Number of any yes answers: " + str(self.get_any_yes_count()))
        print("Number of all yes answers: " + str(self.get_all_yes_count()))

def read_file(input_file):
    file = open(input_file,"r")

    all_answers = []
    group_answers = []
    for line in file:
        if not line.rstrip():
            # blank line means we're done with a group

            # only add if the group had answers
            if len(group_answers) > 0:
                group = CustomsFormAnswers(group_answers)
                all_answers.append(group)

                # reset group answers
                group_answers = []
        
        else:
            #parse the line into a new answer
            group_answers.append(line.strip())
            print("Added: " + line.rstrip())
    
    # add final entry, if necessary
    if len(group_answers) > 0:
        group = CustomsFormAnswers(group_answers)
        all_answers.append(group)

        # reset group answers
        group_answers = []

    file.close()
    return all_answers

def sum_yes_answers(answers, require_all):
    yes_sum = 0
    for answer in all_answers:
        if require_all:
            yes_sum += answer.get_all_yes_count()
        else:
            yes_sum += answer.get_any_yes_count()
    
    print("Total yes answers: " + str(yes_sum))
    return yes_sum


all_answers = read_file("day06_real.txt")
sum_yes_answers(all_answers, True)