file = open("numbers.txt", "r")
data_lines = file.readlines()
file.close()

counter = 1

for line in data_lines:
    cleaned_line = line.strip()
    num_strings = cleaned_line.split(",")
    num_list = [int(x) for x in num_strings]
    total = sum(num_list)
    total_str = str(total)
    
    if total_str == total_str[::-1]:
        result = "Palindrome"
    else:
        result = "Not a palindrome"
    
    print(f"Line {counter}: {cleaned_line} (sum {total}) - {result}")
    counter += 1