import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")


def create_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            grade TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_student(name, age, grade):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
        (name, age, grade)
    )
    conn.commit()
    conn.close()
    print(f"Student '{name}' added successfully.")


def view_all_students():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, grade FROM students")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No student records found.")
        return

    print("\n--- Student List ---")
    print(f"{'ID':<5} {'Name':<20} {'Age':<6} {'Grade':<6}")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<6} {row[3]:<6}")


def search_by_grade(grade):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, age, grade FROM students WHERE grade = ?",
        (grade,)
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"No students found with grade '{grade}'.")
        return

    print(f"\n--- Students with Grade: {grade} ---")
    print(f"{'ID':<5} {'Name':<20} {'Age':<6} {'Grade':<6}")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<6} {row[3]:<6}")


def update_student_grade(student_id, new_grade):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET grade = ? WHERE id = ?",
        (new_grade, student_id)
    )
    conn.commit()
    updated_count = cur.rowcount
    conn.close()

    if updated_count == 0:
        print(f"No student found with ID {student_id}.")
    else:
        print(f"Student ID {student_id} updated with new grade '{new_grade}'.")


def delete_student(student_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    conn.commit()
    deleted_count = cur.rowcount
    conn.close()

    if deleted_count == 0:
        print(f"No student found with ID {student_id}.")
    else:
        print(f"Student ID {student_id} deleted successfully.")


def main():
    create_table()

    while True:
        print("\n=== Student Management System ===")
        print("1. View All Students")
        print("2. Add New Student")
        print("3. Search Students by Grade")
        print("4. Update Student Grade")
        print("5. Delete Student")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ").strip()

        if choice == "1":
            view_all_students()

        elif choice == "2":
            name = input("Enter student name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue

            age_input = input("Enter student age: ").strip()
            try:
                age = int(age_input)
            except ValueError:
                print("Invalid age. Please enter numbers only.")
                continue

            grade = input("Enter grade (e.g. A, B, C): ").strip()
            add_student(name, age, grade)

        elif choice == "3":
            grade = input("Enter grade to search: ").strip()
            search_by_grade(grade)

        elif choice == "4":
            id_input = input("Enter student ID to update: ").strip()
            try:
                student_id = int(id_input)
            except ValueError:
                print("Invalid ID. Please enter numbers only.")
                continue

            new_grade = input("Enter new grade: ").strip()
            update_student_grade(student_id, new_grade)

        elif choice == "5":
            id_input = input("Enter student ID to delete: ").strip()
            try:
                student_id = int(id_input)
            except ValueError:
                print("Invalid ID. Please enter numbers only.")
                continue

            delete_student(student_id)

        elif choice == "0":
            print("Exiting application. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose an option from 0 to 5.")


if __name__ == "__main__":
    main()
