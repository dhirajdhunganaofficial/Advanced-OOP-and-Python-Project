import sqlite3

#welcome message for the program
print("\nWelcome to the Program where we interact with student database!!!\n")

#unique parameter for database name
user_selected_database_name = input("Please select the database you want to use:\n Select '1' for students_0452\n Select '2' for students_0967\n")
student_ids = ['s20230452','s20230967']

def choose_database_name(selected_database_name):
    if selected_database_name == 1:
        selected_student_id = student_ids[selected_database_name-1]
        return selected_student_id
    elif selected_database_name == 2:
        selected_student_id = student_ids[selected_database_name-1]
        return selected_student_id
    else:
        print("\nYou have entered an invalid option!")
        user_selected_database_name = int(input("Please select the student id you want to use it for database name:\n Select '1' for students_0452\n Select '2' for students_0967\n"))
        selected_student_id = choose_database_name(user_selected_database_name)
        return selected_student_id

student_id = choose_database_name(int(user_selected_database_name))

#below statement sets database name with the last digit of the student as a unique parameter
database_name = "students_"+student_id[-4:]
print("\nYou have selected "+database_name+" database\n")

#logic to connect SQLite database or create the database if it does not exist
def connection_to_database():
    connection = sqlite3.connect(database_name)
    return connection

#create table if the table does not exist
def create_table():
    connection = connection_to_database()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL, 
                    age INTEGER NOT NULL, 
                    grade TEXT NOT NULL,
                    privacy_consent BOOLEAN NOT NULL)''')
    connection.commit()
    connection.close()

#validate user inputs
def validate_user_input(name, age, grade, privacy_consent):
    if not name or len(name) > 255:
        return "Invalid name: cannot be empty or exceed 255 characters."
    if not (5 <= age <= 100):
        return "Invalid age: must be between 5 and 100."
    if grade not in ["A", "B", "C", "D", "E", "F"]:
        return "Invalid grade: must be one of A, B, C, D, E, F."
    if privacy_consent not in [0, 1]:
        return "Invalid privacy consent: must be 0 (no) or 1 (yes)."
    return None

#read a record from a database table, retrieve data
def get_students():
    connection = connection_to_database()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    connection.close()

    print("Students List:")
    for row in rows:
        print(row)

    connection.close()

    continue_program = input("\nPress any key to continue or press 'N' for exit...")
    continue_operation(continue_program)

#create a Final Project Development and Presentation student record, insert into the table
def add_student(name, age, grade, privacy_consent):
    error = validate_user_input(name, age, grade, privacy_consent)
    if error:
        print(error)
        continue_program = input("\nPress any key to continue or press 'N' for exit...")
        continue_operation(continue_program)
        # return

    if privacy_consent == 0:
        print("Cannot add student without privacy consent.")
        continue_program = input("\nPress any key to continue or press 'N' for exit...")
        continue_operation(continue_program)
        # return

    connection = connection_to_database()
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO students (name, age, grade, privacy_consent)
                    VALUES (?, ?, ?, ?)''', (name, age, grade, privacy_consent))
    connection.commit()
    connection.close()
    print("Student added successfully.")

    continue_program = input("\nPress any key to continue or press 'N' for exit...")
    continue_operation(continue_program)

#update a student's record
def update_student(student_id, name, age, grade, privacy_consent):
    error = validate_user_input(name, age, grade, privacy_consent)
    if error:
        print(error)
        return

    if privacy_consent == 0:
        print("Cannot update student without privacy consent.")
        return

    connection = connection_to_database()
    cursor = connection.cursor()

    # Update only non-null fields
    updates = []
    params = []
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if age is not None:
        updates.append("age = ?")
        params.append(age)
    if grade is not None:
        updates.append("grade = ?")
        params.append(grade)
    if privacy_consent is not None:
        updates.append("privacy_consent = ?")
        params.append(privacy_consent)

    if updates:
        query = f"UPDATE Students SET {', '.join(updates)} WHERE id = ?"
        params.append(student_id)
        cursor.execute(query, tuple(params))
        connection.commit()
        print("Student updated successfully.")
    else:
        print("No updates made.")

    connection.close()

    continue_program = input("\nPress any key to continue or press 'N' for exit...")
    continue_operation(continue_program)

# Delete a student record
def delete_student(student_id):
    connection = connection_to_database()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Students WHERE id = ?', (student_id,))
    connection.commit()
    connection.close()
    print("Student deleted successfully.")

    continue_program = input("\nPress any key to continue or press 'N' for exit...")
    continue_operation(continue_program)

def choose_operation(selected_operation):
    if selected_operation == 1:
        get_students()

    elif selected_operation == 2:
        name = input("Name: ")
        age = input("Age: ")
        grade = input("Grade: ")
        privacy_consent = input("Privacy Consent: ")
        add_student(name, int(age), grade, int(privacy_consent))

    elif selected_operation == 3:
        id = input("Student ID: ")
        name = input("Name: ")
        age = input("Age: ")
        grade = input("Grade: ")
        privacy_consent = input("Privacy Consent: ")
        update_student(id, name, int(age), grade, int(privacy_consent))

    elif selected_operation == 4:
        id = input("Student ID: ")
        delete_student(id)

    else:
        print("You selected wrong option!")
        option = input("Please select the operation you want to perform in " + database_name + " database:\n Select '1' to Read Data\n Select '2' to Insert Date\n Select '3' to Update Date\n Select '4' to Delete Date\n")
        choose_operation(option)

def continue_operation(key_selection):
    if key_selection == 'n' or key_selection == 'N':
        exit()
    else:
        operation_selected = int(input(
            "Please select the operation you want to perform in " + database_name + " database:\n Select '1' to Read Data\n Select '2' to Insert Date\n Select '3' to Update Date\n Select '4' to Delete Date\n"))
        choose_operation(operation_selected)

#the main function, the main execution of a program
if __name__ == '__main__':
    #this command creates a table in the database
    create_table()

    #menu to create selection options for the table
    operation_selected = int(input("Please select the operation you want to perform in " + database_name + " database:\n Select '1' to Read Data\n Select '2' to Insert Date\n Select '3' to Update Date\n Select '4' to Delete Date\n"))

    choose_operation(operation_selected)
