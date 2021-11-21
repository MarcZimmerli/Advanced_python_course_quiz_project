import os
import pandas as pd
user_actions = ['Add a new question to the database','Print questions & answers','Exit']
questions_answers_dict = {}

#TODO try to remove the NaN from empty initialization (if csv has to be created from scratch)
try:
    question_df = pd.read_csv('Questions_answers.csv',index_col=[0,1])
except:
    print('No existing question database detected')
    question_df = pd.DataFrame(index=[['Question'],['Options']],columns=['Is correct?'])


import os
def quit():
    global question_df
    question_df.to_csv('Questions_answers.csv')
    exit()
    

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def add_questions():
    global question_df
    clearConsole()
    question = input('Type in your new question for the quiz:\n')

    while True:
        try:
            answer_option_count = int(input('How many possible answer options would you like to add?:\n'))
            break
        except ValueError as ex:
            print(ex,'\nInvalid amount of quesitons specified')

    possible_answers = [input('Enter Option {}:\n'.format(i+1)) for i in range(answer_option_count)]
    clearConsole()
    
    print('Question:\n'+question+'\n\nFrom the given options:\n')
    for i in range(len(possible_answers)):
        print(str(i+1)+': '+possible_answers[i])
    
    while True:
        
        correct_index_str = input('\nPlease list the indices of all answers which are considered correct (separated by commas if multiple answers are correct):\n')
        if correct_index_str == '':
            answer_option_count += 1
            correct_index_list = [answer_option_count]
            possible_answers.append('None of the above')
            break
        
        try:
            correct_index_list = [int(index) for index in correct_index_str.split(',')]
        except:
            print('Solution input not recognized - either input a single integer or a list of integers separated by a comma')
            continue
        
        faulty_entries = set(correct_index_list).difference(range(1,answer_option_count+1))

        if  len(faulty_entries) != 0:
            print('Error: The given indices {} are not among the possible indices of 1-{}\n'.format(faulty_entries,answer_option_count))
            continue
        break
    
    clearConsole()
    print('Confirming new entry:\n')
    print('Question:\n' \
        +question +'\n\n'\
            +'Options:\n')
    for index, answer in enumerate(possible_answers):
        print('{}:  {}'.format(index+1,answer))
    print('Correct answers:',correct_index_list)
    
    while True:
        confirmation = input('Is this entry correct? (Y/N)\n').upper()
        if confirmation == 'N':
            clearConsole()
            print('Entry discarded - returning to main menu')
            break
        elif confirmation !='Y' and confirmation != 'N':
            print('Invalid input - please type either Y for yes or N for no')
        else:
            name = 'Question {}'.format(len(questions_answers_dict.keys()))
            questions_answers_dict[name] = (question,possible_answers,correct_index_list)
            clearConsole()
            question_df = pd.concat([question_df,question_to_df(question,possible_answers,correct_index_list)])
            print('Entry added to the database - returning to main menu')

            break

def print_questions():
    global question_df
    print(question_df)

def question_to_df(question,options,correct):
    index = pd.MultiIndex.from_product([[question],options],names=['Question','Options'])
    df = pd.DataFrame(data = [answer in correct for answer in range(1,len(options)+1)],index=index, columns=['Is correct?'])
    return df

def main():
    action_functions = [add_questions,print_questions,quit]
    def chooseAction():
        action = input('Please select your action: ')
        if not action.isdigit():
            raise TypeError('Invalid input - please type in the INTEGER corresponding to your action of choice')
        action = int(action)
        action_functions[action]()
    
    clearConsole()
    
    while True:
        print('\nWelcome to the Quiz interface\n\nWhat would you like to do?')
        for index,action in enumerate(user_actions):
            print(str(index)+': '+action)

        try:
            chooseAction()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()   