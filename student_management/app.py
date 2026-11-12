import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")


def create_table():
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    grade TEXT
                )
            """)
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def add_student(name, age, grade):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(
                "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
                (name, age, grade)
            )
        print(f"Student '{name}' added successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def view_all_students():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute("SELECT id, name, age, grade FROM students")
        rows = cur.fetchall()

        if not rows:
            print("No student records found.")
            return

        print("\n--- Student List ---")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def search_by_grade(grade):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(
            "SELECT id, name, age, grade FROM students WHERE grade = ?",
            (grade,)
        )
        rows = cur.fetchall()

        if not rows:
            print(f"No students found with grade '{grade}'.")
            return

        print(f"\n--- Students with Grade: {grade} ---")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def update_student_grade(student_id, new_grade):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            cur = conn.execute(
                "UPDATE students SET grade = ? WHERE id = ?",
                (new_grade, student_id)
            )
            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}.")
            else:
                print(f"Student ID {student_id} updated with new grade '{new_grade}'.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def delete_student(student_id):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            cur = conn.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )
            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}.")
            else:
                print(f"Student ID {student_id} deleted successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


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
