"""
Database module for Course Enrollment System (3 Tables Capstone)
Topics demonstrated:
- Many-to-Many Relationship via a Junction Table (enrollments)
- SQLite3 Foreign Keys (PRAGMA foreign_keys = ON)
- UNIQUE constraint across multiple columns (UNIQUE(student_id, course_id))
- 3-Table INNER JOIN queries
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "enrollment.db")


def get_connection():
    """Create a database connection with foreign key constraint enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables():
    """Create 'students', 'courses', and 'enrollments' tables."""
    with get_connection() as conn:
        # Table 1: students
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        """)

        # Table 2: courses
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                instructor TEXT NOT NULL
            );
        """)

        # Table 3: enrollments (Junction / Bridge Table)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enroll_date TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (course_id) REFERENCES courses (id),
                UNIQUE (student_id, course_id)
            );
        """)


def add_student(name, email):
    """Add a student. Returns (success: bool, message: str)"""
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO students (name, email) VALUES (?, ?);",
                (name, email)
            )
        return True, f"Student '{name}' added successfully."
    except sqlite3.IntegrityError:
        return False, f"A student with email '{email}' already exists."


def get_all_students():
    """Retrieve all students."""
    with get_connection() as conn:
        cur = conn.execute("SELECT id, name, email FROM students ORDER BY id;")
        return cur.fetchall()


def get_student_by_id(student_id):
    """Retrieve a single student by ID."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, name, email FROM students WHERE id = ?;",
            (student_id,)
        )
        return cur.fetchone()


def add_course(course_name, instructor):
    """Add a new course."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO courses (course_name, instructor) VALUES (?, ?);",
            (course_name, instructor)
        )


def get_all_courses():
    """Retrieve all courses."""
    with get_connection() as conn:
        cur = conn.execute("SELECT id, course_name, instructor FROM courses ORDER BY id;")
        return cur.fetchall()


def get_course_by_id(course_id):
    """Retrieve a single course by ID."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, course_name, instructor FROM courses WHERE id = ?;",
            (course_id,)
        )
        return cur.fetchone()


def enroll_student(student_id, course_id, enroll_date):
    """
    Enroll a student into a course.
    Validates foreign keys and prevents duplicate enrollments using UNIQUE constraint.
    Returns (success: bool, message: str)
    """
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO enrollments (student_id, course_id, enroll_date)
                VALUES (?, ?, ?);
            """, (student_id, course_id, enroll_date))
        return True, "Student enrolled into course successfully."
    except sqlite3.IntegrityError as e:
        # Handles duplicate enrollment or non-existent foreign key
        err_msg = str(e).lower()
        if "unique" in err_msg:
            return False, "This student is already enrolled in this course."
        elif "foreign key" in err_msg:
            return False, "Invalid Student ID or Course ID."
        return False, f"Database error: {e}"


def get_all_enrollments():
    """
    Demonstrates 3-Table INNER JOIN:
    Combines enrollments, students, and courses into one readable view.
    """
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT 
                enrollments.id,
                students.name,
                students.email,
                courses.course_name,
                courses.instructor,
                enrollments.enroll_date
            FROM enrollments
            INNER JOIN students ON enrollments.student_id = students.id
            INNER JOIN courses ON enrollments.course_id = courses.id
            ORDER BY enrollments.id;
        """)
        return cur.fetchall()


def get_courses_by_student(student_id):
    """Get all courses a specific student is enrolled in."""
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT 
                courses.id,
                courses.course_name,
                courses.instructor,
                enrollments.enroll_date
            FROM enrollments
            INNER JOIN courses ON enrollments.course_id = courses.id
            WHERE enrollments.student_id = ?
            ORDER BY enrollments.id;
        """, (student_id,))
        return cur.fetchall()


def get_students_by_course(course_id):
    """Get all students enrolled in a specific course."""
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT 
                students.id,
                students.name,
                students.email,
                enrollments.enroll_date
            FROM enrollments
            INNER JOIN students ON enrollments.student_id = students.id
            WHERE enrollments.course_id = ?
            ORDER BY enrollments.id;
        """, (course_id,))
        return cur.fetchall()


def cancel_enrollment(enrollment_id):
    """Delete an enrollment record by its ID."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM enrollments WHERE id = ?;", (enrollment_id,))
        return cur.rowcount > 0
