import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_name TEXT NOT NULL,
                room_number TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                class_id INTEGER NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes (id)
            )
        """)


def add_class(class_name, room_number):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO classes (class_name, room_number) VALUES (?, ?)",
            (class_name, room_number),
        )


def get_all_classes():
    with get_connection() as conn:
        cur = conn.execute("SELECT id, class_name, room_number FROM classes")
        return cur.fetchall()


def get_class_by_id(class_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, class_name, room_number FROM classes WHERE id = ?", (class_id,)
        )
        return cur.fetchone()


def add_student(name, email, class_id):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO students (name, email, class_id) VALUES (?, ?, ?)",
            (name, email, class_id),
        )


def get_all_students():
    with get_connection() as conn:
        cur = conn.execute("SELECT id, name, email, class_id FROM students")
        return cur.fetchall()


def get_students_by_class(class_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, name, email FROM students WHERE class_id = ?", (class_id,)
        )
        return cur.fetchall()


def delete_student(student_id):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return cur.rowcount > 0


def delete_class(class_id):
    with get_connection() as conn:
        # Check if any students are enrolled in this class
        cur = conn.execute(
            "SELECT COUNT(*) FROM students WHERE class_id = ?", (class_id,)
        )
        if cur.fetchone()[0] > 0:
            return False  # Cannot delete because students are in this class

        cur = conn.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        return cur.rowcount > 0
