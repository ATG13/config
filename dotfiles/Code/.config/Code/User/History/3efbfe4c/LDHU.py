def arithmetic_arranger(problems, show_answers=False):
    #Line strings
    l1 = ''
    l2 = ''
    l3 = ''
    l4 = ''
    #For spaces & dash in line
    space = ' '
    dash = '-'
    tab = '    '

    #ERROR for too many problems
    if len(problems) > 5:
        return 'Error: Too many problems.'
        
    #Looks at each tuple in the list
    for prob in problems:
        #Split each number and operator
        broken_problem = prob.split(' ')
        first_num = broken_problem[0]
        second_num = broken_problem[2]

        #ERROR for not digits and convert to int
        try:
            first_num = int(broken_problem[0])
            second_num = int(broken_problem[2])
        except ValueError:
            return 'Error: Numbers must only contain digits.'
        
        #ERROR max digits = 4
        if len(str(first_num)) > 4 or len(str(second_num)) > 4:
            return 'Error: Numbers cannot be more than four digits.'


        #Getting answer or raising ERROR
        if broken_problem[1] == '+':
            answer = first_num + second_num
        elif broken_problem[1] == '-':
            answer = first_num - second_num
        else:
            #ERROR for + or -
            print('Error: Operator must be '+' or '-'.')
        
        ##Creating the right output

        #l1 dash value
        if len(str(first_num)) > len(str(second_num)):
            num1_space = 2
        elif len(str(first_num)) < len(str(second_num)):
            num1_space = 2 + (len(str(second_num)) - len(str(first_num)))
        else:
            num1_space = 2
        
        #append to l1
        l1 = l1 + num1_space*space + str(first_num) + tab

        #l2 dash value
        operator = broken_problem[1]
        if len(str(first_num)) < len(str(second_num)):
            num2_space = 1
        elif len(str(first_num)) > len(str(second_num)):
            num2_space = 1 + len(str(first_num)) - len(str(second_num))
        else:
            num2_space = 1

        #append to l2
        l2 = l2 + operator + num2_space*space + str(second_num) + tab

        #l3 dash value
        num3_space = len(l2-tab)
        l3 = l3 + num3_space*dash + tab


    
    #Final output 
    if show_answers==False:
        print(l1 + '\n' + l2 + '\n' + l3 )
    elif show_answers==True:
        print(l1 + '\n' + l2 + '\n' + l3 + '\n' + l4)

    else:
        return 'Provide either True or False for show_answers'
    


def main():
    print(arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]))

main()