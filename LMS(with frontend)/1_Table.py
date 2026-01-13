import sqlite3
conn = sqlite3.connect("sqllite3.db")
conn.execute('''
        create table if not exists student(
             st_id INTEGER PRIMARY key,
             st_Roll_no INTEGER,
             st_Name VARCHAR (50),
             st_Father_Name VARCHAR(60),
             st_Department VARCHAR (50),
             st_Semester VARCHAR(50),
             st_Marks REAL,
             st_Attendance REAL,
             st_Fees_Status VARCHAR(100),
             st_GPA REAL,
             st_Course_Enrollment VARCHAR(200)

        )
    ''')
conn.execute('''
        create table IF NOT EXISTS Student_marks(
             st_Id INTEGER PRIMARY KEY,
             st_Roll_no VARCHAR(50),
             st_Name TEXT,
             English REAL,
             Urdu REAL,
             Math REAL,
             Biology REAL,
             Physics REAL,
             Total_Marks REAL,
             CGPA REAL,
             FOREIGN KEY (st_Roll_no) REFERENCES student(St_Roll_no)

        )
    ''')

conn.commit()
conn.close()