import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Connection to the SQLite database
def connect_db():
    connection = sqlite3.connect('students_privacy.db')
    return connection

#create table if the table does not exist
def create_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL,
            privacy_consent INTEGER NOT NULL CHECK (privacy_consent IN (0, 1))
        )
    ''')
    connection.commit()
    connection.close()

#code to name the window title with last four digit of student is as a unique parameter
student_ids = ['s20230452','s20230967']
selected_student_id = student_ids[random.randint(0, len(student_ids) - 1)]
unique_parameter = selected_student_id[-4:]

# GUI for Student Management System
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System "+unique_parameter)
        self.root.geometry("400x300")
        self.root.minsize(400, 300)
        self.root.maxsize(700, 700)
        self.create_widgets()
        create_table()

    def create_widgets(self):
        # Labels and their respective input fields
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Age:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Grade:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Privacy Consent (1 = Yes, 0 = No):").grid(row=3, column=0, padx=10, pady=10)

        self. name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1)

        self.grade_entry = tk.Entry(self.root)
        self.grade_entry.grid(row=2, column=1)

        self.consent_entry = tk.Entry(self.root)
        self.consent_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(self.root, text="Add Student", command=self.add_student).grid(row=4, column=0, pady=10)
        tk.Button(self.root, text="View Students", command=self.view_students).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Update Student", command=self.update_student).grid(row=5, column=0, pady=10)
        tk.Button(self.root, text="Delete Student", command=self.delete_student).grid(row=5, column=1, pady=10)

    # validate user inputs
    def validate_input(self, name, age, grade, consent):
        if not name or not age or not grade or not consent:
            return "All fields are required!"
        if not age.isdigit() or not (5 <= int(age) <= 100):
            return "Invalid age! Age should be a number between 5 and 100."
        if consent not in ['0', '1']:
            return "Privacy consent must be 0 (No) or 1 (Yes)."
        return None

    # create a Final Project Development and Presentation student record, insert into the table
    def add_student(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        grade = self.grade_entry.get()
        consent = self.consent_entry.get()

        error = self.validate_input(name, age, grade, consent)
        if error:
            messagebox.showerror("Input Error", error)
            return

        if consent == "0":
            messagebox.showerror("Privacy Error", "Cannot add student without privacy consent.")
            return

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Students (name, age, grade, privacy_consent) 
            VALUES (?, ?, ?, ?)
        ''', (name, age, grade, consent))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student added successfully!")
        self.clear_entries()

    # reads records from a database table, retrieve data
    def view_students(self):
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
        connection.close()

        student_list = ""
        for student in students:
            student_list += f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}, Consent: {student[4]}\n"

        messagebox.showinfo("Students List", student_list)

    # update a student's record
    def update_student(self):
        try:
            student_id = int(simpledialog.askstring("Input", "Enter Student ID to update"))
        except ValueError:
            messagebox.showerror("Error", "Invalid Student ID")
            return

        name = self.name_entry.get()
        age = self.age_entry.get()
        grade = self.grade_entry.get()
        consent = self.consent_entry.get()

        error = self.validate_input(name, age, grade, consent)
        if error:
            messagebox.showerror("Input Error", error)
            return

        if consent == 0:
            messagebox.showerror("Input Error", error)
            return

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE Students SET name=?, age=?, grade=?, privacy_consent=? WHERE id=?
        ''', (name, age, grade, consent, student_id))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student updated successfully!")
        self.clear_entries()

    # Delete a student record
    def delete_student(self):
        try:
            student_id = int(simpledialog.askstring("Input", "Enter Student ID to delete"))
        except ValueError:
            messagebox.showerror("Error", "Invalid Student ID")
            return

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Students WHERE id=?", (student_id,))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student deleted successfully!")

    # Clears all input fields
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.consent_entry.delete(0, tk.END)

#the main function, the main execution of a program
if __name__ == '__main__':
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
