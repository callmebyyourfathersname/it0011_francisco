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

        count = 0
        while count < v:
            print(v, end="")
            count += 1
        print()
        v += 1
