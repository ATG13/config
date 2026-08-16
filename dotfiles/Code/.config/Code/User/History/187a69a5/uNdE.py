# Question 1

m1 = int(input("What is the marks of your first subject: "))
m2 = int(input("What is the marks of your second subject: "))
m3 = int(input("What is the marks of your third subject: "))
m4 = int(input("What is the marks of your fourth subject: "))
m5 = int(input("What is the marks of your fifth subject: "))

tot = m1+m2+m3+m4+m5
avg = tot / 5
per = str(avg) + '%'

print(f"The total marks is {tot}, average marks is {avg} and the average percentage is {per}")
