def is_palindrome(n):
    return str(n) == str(n)[::-1]

with open("numbers.txt", "r") as file:
    lines = file.readlines()

for i, line in enumerate(lines, start=1):
    numbers = [int(num) for num in line.strip().split(",") if num.strip().isdigit()]
    if not numbers:
        continue
    total_sum = sum(numbers)
    result = "Palindrome" if is_palindrome(total_sum) else "Not a palindrome"
    print(f"Line {i}: {line.strip()} (sum {total_sum}) - {result}")