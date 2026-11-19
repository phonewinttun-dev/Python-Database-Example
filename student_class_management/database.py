"""
Database module for Student & Class Management (2 Tables Capstone)
Topics demonstrated:
- SQLite3 Connection with Foreign Key Support (PRAGMA foreign_keys = ON)
- 1-to-Many Relationship (One Class has Many Students)
- INNER JOIN Query
- Safe Deletion (Checking dependent records before delete)
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")


def get_connection():
    """Create a database connection with foreign key constraint enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables():
    """Create 'classes' and 'students' tables if they don't exist."""
    with get_connection() as conn:
        # Table 1: classes (Parent Table)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_name TEXT NOT NULL,
                room_number TEXT NOT NULL
            );
        """)

        # Table 2: students (Child Table with Foreign Key)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                class_id INTEGER NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes (id)
            );
        """)


def add_class(class_name, room_number):
    """Add a new class record."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO classes (class_name, room_number) VALUES (?, ?);",
            (class_name, room_number)
        )


def get_all_classes():
    """Retrieve all classes ordered by id."""
    with get_connection() as conn:
        cur = conn.execute("SELECT id, class_name, room_number FROM classes ORDER BY id;")
        return cur.fetchall()


def get_class_by_id(class_id):
    """Retrieve a single class by its ID."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, class_name, room_number FROM classes WHERE id = ?;",
            (class_id,)
        )
        return cur.fetchone()


def add_student(name, email, class_id):
    """Add a new student linked to an existing class."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO students (name, email, class_id) VALUES (?, ?, ?);",
            (name, email, class_id)
        )


def get_all_students_with_class():
    """
    Demonstrates INNER JOIN:
    Fetches students along with the class name and room number they belong to.
    """
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT 
                students.id,
                students.name,
                students.email,
                classes.class_name,
                classes.room_number
            FROM students
            INNER JOIN classes ON students.class_id = classes.id
            ORDER BY students.id;
        """)
        return cur.fetchall()


def get_students_by_class(class_id):
    """Get all students belonging to a specific class."""
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT id, name, email 
            FROM students 
            WHERE class_id = ? 
            ORDER BY id;
        """, (class_id,))
        return cur.fetchall()


def delete_student(student_id):
    """Delete a student record. Returns True if deleted, False otherwise."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM students WHERE id = ?;", (student_id,))
        return cur.rowcount > 0


def delete_class(class_id):
    """
    Safe delete: Checks if students are still enrolled before deleting the class.
    Returns (success: bool, message: str)
    """
    with get_connection() as conn:
        # Check student count first
        cur = conn.execute("SELECT COUNT(*) FROM students WHERE class_id = ?;", (class_id,))
        count = cur.fetchone()[0]

        if count > 0:
            return False, f"Cannot delete: {count} student(s) are still in this class. Remove or reassign them first."

        cur = conn.execute("DELETE FROM classes WHERE id = ?;", (class_id,))
        if cur.rowcount > 0:
            return True, "Class deleted successfully."
        return False, "Class not found."
