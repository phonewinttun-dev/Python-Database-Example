import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")


def create_table():
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL)
            """)
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def add_book(title, author):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        print(f"Book '{title}' added successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def view_all_books():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute("SELECT id, title, author FROM books")
        rows = cur.fetchall()

        if not rows:
            print("No books found.")
            return

        print("\n--- Book List ---")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def view_books_by_id(book_id):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute("SELECT id, title, author FROM books WHERE id = ?", (book_id,))
        row = cur.fetchone()

        if not row:
            print(f"No book found with ID {book_id}.")
            return

        print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def search_books_by_author(author):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute("SELECT id, title, author FROM books WHERE author = ?", (author,))
        rows = cur.fetchall()

        if not rows:
            print(f"No books found by author '{author}'.")
            return

        print(f"\n--- Books by Author: {author} ---")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def update_book_title(book_id, new_title):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            cur = conn.execute("UPDATE books SET title = ? WHERE id = ?", (new_title, book_id))
            if cur.rowcount == 0:
                print(f"No book found with ID {book_id}.")
            else:
                print(f"Book ID {book_id} title updated to '{new_title}'.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def delete_book(book_id):
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            cur = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            if cur.rowcount == 0:
                print(f"No book found with ID {book_id}.")
            else:
                print(f"Book ID {book_id} deleted successfully.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def main():
    create_table()

    while True:
        print("\n=== Library Management System ===")
        print("1. View All Books")
        print("2. Add New Book")
        print("3. View Book by ID")
        print("4. Search Books by Author")
        print("5. Update Book Title")
        print("6. Delete Book")
        print("0. Exit")

        choice = input("Enter your choice (0-6): ").strip()

        if choice == "1":
            view_all_books()

        elif choice == "2":
            title = input("Enter book title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue

            author = input("Enter author name: ").strip()
            if not author:
                print("Author cannot be empty.")
                continue

            add_book(title, author)

        elif choice == "3":
            id_input = input("Enter book ID: ").strip()
            try:
                book_id = int(id_input)
            except ValueError:
                print("Invalid ID. Please enter numbers only.")
                continue

            view_books_by_id(book_id)

        elif choice == "4":
            author = input("Enter author name to search: ").strip()
            search_books_by_author(author)

        elif choice == "5":
            id_input = input("Enter book ID to update: ").strip()
            try:
                book_id = int(id_input)
            except ValueError:
                print("Invalid ID. Please enter numbers only.")
                continue

            new_title = input("Enter new title: ").strip()
            if not new_title:
                print("Title cannot be empty.")
                continue

            update_book_title(book_id, new_title)

        elif choice == "6":
            id_input = input("Enter book ID to delete: ").strip()
            try:
                book_id = int(id_input)
            except ValueError:
                print("Invalid ID. Please enter numbers only.")
                continue

            delete_book(book_id)

        elif choice == "0":
            print("Exiting application. Goodbye!")
            break

        else:
            print("Invalid selection. Please choose an option from 0 to 6.")


if __name__ == "__main__":
    main()
