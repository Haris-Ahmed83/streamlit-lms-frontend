import sqlite3

conn = sqlite3.connect("sqllite3.db")
cursors = conn.cursor()

#Student Data
students = [
    (123, "Ali", "Saeed", "Com", "3rd", 20, 78, "Paid", 3.14, "CS, Calculus-I, Physics"),
    (456, "Ahmed", "Saeed", "English", "3rd", 30, 78, "Paid", 3.14, "CS, Calculus-I, Physics"),
    (789, "Moiz", "Saeed", "Math", "3rd", 89, 78, "Paid", 3.14, "CS, Calculus-I, Physics")
]

for student in students:
    st_Roll_no, st_Name, st_Father_Name, st_Department, st_Semester, st_Marks, st_Attendance, st_Fees_Status, st_GPA, st_Course_Enrollment = student

    #Insertstudent table
    cursors.execute('''
        INSERT INTO student(st_Roll_no, st_Name, st_Father_Name, st_Department, st_Semester, st_Marks, st_Attendance, st_Fees_Status, st_GPA, st_Course_Enrollment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (st_Roll_no, st_Name, st_Father_Name, st_Department, st_Semester, st_Marks, st_Attendance, st_Fees_Status, st_GPA, st_Course_Enrollment))

    # Marks calculation
    if st_Name == "Ali":
        English, Urdu, Math, Biology, Physics = 80, 67, 54, 43, 32
    elif st_Name == "Ahmed":
        English, Urdu, Math, Biology, Physics = 70, 60, 65, 55, 50
    elif st_Name == "Moiz":
        English, Urdu, Math, Biology, Physics = 90, 85, 88, 80, 75

    Total_Marks = English + Urdu + Math + Biology + Physics
    CGPA = Total_Marks / 500 * 4

    # Insert into Student_marks table
    cursors.execute('''
        INSERT INTO Student_marks(st_Roll_no, st_Name, English, Urdu, Math, Biology, Physics, Total_Marks, CGPA)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (st_Roll_no, st_Name, English, Urdu, Math, Biology, Physics, Total_Marks, round(CGPA,2)))

conn.commit()
conn.close()
