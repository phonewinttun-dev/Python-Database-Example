"""
Main application file for Course Enrollment System (3 Tables)
User interface via Command Line Menu (CLI)
"""

from datetime import date
import database as db


def show_menu():
    print("\n" + "=" * 48)
    print("      COURSE ENROLLMENT SYSTEM (3 TABLES)")
    print("=" * 48)
    print("1.  Add New Student")
    print("2.  View All Students")
    print("3.  Add New Course")
    print("4.  View All Courses")
    print("5.  Enroll Student in Course")
    print("6.  View All Enrollments (3-Table JOIN)")
    print("7.  View Courses Enrolled by a Student")
    print("8.  View Students Enrolled in a Course")
    print("9.  Cancel an Enrollment")
    print("10. Exit")
    print("=" * 48)


def handle_add_student():
    print("\n--- Add New Student ---")
    name = input("Enter student name: ").strip()
    email = input("Enter student email: ").strip()

    if not name or not email:
        print("Error: Name and email cannot be empty.")
        return

    success, message = db.add_student(name, email)
    if success:
        print(f"Success: {message}")
    else:
        print(f"Notice: {message}")


def handle_view_students():
    students = db.get_all_students()
    print("\n--- Student List ---")
    if not students:
        print("No students found.")
        return

    print(f"{'ID':<6} {'Name':<25} {'Email':<30}")
    print("-" * 65)
    for s in students:
        print(f"{s[0]:<6} {s[1]:<25} {s[2]:<30}")


def handle_add_course():
    print("\n--- Add New Course ---")
    course_name = input("Enter course name (e.g. Python Programming): ").strip()
    instructor = input("Enter instructor name (e.g. Daw Aye Aye): ").strip()

    if not course_name or not instructor:
        print("Error: Course name and instructor cannot be empty.")
        return

    db.add_course(course_name, instructor)
    print(f"Success: Course '{course_name}' taught by '{instructor}' added successfully.")


def handle_view_courses():
    courses = db.get_all_courses()
    print("\n--- Course List ---")
    if not courses:
        print("No courses found.")
        return

    print(f"{'ID':<6} {'Course Name':<30} {'Instructor':<25}")
    print("-" * 65)
    for c in courses:
        print(f"{c[0]:<6} {c[1]:<30} {c[2]:<25}")


def handle_enroll_student():
    print("\n--- Enroll Student in Course ---")
    students = db.get_all_students()
    courses = db.get_all_courses()

    if not students:
        print("Notice: No students found. Please add a student first.")
        return
    if not courses:
        print("Notice: No courses found. Please add a course first.")
        return

    print("\nAvailable Students:")
    for s in students:
        print(f"ID: {s[0]} | {s[1]} ({s[2]})")

    print("\nAvailable Courses:")
    for c in courses:
        print(f"ID: {c[0]} | {c[1]} (Instructor: {c[2]})")

    try:
        student_id = int(input("\nEnter Student ID to enroll: ").strip())
        if not db.get_student_by_id(student_id):
            print(f"Error: Student ID {student_id} does not exist.")
            return

        course_id = int(input("Enter Course ID to enroll: ").strip())
        if not db.get_course_by_id(course_id):
            print(f"Error: Course ID {course_id} does not exist.")
            return

        today_str = date.today().isoformat()
        date_input = input(f"Enter enrollment date (Press Enter for today: {today_str}): ").strip()
        enroll_date = date_input if date_input else today_str

        success, message = db.enroll_student(student_id, course_id, enroll_date)
        if success:
            print(f"Success: {message}")
        else:
            print(f"Notice: {message}")

    except ValueError:
        print("Error: Student ID and Course ID must be numbers.")


def handle_view_enrollments_join():
    enrollments = db.get_all_enrollments()
    print("\n--- All Enrollments (3-Table INNER JOIN) ---")
    if not enrollments:
        print("No enrollments found.")
        return

    print(f"{'ID':<5} {'Student Name':<20} {'Email':<25} {'Course Name':<25} {'Instructor':<20} {'Date':<12}")
    print("-" * 110)
    for e in enrollments:
        print(f"{e[0]:<5} {e[1]:<20} {e[2]:<25} {e[3]:<25} {e[4]:<20} {e[5]:<12}")


def handle_view_courses_by_student():
    try:
        student_id = int(input("\nEnter Student ID: ").strip())
        student = db.get_student_by_id(student_id)
        if not student:
            print(f"Error: Student ID {student_id} not found.")
            return

        courses = db.get_courses_by_student(student_id)
        print(f"\n--- Courses Enrolled by '{student[1]}' ({student[2]}) ---")
        if not courses:
            print("This student has not enrolled in any courses yet.")
            return

        print(f"{'Course ID':<10} {'Course Name':<30} {'Instructor':<25} {'Enroll Date':<12}")
        print("-" * 80)
        for c in courses:
            print(f"{c[0]:<10} {c[1]:<30} {c[2]:<25} {c[3]:<12}")
    except ValueError:
        print("Error: Student ID must be a number.")


def handle_view_students_by_course():
    try:
        course_id = int(input("\nEnter Course ID: ").strip())
        course = db.get_course_by_id(course_id)
        if not course:
            print(f"Error: Course ID {course_id} not found.")
            return

        students = db.get_students_by_course(course_id)
        print(f"\n--- Students Enrolled in '{course[1]}' (Instructor: {course[2]}) ---")
        if not students:
            print("No students have enrolled in this course yet.")
            return

        print(f"{'Student ID':<12} {'Name':<25} {'Email':<30} {'Enroll Date':<12}")
        print("-" * 80)
        for s in students:
            print(f"{s[0]:<12} {s[1]:<25} {s[2]:<30} {s[3]:<12}")
    except ValueError:
        print("Error: Course ID must be a number.")


def handle_cancel_enrollment():
    try:
        enrollment_id = int(input("\nEnter Enrollment ID to cancel: ").strip())
        if db.cancel_enrollment(enrollment_id):
            print(f"Success: Enrollment ID {enrollment_id} cancelled.")
        else:
            print(f"Error: Enrollment ID {enrollment_id} not found.")
    except ValueError:
        print("Error: Enrollment ID must be a number.")


def main():
    # Initialize the database tables on startup
    db.create_tables()

    while True:
        show_menu()
        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            handle_add_student()
        elif choice == "2":
            handle_view_students()
        elif choice == "3":
            handle_add_course()
        elif choice == "4":
            handle_view_courses()
        elif choice == "5":
            handle_enroll_student()
        elif choice == "6":
            handle_view_enrollments_join()
        elif choice == "7":
            handle_view_courses_by_student()
        elif choice == "8":
            handle_view_students_by_course()
        elif choice == "9":
            handle_cancel_enrollment()
        elif choice == "10":
            print("\nThank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()
