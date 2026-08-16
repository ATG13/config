# Question 4

x = str(input("Enter your basic salary:"))
if x > 20000:
    print("The Dearness Allowance is:", (50/100)*x)
    print("The House Rent Allowance is:",(50/100)*x)
elif x > 10000:
    print("The Dearness Allowance is:", (30/100)*x)
    print("The House Rent Allowance is:",(40/100)*x)
elif x > 5000:
    print("The Dearness Allowance is:", (20/100)*x)
    print("The House Rent Allowance is:",(30/100)*x)
else:
    print("The Dearness Allowance is:", (10/100)*x)
    print("The House Rent Allowance is:",(20/100)*x)