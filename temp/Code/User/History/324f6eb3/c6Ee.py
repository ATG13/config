def arithmetic_arranger(problems, show_answers=False):

    broken_problem = problems.split(' ')
    first_num = broken_problem[0]
    second_num = broken_problem[1]
    third_num = broken_problem[2]

    if len(first_num) < len(third_num):
        # Ex: 12 + 123
        addition = len(third_num) - len(first_num)
        first_num = ' ' * (addition + 2) + first_num
        dashes = '-' * (2 + len(third_num))

        if show_answers == True:
            if second_num == '+':
                answer = int(first_num) + int(third_num)

                print(f'{first_num}\n{second_num} {third_num}\n{dashes}\n  {answer}')
            elif second_num == '-':
                answer = int(first_num) - int(third_num)

                print(f'{first_num}\n{second_num} {third_num}\n{dashes}\n {answer}')
            else:
                ValueError('Invalid Syntax')
        else:
            print(f'{first_num}\n{second_num} {third_num}\n{dashes}')
    elif len(first_num) > len(third_num):
        # Ex: 123 + 12
        addition = len(first_num) - len(third_num)
        pass
    else:
        pass



print(f'\n{arithmetic_arranger("123 - 69", True)}')


'''
Perfect
Now do this for 4 or more problems, somehow
'''