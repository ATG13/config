# Question 2

teenage  = 13
adult    = 18
senior   = 60

age = str(input("What is your age? "))

if age >= senior:
    print("You are a senior citizen.")
elif age >= adult:
    print('You are a adult.')
elif age >= teenage:
    print("You are a teenager.")
else:
    print("You are a child.")