def arithmetic_arranger(problems, show_answers=False):

    # Splitting the string
    for i in problems:
        broken_problem = i.split(' ')
        return broken_problem
    

# print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"])}')

print("3801      123\n-    2    +  49\n------    -----")


'''
Steps to figure this problem out
    Only one input(for now)
1) Split() the sting
2) Add space based on the number of intergers
3) Do the operation if true in mentioned
'''