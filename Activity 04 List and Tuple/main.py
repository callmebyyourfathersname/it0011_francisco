records = []

try:
    with open("students.txt", "r") as file:
        for line in file:
            data = line.strip().split("|")
            if len(data) == 5:
                try:
                    records.append({
                        "student_id": data[0],
                        "name": (data[1], data[2]),
                        "class_standing": float(data[3]),
                        "major_exam": float(data[4])
                    })
                except ValueError:
                    print(f"Skipping invalid record: {line.strip()}")
except FileNotFoundError:
    pass

while True:
    print("\nStudent record management:")
    print("\nMenu:")
    print("1. Show All Students Record")
    print("2. Order by Last Name")
    print("3. Order by Grade")
    print("4. Show Student Record")
    print("5. Add Record")
    print("6. Edit Record")
    print("7. Delete Record")
    print("8. Save to File")
    print("9. Exit")
    choice = input("Choose an option: ") #please save 1st b4 exit
    
    if choice == "1":
        for record in records:
            print(record)
    elif choice == "2":
        records = sorted(records, key=lambda x: x['name'][1])
        for record in records:
            print(record)
    elif choice == "3":
        records = sorted(records, key=lambda x: (x['class_standing'] * 0.6) + (x['major_exam'] * 0.4), reverse=True)
        for record in records:
            print(record)
    elif choice == "4":
        student_id = input("Enter Student ID: ")
        found = False
        for record in records:
            if record['student_id'] == student_id:
                print(record)
                found = True
        if not found:
            print("Student not found.")
    elif choice == "5":
        student_id = input("Enter Student ID (6-digit number): ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        class_standing = float(input("Enter Class Standing Grade: "))
        major_exam = float(input("Enter Major Exam Grade: "))
        records.append({"student_id": student_id, "name": (first_name, last_name), "class_standing": class_standing, "major_exam": major_exam})
    elif choice == "6":
        student_id = input("Enter Student ID to Edit: ")
        found = False
        for record in records:
            if record['student_id'] == student_id:
                record['class_standing'] = float(input("Enter new Class Standing Grade: "))
                record['major_exam'] = float(input("Enter new Major Exam Grade: "))
                found = True
        if not found:
            print("Student not found.")
    elif choice == "7":
        student_id = input("Enter Student ID to Delete: ")
        for record in records:
            if record['student_id'] == student_id:
                records.remove(record)
                break
        else:
            print("Student not found.")
    elif choice == "8":
        with open("students.txt", "w") as file:
            for record in records:
                file.write(f"{record['student_id']}|{record['name'][0]}|{record['name'][1]}|{record['class_standing']}|{record['major_exam']}\n")
        print("Records saved successfully.")
    elif choice == "9":
        break
    else:
        print("Invalid Choice. Try Again.")
