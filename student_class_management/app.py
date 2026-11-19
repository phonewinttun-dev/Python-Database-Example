import database as db


def main():
    db.create_tables()

    while True:
        print("""
--- Student & Class Management ---
1. Add Class
2. View All Classes
3. Add Student
4. View All Students
5. View Students by Class
6. Delete Student
7. Delete Class
8. Exit""")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            name = input("Enter class name: ").strip()
            room = input("Enter room number: ").strip()
            if name and room:
                db.add_class(name, room)
                print(f"Class '{name}' added successfully.")
            else:
                print("Class name and room cannot be empty.")

        elif choice == "2":
            classes = db.get_all_classes()
            if not classes:
                print("No classes found.")
                continue

            print("\n--- Classes ---")
            for c in classes:
                print(f"ID: {c[0]}, Name: {c[1]}, Room: {c[2]}")

        elif choice == "3":
            classes = db.get_all_classes()
            if not classes:
                print("Please create a class first.")
                continue

            print("\nAvailable Classes:")
            for c in classes:
                print(f"ID: {c[0]} - {c[1]}")

            try:
                class_id = int(input("Enter Class ID: ").strip())
                if not db.get_class_by_id(class_id):
                    print(f"Class ID {class_id} not found.")
                    continue

                name = input("Enter student name: ").strip()
                email = input("Enter student email: ").strip()
                if name and email:
                    db.add_student(name, email, class_id)
                    print(f"Student '{name}' added successfully.")
                else:
                    print("Name and email cannot be empty.")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "4":
            students = db.get_all_students()
            if not students:
                print("No students found.")
                continue

            print("\n--- All Students ---")
            for s in students:
                print(f"ID: {s[0]}, Name: {s[1]}, Email: {s[2]}, Class ID: {s[3]}")

        elif choice == "5":
            try:
                class_id = int(input("Enter Class ID: ").strip())
                students = db.get_students_by_class(class_id)
                if not students:
                    print(f"No students found in Class ID {class_id}.")
                    continue

                print(f"\n--- Students in Class ID {class_id} ---")
                for s in students:
                    print(f"ID: {s[0]}, Name: {s[1]}, Email: {s[2]}")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "6":
            try:
                student_id = int(input("Enter Student ID to delete: ").strip())
                if db.delete_student(student_id):
                    print(f"Student ID {student_id} deleted successfully.")
                else:
                    print(f"Student ID {student_id} not found.")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "7":
            try:
                class_id = int(input("Enter Class ID to delete: ").strip())
                if db.delete_class(class_id):
                    print(f"Class ID {class_id} deleted successfully.")
                else:
                    print(f"Cannot delete: Class ID {class_id} has enrolled students or does not exist.")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "8":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()
