def sum_d():
    i = input("Enter a string: ")
    
    total = 0
    
    for char in i:
        if char.isdigit():
            total += int(char)
    
    print(f"Sum of digits: {total}")

sum_d()