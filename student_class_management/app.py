"""
Main application file for Student & Class Management System (2 Tables)
User interface via Command Line Menu (CLI)
"""

import database as db


def show_menu():
    print("\n" + "=" * 45)
    print("   STUDENT & CLASS MANAGEMENT (2 TABLES)")
    print("=" * 45)
    print("1. Add New Class")
    print("2. View All Classes")
    print("3. Add New Student")
    print("4. View All Students (with Class Info - JOIN)")
    print("5. View Students in a Specific Class")
    print("6. Delete Student")
    print("7. Delete Class (with Safety Check)")
    print("8. Exit")
    print("=" * 45)


def handle_add_class():
    print("\n--- Add New Class ---")
    name = input("Enter class name (e.g. Python Batch 1): ").strip()
    room = input("Enter room number (e.g. Room-101): ").strip()

    if not name or not room:
        print("Error: Class name and room number cannot be empty.")
        return

    db.add_class(name, room)
    print(f"Success: Class '{name}' added successfully.")


def handle_view_classes():
    classes = db.get_all_classes()
    print("\n--- Class List ---")
    if not classes:
        print("No classes found. Please add a class first.")
        return

    print(f"{'ID':<6} {'Class Name':<25} {'Room Number':<15}")
    print("-" * 50)
    for c in classes:
        print(f"{c[0]:<6} {c[1]:<25} {c[2]:<15}")


def handle_add_student():
    classes = db.get_all_classes()
    if not classes:
        print("\nNotice: You must create at least one class before adding students!")
        return

    print("\n--- Available Classes ---")
    for c in classes:
        print(f"ID: {c[0]} | Name: {c[1]} (Room: {c[2]})")

    try:
        class_id = int(input("\nEnter Class ID for this student: ").strip())
        target_class = db.get_class_by_id(class_id)
        if not target_class:
            print(f"Error: Class ID {class_id} does not exist.")
            return

        name = input("Enter student name: ").strip()
        email = input("Enter student email: ").strip()

        if not name or not email:
            print("Error: Name and email cannot be empty.")
            return

        db.add_student(name, email, class_id)
        print(f"Success: Student '{name}' enrolled into '{target_class[1]}'.")
    except ValueError:
        print("Error: Class ID must be a valid number.")


def handle_view_students_join():
    students = db.get_all_students_with_class()
    print("\n--- All Students with Class Details (INNER JOIN) ---")
    if not students:
        print("No students found.")
        return

    print(f"{'ID':<6} {'Name':<20} {'Email':<25} {'Class':<20} {'Room':<10}")
    print("-" * 85)
    for s in students:
        print(f"{s[0]:<6} {s[1]:<20} {s[2]:<25} {s[3]:<20} {s[4]:<10}")


def handle_view_students_by_class():
    try:
        class_id = int(input("\nEnter Class ID: ").strip())
        target_class = db.get_class_by_id(class_id)
        if not target_class:
            print(f"Error: Class ID {class_id} not found.")
            return

        students = db.get_students_by_class(class_id)
        print(f"\n--- Students in {target_class[1]} (Room: {target_class[2]}) ---")
        if not students:
            print("No students are enrolled in this class.")
            return

        print(f"{'ID':<6} {'Name':<20} {'Email':<25}")
        print("-" * 55)
        for s in students:
            print(f"{s[0]:<6} {s[1]:<20} {s[2]:<25}")
    except ValueError:
        print("Error: Class ID must be a valid number.")


def handle_delete_student():
    try:
        student_id = int(input("\nEnter Student ID to delete: ").strip())
        if db.delete_student(student_id):
            print(f"Success: Student ID {student_id} deleted.")
        else:
            print(f"Error: Student ID {student_id} not found.")
    except ValueError:
        print("Error: Student ID must be a valid number.")


def handle_delete_class():
    try:
        class_id = int(input("\nEnter Class ID to delete: ").strip())
        success, message = db.delete_class(class_id)
        if success:
            print(f"Success: {message}")
        else:
            print(f"Notice: {message}")
    except ValueError:
        print("Error: Class ID must be a valid number.")


def main():
    # Initialize the database tables on startup
    db.create_tables()

    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            handle_add_class()
        elif choice == "2":
            handle_view_classes()
        elif choice == "3":
            handle_add_student()
        elif choice == "4":
            handle_view_students_join()
        elif choice == "5":
            handle_view_students_by_class()
        elif choice == "6":
            handle_delete_student()
        elif choice == "7":
            handle_delete_class()
        elif choice == "8":
            print("\nThank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
