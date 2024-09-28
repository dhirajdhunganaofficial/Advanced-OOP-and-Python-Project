import unittest
import sqlite3
import tkinter as tk
from student_management_system import StudentApp

class TestStudentApp(unittest.TestCase):
    def setUp(self):
        self.app = StudentApp(tk.Tk())

    def test_add_student(self):
        self.app.name_entry.insert(0, "test_Student")
        self.app.age_entry.insert(0, "25")
        self.app.grade_entry.insert(0, "A")
        self.app.consent_entry.insert(0, "1")
        self.app.add_student()

        connection = sqlite3.connect('students_management_system_0452.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Students WHERE age=25")
        student = cursor.fetchone()
        self.assertIsNotNone(student)
        self.assertEqual(student[2], 25)
        connection.close()

    def test_input_validation(self):
        # Test validation for missing inputs
        self.app.name_entry.delete(0, tk.END)
        self.app.age_entry.insert(0, "25")
        self.app.grade_entry.insert(0, "A")
        self.app.consent_entry.insert(0, "1")
        self.assertEqual(self.app.validate_input("", "25", "A", "1"), "No field should be empty!")

if __name__ == '__main__':
    unittest.main()
