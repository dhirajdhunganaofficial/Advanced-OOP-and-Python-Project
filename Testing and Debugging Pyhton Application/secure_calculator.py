import tkinter as tk
from tkinter import messagebox
import re
import random

# Secure Calculator Class
class SecureCalculator:
    #this function is used to validate all the user's inputs. It also ensures only integer and number is entered to protect against injection attacks
    def validate_input(self, value):

        if not re.match(r"^-?\d+(\.\d+)?$", value):
            raise ValueError("Invalid input: only numerical values are allowed")
        return float(value)

    def add(self, a, b):
        a = self.validate_input(a)
        b = self.validate_input(b)
        return a + b

    def subtract(self, a, b):
        a = self.validate_input(a)
        b = self.validate_input(b)
        return a - b

    def multiply(self, a, b):
        a = self.validate_input(a)
        b = self.validate_input(b)
        return a * b

    def divide(self, a, b):
        a = self.validate_input(a)
        b = self.validate_input(b)
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

#code to name the window title with last four digit of student is as a unique parameter
student_ids = ['s20230452','s20230967']
selected_student_id = student_ids[random.randint(0, len(student_ids) - 1)]
unique_parameter = selected_student_id[-4:]

# GUI for Calculator
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Calculator "+unique_parameter)
        self.root.geometry("300x450")

        self.calculator = SecureCalculator()

        # Display screen
        self.entry = tk.Entry(root, width=13, font=('Arial', 24), borderwidth=5, relief='sunken')
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.entry.bind("<Key>", lambda e: "break")

        # Button layout
        button_layout = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
        ]

        # Adding buttons to the grid
        for (text, row, col) in button_layout:
            if text == "=":
                tk.Button(root, text=text, height=4, width=9, command=self.calculate).grid(row=row, column=col)
            else:
                tk.Button(root, text=text, height=4, width=9, command=lambda t=text: self.on_button_click(t)).grid(row=row, column=col)

        # Clear the display
        tk.Button(root, text='CLEAR', height=4, width=40, command=self.clear).grid(row=5, column=0, columnspan=4, pady=10)

        self.current_input = ""

    def on_button_click(self, char):
        self.current_input += str(char)
        self.update_entry()

    def clear(self):
        self.current_input = ""
        self.update_entry()

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.current_input)

    def calculate(self):
        try:
            result = eval(self.current_input)
            self.current_input = str(result)
            self.update_entry()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation: {e}")
            self.clear()

# Running the GUI
if __name__ == '__main__':
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
