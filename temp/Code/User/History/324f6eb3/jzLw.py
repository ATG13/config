def arithmetic_arranger(problems, show_answers=False):

    broken_problem = problems.split(' ')
    first_num = broken_problem[0]
    second_num = broken_problem[1]
    third_num = broken_problem[2]

    if len(first_num) < len(third_num):
        # Ex: 12 + 123
        addition = len(third_num)-len(first_num)
        first_num = ' '*(addition+2) + first_num
        print(f'{first_num}\n{second_num} {third_num}')

print(f'\n{arithmetic_arranger("32 + 698")}')

'''
Steps to figure this problem out
    Only one input(for now)
1) Split() the sting
2) Add space based on the number of intergers
3) Do the operation if true in mentioned

Output
"    32 \n + 698 \n ------"
'''