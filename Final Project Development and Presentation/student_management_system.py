import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet

# Encryption setup
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Student class which has encrypted values for sensitive information
class Student:
    def __init__(self, name, age, grade, privacy_consent):
        self.name = cipher.encrypt(name.encode()).decode()
        self.age = age
        self.grade = cipher.encrypt(grade.encode()).decode()
        self.privacy_consent = privacy_consent

    @staticmethod
    def decrypt_data(encrypted_data):
        return cipher.decrypt(encrypted_data.encode()).decode()

# Database operations
def connect_db():
    #naming the database with last four digits of student id of group leader
    connection = sqlite3.connect('students_management_system_0452.db')
    return connection

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

# GUI using Tkinter for the Student Management System
class StudentApp:
    def __init__(self, root):
        self.root = root
        #window name has last 4 digits of the group leader
        self.root.title("Student Management System 0452")
        self.root.geometry("380x380")
        self.create_widgets()
        create_table()

    def create_widgets(self):
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Age:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Grade:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Privacy Consent (1 = Yes, 0 = No):").grid(row=3, column=0, padx=10, pady=10)

        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1)

        self.grade_entry = tk.Entry(self.root)
        self.grade_entry.grid(row=2, column=1)

        self.consent_entry = tk.Entry(self.root)
        self.consent_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Add Student", command=self.add_student).grid(row=4, column=0, pady=10)
        tk.Button(self.root, text="View Students", command=self.view_students).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Update Student", command=self.update_student).grid(row=5, column=0, pady=10)
        tk.Button(self.root, text="Delete Student", command=self.delete_student).grid(row=5, column=1, pady=10)

    def validate_input(self, name, age, grade, consent):
        if not name or not age or not grade or not consent:
            return "No field should be empty!"
        if not age.isdigit() or not (5 <= int(age) <= 100):
            return "Invalid age! Age should be a number between 5 and 100."
        if consent not in ['0', '1']:
            return "Privacy consent must be 0 (No) or 1 (Yes)."
        return None

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

        student = Student(name, age, grade, consent)

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Students (name, age, grade, privacy_consent) 
            VALUES (?, ?, ?, ?)
        ''', (student.name, student.age, student.grade, student.privacy_consent))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student added successfully!")
        self.clear_entries()

    def view_students(self):
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
        connection.close()

        student_list = ""
        for student in students:
            decrypted_name = Student.decrypt_data(student[1])
            decrypted_grade = Student.decrypt_data(student[3])
            student_list += f"ID: {student[0]}, Name: {decrypted_name}, Age: {student[2]}, Grade: {decrypted_grade}, Consent: {student[4]}\n"

        messagebox.showinfo("Students List", student_list)

    def update_student(self):
        try:
            student_id = int(tk.simpledialog.askstring("Input", "Enter Student ID to update"))
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

        student = Student(name, age, grade, consent)

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE Students SET name=?, age=?, grade=?, privacy_consent=? WHERE id=?
        ''', (student.name, student.age, student.grade, student.privacy_consent, student_id))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student updated successfully!")
        self.clear_entries()

    def delete_student(self):
        try:
            student_id = int(tk.simpledialog.askstring("Input", "Enter Student ID to delete"))
        except ValueError:
            messagebox.showerror("Error", "Invalid Student ID")
            return

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Students WHERE id=?", (student_id,))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Student deleted successfully!")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.consent_entry.delete(0, tk.END)

# main execution of the program
if __name__ == '__main__':
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
