# 3.1. Activity for Performing String Manipulations
# Objective: To perform common and practical string manipulations in Python.

# Task: Write a Python program that includes the following string manipulations:
# - Concatenate your first name and last name into a full name.
# - Slice the full name to extract the first three characters of the first name.
# - Use string formatting to create a greeting message that includes the sliced first name


FName = input("Enter your first name: ")
LName = input("Enter your last name: ")
Age = int(input("Enter your age: "))
FullName = FName + " " + LName
SlicedName = FullName[0:3]

Greetings = "Greeting Message: Hello, {0}  ! Welome. You are {1}   years old"

print("Full Name: ", FName + " " + " LName")
print("Sliced Name: ", FullName[0:3] )
print(Greetings.format(SlicedName, Age))