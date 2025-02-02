def TA_3a():
    for i in range(1, 6):
        
        for j in range(5 - i):
            print(" ", end="")
        
        for k in range(1, i + 1):
            print(k, end="")
        print()

TA_3a()