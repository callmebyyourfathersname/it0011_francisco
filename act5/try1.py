def divide(a, b):
    if b == 0:
        return None
    return a / b

def exponentiation(a, b):
    return a ** b

def remainder(a, b):
    if b == 0:
        return None
    return a % b

def summation(a, b):
    if b <= a:
        return None
    a_int = int(a)
    b_int = int(b)
    total = 0
    for num in range(a_int, b_int + 1):
        total += num
    return total

def main():
    while True:
        print("\n[D] - Divide")
        print("[E] - Exponentiation")
        print("[R] - Remainder")
        print("[F] - Summation")
        choice = input("Enter your choice: ").upper()
        if choice not in ['D', 'E', 'R', 'F']:
            print("Invalid choice. Please try again.")
            continue
        try:
            num1 = float(input("Please Enter first number: "))
            num2 = float(input("Please Enter second number: "))
        except ValueError:
            print("Invalid input. Please Try again.")
            continue
        
        if choice == 'D':
            result = divide(num1, num2)
            op = "Division"
        elif choice == 'E':
            result = exponentiation(num1, num2)
            op = "Exponentiation"
        elif choice == 'R':
            result = remainder(num1, num2)
            op = "Remainder"
        elif choice == 'F':
            result = summation(num1, num2)
            op = "Summation"
        
        if result is None:
            print(f"Error: Invalid input for {op}")
        else:
            print(f"Result: {result}")
if __name__ == "__main__":
    main()