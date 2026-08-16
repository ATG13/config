# Question 5

x = int(input("Enter your percentage:"))
if x >= 40:
    if x < 60:
        print("The Grade is D")
    elif x < 80:
        print("The Grade is C")
    elif x < 90:
        print("The Grade is B")
    elif x >= 90:
        print("The Grade is A")
else:
    print("The Grade is F")