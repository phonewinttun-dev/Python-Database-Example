from datetime import date
import database as db


def main():
    db.create_tables()

    while True:
        print("""
            --- Course Enrollment System ---
            1. Add Student
            2. View All Students
            3. Add Course
            4. View All Courses
            5. Enroll Student in Course
            6. View All Enrollments
            7. View Enrollments by Student
            8. View Enrollments by Course
            9. Cancel Enrollment
            10. Exit""")

        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            name = input("Enter student name: ").strip()
            email = input("Enter student email: ").strip()
            if name and email:
                success, msg = db.add_student(name, email)
                print(msg)
            else:
                print("Name and email cannot be empty.")

        elif choice == "2":
            students = db.get_all_students()
            if not students:
                print("No students found.")
                continue

            print("\n--- Students ---")
            for s in students:
                print(f"ID: {s[0]}, Name: {s[1]}, Email: {s[2]}")

        elif choice == "3":
            course_name = input("Enter course name: ").strip()
            instructor = input("Enter instructor name: ").strip()
            if course_name and instructor:
                db.add_course(course_name, instructor)
                print(f"Course '{course_name}' added successfully.")
            else:
                print("Course name and instructor cannot be empty.")

        elif choice == "4":
            courses = db.get_all_courses()
            if not courses:
                print("No courses found.")
                continue

            print("\n--- Courses ---")
            for c in courses:
                print(f"ID: {c[0]}, Course: {c[1]}, Instructor: {c[2]}")

        elif choice == "5":
            students = db.get_all_students()
            courses = db.get_all_courses()
            if not students or not courses:
                print("Please add at least one student and one course first.")
                continue

            print("\nAvailable Students:")
            for s in students:
                print(f"ID: {s[0]} - {s[1]}")

            print("\nAvailable Courses:")
            for c in courses:
                print(f"ID: {c[0]} - {c[1]}")

            try:
                student_id = int(input("\nEnter Student ID: ").strip())
                if not db.get_student_by_id(student_id):
                    print(f"Student ID {student_id} not found.")
                    continue

                course_id = int(input("Enter Course ID: ").strip())
                if not db.get_course_by_id(course_id):
                    print(f"Course ID {course_id} not found.")
                    continue

                today_str = date.today().isoformat()
                date_input = input(
                    f"Enter enrollment date (Press Enter for {today_str}): "
                ).strip()
                enroll_date = date_input if date_input else today_str

                success, msg = db.enroll_student(student_id, course_id, enroll_date)
                print(msg)
            except ValueError:
                print("Invalid input. IDs must be numbers.")

        elif choice == "6":
            enrollments = db.get_all_enrollments()
            if not enrollments:
                print("No enrollments found.")
                continue

            print("\n--- All Enrollments ---")
            for e in enrollments:
                print(
                    f"Enrollment ID: {e[0]}, Student ID: {e[1]}, Course ID: {e[2]}, Date: {e[3]}"
                )

        elif choice == "7":
            try:
                student_id = int(input("Enter Student ID: ").strip())
                enrollments = db.get_enrollments_by_student(student_id)
                if not enrollments:
                    print(f"No enrollments found for Student ID {student_id}.")
                    continue

                print(f"\n--- Enrollments for Student ID {student_id} ---")
                for e in enrollments:
                    print(f"Enrollment ID: {e[0]}, Course ID: {e[1]}, Date: {e[2]}")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "8":
            try:
                course_id = int(input("Enter Course ID: ").strip())
                enrollments = db.get_enrollments_by_course(course_id)
                if not enrollments:
                    print(f"No enrollments found for Course ID {course_id}.")
                    continue

                print(f"\n--- Enrollments for Course ID {course_id} ---")
                for e in enrollments:
                    print(f"Enrollment ID: {e[0]}, Student ID: {e[1]}, Date: {e[2]}")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "9":
            try:
                enrollment_id = int(input("Enter Enrollment ID to cancel: ").strip())
                if db.cancel_enrollment(enrollment_id):
                    print(f"Enrollment ID {enrollment_id} cancelled successfully.")
                else:
                    print(f"Enrollment ID {enrollment_id} not found.")
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "10":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1-10.")


if __name__ == "__main__":
    main()
