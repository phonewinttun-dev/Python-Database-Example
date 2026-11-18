import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "staff.db")


def create_table():
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                salary decimal NOT NULL)
            """)
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def add_staff(name, position, salary):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(
                "INSERT INTO staff (name, position, salary) VALUES (?, ?, ?)",
                (name, position, salary),
            )
        print(f"Staff member '{name}' added successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def view_staff():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute("SELECT id, name, position, salary FROM staff")
        rows = cur.fetchall()

        if not rows:
            print("No staff members found.")
            return

        print("\n--- Staff List ---")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Salary: {row[3]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def update_staff_position(staff_id, new_position):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(
                "UPDATE staff SET position = ? WHERE id = ?", (new_position, staff_id)
            )
        print(f"Staff member with ID {staff_id} updated successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def update_staff_salary(staff_id, new_salary):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(
                "UPDATE staff SET salary = ? WHERE id = ?", (new_salary, staff_id)
            )
        print(f"Staff member with ID {staff_id} updated successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def delete_staff(staff_id):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
        print(f"Staff member with ID {staff_id} deleted successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def search_staff_by_name(name):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(
            "SELECT id, name, position, salary FROM staff WHERE name LIKE ?",
            (f"%{name}%",),
        )
        rows = cur.fetchall()

        if not rows:
            print(f"No staff members found with name containing '{name}'.")
            return

        print(f"\n--- Staff Members with Name Containing: {name} ---")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Salary: {row[3]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def search_staff_by_id(staff_id):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(
            "SELECT id, name, position, salary FROM staff WHERE id = ?", (staff_id,)
        )
        row = cur.fetchone()

        if not row:
            print(f"No staff member found with ID {staff_id}.")
            return

        print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Salary: {row[3]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def main():
    create_table()
    while True:
        print("\n--- Staff Management System ---")
        print("1. Add Staff Member")
        print("2. View All Staff Members")
        print("3. Update Staff Position")
        print("4. Update Staff Salary")
        print("5. Delete Staff Member")
        print("6. Search Staff by Name")
        print("7. Search Staff by ID")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter staff name: ")
            position = input("Enter staff position: ")
            salary = float(input("Enter staff salary: "))
            add_staff(name, position, salary)
        elif choice == "2":
            view_staff()
        elif choice == "3":
            staff_id = int(input("Enter staff ID to update position: "))
            new_position = input("Enter new position: ")
            update_staff_position(staff_id, new_position)
        elif choice == "4":
            staff_id = int(input("Enter staff ID to update salary: "))
            new_salary = float(input("Enter new salary: "))
            update_staff_salary(staff_id, new_salary)
        elif choice == "5":
            staff_id = int(input("Enter staff ID to delete: "))
            delete_staff(staff_id)
        elif choice == "6":
            name = input("Enter name to search: ")
            search_staff_by_name(name)
        elif choice == "7":
            staff_id = int(input("Enter staff ID to search: "))
            search_staff_by_id(staff_id)
        elif choice == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
