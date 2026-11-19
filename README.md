# Python Database Example

A collection of beginner-friendly database projects built with Python and SQLite (`sqlite3`).

These projects are designed with a simple, easy-to-understand, and beginner-friendly approach. All examples use Python's built-in `sqlite3` library with zero external dependencies, making them lightweight and easy to run, study, and modify.

The projects follow a progressive learning path: starting with single-table CRUD operations, moving up to two-table relational foreign keys, and advancing to a three-table system with a junction table.

---

## Project Structure

```
Python-Database-Example/
├── library_management/        # 1 Table: Books Management
│   └── app.py
├── staff_management/          # 1 Table: Staff Management
│   └── app.py
├── student_management/        # 1 Table: Student Records
│   └── app.py
├── student_class_management/  # 2 Tables: Classes & Students
│   ├── database.py
│   └── app.py
└── course_enrollment_system/  # 3 Tables: Students, Courses & Enrollments
    ├── database.py
    └── app.py
```

---

## Projects Overview

### Level 1: Single-Table Projects (1 Table)

Focuses on fundamental CRUD (Create, Read, Update, Delete) operations using a single SQLite table:

1. **`library_management/`**
   - **Table:** `books` (`id`, `title`, `author`, `year`)
   - **Key Features:** Table creation, inserting records (including batch insert via `executemany`), viewing, updating, and deleting books.

2. **`staff_management/`**
   - **Table:** `staff` (`id`, `name`, `position`, `salary`)
   - **Key Features:** Interactive CLI menu loop, parameterized SQL queries, updating staff position and salary, searching by ID and name.

3. **`student_management/`**
   - **Table:** `students` (`id`, `name`, `age`, `grade`)
   - **Key Features:** Basic student record tracking, listing students, updating grades, and deleting records.

---

### Level 2: Two-Table Project (2 Tables)

Introduces relational database structure and Foreign Keys with a straightforward design without complex JOIN queries:

- **`student_class_management/`**
  - **Tables:**
    - `classes` (`id`, `class_name`, `room_number`)
    - `students` (`id`, `name`, `email`, `class_id`)
  - **Key Features:**
    - **One-to-Many Relationship:** One class can contain multiple students.
    - **Foreign Key:** `class_id` in the `students` table references the `classes` table.
    - **Safety Check:** Prevents deleting a class if students are currently enrolled in it.
    - **Modular Structure:** Separated into `database.py` (data access functions) and `app.py` (CLI menu interface).

---

### Level 3: Three-Table Project (3 Tables)

Demonstrates how to handle relationships between multiple entities using an intermediary junction table:

- **`course_enrollment_system/`**
  - **Tables:**
    - `students` (`id`, `name`, `email` UNIQUE)
    - `courses` (`id`, `course_name`, `instructor`)
    - `enrollments` (`id`, `student_id`, `course_id`, `enroll_date`, `UNIQUE(student_id, course_id)`)
  - **Key Features:**
    - **Many-to-Many Concept:** Students can take multiple courses, and courses can have multiple students.
    - **Junction Table:** The `enrollments` table connects `student_id` with `course_id`.
    - **Duplicate Prevention:** Enforces a `UNIQUE` constraint so a student cannot enroll in the same course twice.
    - **Relational Filtering:** View all enrollments, enrollments for a specific student, or enrollments for a specific course without multi-table joins.

---

## Local Run Guide

### Prerequisites
- Python 3.8 or higher installed.
- No third-party packages required (SQLite is included with Python).

### Running Any Project

Open your terminal or command prompt and navigate to the project directory you want to run:

#### 1. Library Management (1 Table)
```bash
cd library_management
python app.py
```

#### 2. Staff Management (1 Table)
```bash
cd staff_management
python app.py
```

#### 3. Student Management (1 Table)
```bash
cd student_management
python app.py
```

#### 4. Student & Class Management (2 Tables)
```bash
cd student_class_management
python app.py
```

#### 5. Course Enrollment System (3 Tables)
```bash
cd course_enrollment_system
python app.py
```

> **Note:** Each project automatically creates its SQLite database file (`.db`) on its first run if one does not already exist.
