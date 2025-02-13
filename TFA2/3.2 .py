# 3.2 Activity for Performing String Manipulations
# Objective: To perform common and practical string manipulations in Python.


# Task: Write a Python program that includes the following string manipulations:
# -- Input the user's first name and last name.
# -- Concatenate the input names into a full name.
# -- Display the full name in both upper and lower case.
# -- Count and display the length of the full name

FName = input("Enter your first name: ")
LName = input("Enter your last name: ")
FullName = FName + " " + LName

print("Full Name: ", FName + " " + " LName")
print("Full Name (Upper Case) : ", FullName.upper())
print("Full Name (Lower Case) : ", FullName.lower())
print("Length of Full Name: ", len(FullName))


