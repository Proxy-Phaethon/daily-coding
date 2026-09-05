import json
import os

DATA_FILE = "students.json"

def load_students():
    """Load student records from the JSON file. Returns a list of dicts."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("Warning: data file was corrupted or empty. Starting fresh.")
        return []

def save_students(students):
    """Save the list of student dicts back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

def get_next_id(students):
    """Generate the next available student ID (1-based, reuses gaps safely)."""
    if not students:
        return 1
    return max(s["id"] for s in students) + 1

def add_student(students):
    print("\n--- Add New Student ---")
    name = input("Full name: ").strip()
    if not name:
        print("Name cannot be empty. Cancelled.")
        return

    age = input_int("Age: ")
    grade = input("Grade/Class (e.g. '10th', 'Freshman'): ").strip()
    gpa = input_float("GPA (0.0 - 4.0): ")

    student = {
        "id": get_next_id(students),
        "name": name,
        "age": age,
        "grade": grade,
        "gpa": gpa,
    }
    students.append(student)
    save_students(students)
    print(f"Added student '{name}' with ID {student['id']}.")

def view_all_students(students):
    print("\n--- All Students ---")
    if not students:
        print("No student records found.")
        return

    print(f"{'ID':<5}{'Name':<20}{'Age':<6}{'Grade':<12}{'GPA':<6}")
    print("-" * 49)
    for s in sorted(students, key=lambda s: s["id"]):
        print(f"{s['id']:<5}{s['name']:<20}{s['age']:<6}{s['grade']:<12}{s['gpa']:<6}")

def find_student_by_id(students, student_id):
    for s in students:
        if s["id"] == student_id:
            return s
    return None

def search_students(students):
    print("\n--- Search Students ---")
    if not students:
        print("No student records found.")
        return

    query = input("Enter name (or part of name) to search: ").strip().lower()
    results = [s for s in students if query in s["name"].lower()]

    if not results:
        print("No matching students found.")
        return

    print(f"{'ID':<5}{'Name':<20}{'Age':<6}{'Grade':<12}{'GPA':<6}")
    print("-" * 49)
    for s in results:
        print(f"{s['id']:<5}{s['name']:<20}{s['age']:<6}{s['grade']:<12}{s['gpa']:<6}")

def update_student(students):
    print("\n--- Update Student ---")
    if not students:
        print("No student records found.")
        return

    student_id = input_int("Enter the ID of the student to update: ")
    student = find_student_by_id(students, student_id)

    if student is None:
        print(f"No student found with ID {student_id}.")
        return

    print(f"Editing '{student['name']}'. Leave a field blank to keep its current value.")

    new_name = input(f"Name [{student['name']}]: ").strip()
    if new_name:
        student["name"] = new_name

    new_age = input(f"Age [{student['age']}]: ").strip()
    if new_age:
        if new_age.isdigit():
            student["age"] = int(new_age)
        else:
            print("Invalid age, keeping previous value.")

    new_grade = input(f"Grade [{student['grade']}]: ").strip()
    if new_grade:
        student["grade"] = new_grade

    new_gpa = input(f"GPA [{student['gpa']}]: ").strip()
    if new_gpa:
        try:
            student["gpa"] = float(new_gpa)
        except ValueError:
            print("Invalid GPA, keeping previous value.")

    save_students(students)
    print(f"Student ID {student_id} updated.")

def delete_student(students):
    print("\n--- Delete Student ---")
    if not students:
        print("No student records found.")
        return

    student_id = input_int("Enter the ID of the student to delete: ")
    student = find_student_by_id(students, student_id)

    if student is None:
        print(f"No student found with ID {student_id}.")
        return

    confirm = input(f"Are you sure you want to delete '{student['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print(f"Deleted student ID {student_id}.")
    else:
        print("Cancelled.")

def input_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a whole number.")

def input_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number (e.g. 3.5).")

MENU = """
==========================
   STUDENT RECORD SYSTEM
==========================
1. Add student
2. View all students
3. Search students by name
4. Update a student
5. Delete a student
6. Exit
"""

def main():
    students = load_students()

    while True:
        print(MENU)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all_students(students)
        elif choice == "3":
            search_students(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 6.")

if __name__ == "__main__":
    main()