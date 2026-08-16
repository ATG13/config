def func(x,y):
    if x == 0:
        return y
    else:
        return func(x+1,y-x)

print(func(-3, 10))