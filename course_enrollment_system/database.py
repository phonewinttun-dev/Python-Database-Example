import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "enrollment.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                instructor TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enroll_date TEXT NOT NULL,
                UNIQUE (student_id, course_id)
            )
        """)


def add_student(name, email):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO students (name, email) VALUES (?, ?)", (name, email)
            )
        return True, f"Student '{name}' added successfully."
    except sqlite3.IntegrityError:
        return False, f"A student with email '{email}' already exists."


def get_all_students():
    with get_connection() as conn:
        cur = conn.execute("SELECT id, name, email FROM students")
        return cur.fetchall()


def get_student_by_id(student_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, name, email FROM students WHERE id = ?", (student_id,)
        )
        return cur.fetchone()


def add_course(course_name, instructor):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO courses (course_name, instructor) VALUES (?, ?)",
            (course_name, instructor),
        )


def get_all_courses():
    with get_connection() as conn:
        cur = conn.execute("SELECT id, course_name, instructor FROM courses")
        return cur.fetchall()


def get_course_by_id(course_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, course_name, instructor FROM courses WHERE id = ?", (course_id,)
        )
        return cur.fetchone()


def enroll_student(student_id, course_id, enroll_date):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO enrollments (student_id, course_id, enroll_date) VALUES (?, ?, ?)",
                (student_id, course_id, enroll_date),
            )
        return True, "Enrolled successfully."
    except sqlite3.IntegrityError:
        return False, "This student is already enrolled in this course."


def get_all_enrollments():
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, student_id, course_id, enroll_date FROM enrollments"
        )
        return cur.fetchall()


def get_enrollments_by_student(student_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, course_id, enroll_date FROM enrollments WHERE student_id = ?",
            (student_id,),
        )
        return cur.fetchall()


def get_enrollments_by_course(course_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, student_id, enroll_date FROM enrollments WHERE course_id = ?",
            (course_id,),
        )
        return cur.fetchall()


def cancel_enrollment(enrollment_id):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM enrollments WHERE id = ?", (enrollment_id,))
        return cur.rowcount > 0
