def TA_3b():
    v = 1
    while v <= 7:
        if v == 2 or v == 4:
            v += 1
            continue
        
        s = 7 - v
        while s > 0:
            print(" ", end="")
            s -= 1

        for _ in range(v):
            print(v, end="")
        print()
        
        v += 1

TA_3b()