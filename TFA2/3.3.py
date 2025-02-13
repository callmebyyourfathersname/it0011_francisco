# 3.3. Practical Problem Solving with String Manipulation and File Handling
# Objective: Apply string manipulation and file handling techniques to store student information in a file.

# Task: Write a Python program that does the following:
# -- Accepts input for the last name, first name, age, contact number, and course from the user.
# -- Creates a string containing the collected information in a formatted way.

LName = input("Enter last name: ")
FName = input("Enter first name: ")
Age = int(input("Enter your age: "))
ContactN = int(input("Enter contact number: "))
Course = input ("Enter course: ")
ALl_info = f"Name = {LName} + {FName},  Age= {Age}, Contact: {ContactN},John Course: {Course}"

with open("C:\\Users\\202312737\\Documents\\GitHub\\it0011_francisco\\TFA2\\students.txt", "w") as f:
    f.write(ALl_info)
print("Student information has been saved to ‘students.txt’.")
f.close()

