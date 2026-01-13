from tabulate import tabulate
import sqlite3
import time

student_conn = sqlite3.connect("sqllite3.db")
student_cursors = student_conn.cursor()

Student_marks_conn = sqlite3.connect("sqllite3.db")  
Student_Marks_cursors = Student_marks_conn.cursor()

print("===Welcome to Student portal===")
while True:
    print("1.show All Data")
    print("2.Add New student")
    print("3.Delete student")
    print("4.Search Student")
    print("5.View Result")
    print("0.Exit")
    
    choose = int(input("Enter Your Choice: "))

    if choose == 1:
        import time
        print("\nPleace Wait Fetching all student records...")
        time.sleep(3)
        student_cursors.execute("SELECT * FROM student") 
        result = student_cursors.fetchall()
        headers = ["Roll_no","Name","Father_Name","Department","Semester","Marks","Attendance","Fees_Status","GPA","Course_Enrollment"]
        print(tabulate(result, headers=headers, tablefmt="grid"))
        
    elif choose == 2:
        St_Name = input("Enter your Name now:-")
        St_Roll_no = int(input("Enter your Rollno now:-"))
        St_Father_Name = input("Enter your Father Name now:-")
        st_Department = input("Enter your Department now:-")
        st_Semester = input("Enter your Semester now:-")
        St_Attendance = float(input("Enter your Attendance:-"))
        St_Fees_Status = input("Enter your St_Fees_Status:-")
        St_Course_Enrollment = input("Enter your St_Course_Enrollment:-")
        st_Marks = 0 #auto
        st_GPA = 0 #auto

        student_cursors.execute(
            "INSERT INTO student(St_Name,St_Roll_no,St_Father_Name,st_Department,st_Semester,st_Marks,St_Attendance,St_Fees_Status,st_GPA,St_Course_Enrollment) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (St_Name, St_Roll_no, St_Father_Name, st_Department, st_Semester, st_Marks, St_Attendance, St_Fees_Status, st_GPA, St_Course_Enrollment)
        )
        student_conn.commit()
        print("===Adding successfully===")
        print("=====================================================")

        Student_Marks_cursors.execute(
            "INSERT INTO student_marks(St_Roll_no,st_Name,English,Urdu,Math,Biology,Physics,Total_marks,CGPA)VALUES(?,?,0,0,0,0,0,0,0)",
            (St_Roll_no,St_Name)
        )
        Student_marks_conn.commit()
        add_marks=input("Do you want to add marks? (yes/no):")
        if add_marks == "yes":
            English=float(input("Enter your English marks:-"))
            Urdu=float(input("Enter your Urdu marks:-"))
            Math=float(input("Enter your Math marks:-"))
            Biology=float(input("Enter your Biology marks:-"))
            Physics=float(input("Enter your Physics marks:-"))
            print("Uploading Marks....🔃")
            time.sleep(3)
            Total_marks=English+Urdu+Math+Physics+Biology
            CGPA=round(Total_marks/500*4,2)
            
            Student_Marks_cursors.execute("""
                UPDATE Student_marks
                SET English=?, Urdu=?, Math=?, Biology=?, Physics=?, Total_marks=?, CGPA=?
                WHERE St_Roll_no=?
            """, (English, Urdu, Math, Biology, Physics, Total_marks, CGPA, St_Roll_no))
            print("Sucessfully Added ✅")

    elif choose == 3:
        delete_Roll_no = int(input("Enter your Student Roll No to delete: "))
        student_cursors.execute("DELETE FROM student WHERE St_Roll_no=?", (delete_Roll_no,))
        if student_cursors.rowcount <= 0:  
            print("Invalid roll_no")
        else:
            print(f"===ID:- {delete_Roll_no} Deleted. Updated student list===")
        student_conn.commit()
        print("=====================================================")
    
    elif choose == 4:
        search_roll = int(input("Enter a Roll Num:-"))
        student_cursors.execute("SELECT * FROM student WHERE St_Roll_no=?", (search_roll,))
        data = student_cursors.fetchone()
        if not data:
            print("Student not found")
        else:
            headers = ["Roll_no","Name","Father_Name","Department","Semester","Marks","Attendance","Fees_Status","GPA","Course_Enrollment"]
            print(tabulate([data], headers=headers, tablefmt="grid"))
   
    elif choose == 5:
        while True:
            print("1. View all results")
            print("2.Search Result")
            print("3.ADD marks of Any Student")
            print("0. Exit")
            choose=int(input("Chooose Options what you want"))
            if choose == 1:
                import time
                print("\nPleace Wait Fetching Your Data...")
                time.sleep(3)
                Student_Marks_cursors.execute("SELECT *FROM Student_marks")
                result = Student_Marks_cursors.fetchall()
                if not result:
                    print("Data is not Found❌")
                else:
                     headers = ["St_Id","St_Roll_No","St_Name","English","Urdu","Math","Biology","Physics","Total Marks","CGPA"]
                     print(tabulate(result, headers=headers, tablefmt="grid"))
            elif choose==2:
                roll_no = int(input("Enter Your Rollno: "))
                student_cursors.execute(
                    "SELECT st_Id, st_Roll_no, st_Name, English, Urdu, Math, Biology, Physics, Total_Marks, CGPA FROM Student_marks WHERE st_Roll_no=?",
                    (roll_no,) )
                result = student_cursors.fetchone()
                if not result:
                    print("Result Not Found❌")
                else:
                    headers = ["St_Id","St_Roll_No","St_Name","English","Urdu","Math","Biology","Physics","Total Marks","CGPA"]
                    print(tabulate([result], headers=headers, tablefmt="grid"))
            
            elif choose == 3:
                import time
                rollno = int(input("Enter your Rollno:-"))
                add_marks = input("Do you want to add marks? (yes/no): ").lower()  
                if add_marks == "yes":
                  
                    English = float(input("Enter your English marks:-"))
                    Urdu = float(input("Enter your Urdu marks:-"))
                    Math = float(input("Enter your Math marks:-"))
                    Biology = float(input("Enter your Biology marks:-"))
                    Physics = float(input("Enter your Physics marks:-"))

                    
                    Total_marks = English + Urdu + Math + Biology + Physics
                    CGPA = round(Total_marks / 500 * 4, 2)

                    
                    Student_Marks_cursors.execute("""
                        UPDATE Student_marks
                        SET English=?, Urdu=?, Math=?, Biology=?, Physics=?, Total_marks=?, CGPA=?
                        WHERE st_Roll_no=?
                    """, (English, Urdu, Math, Biology, Physics, Total_marks, CGPA, rollno))
                    Student_marks_conn.commit()
                    time.sleep(3)
                    print("Marks Updated Successfully ✅")
                    
                else:
                    print("Thanks, no marks added.")
            else:
                print("Back to home")
                print("=======================================================")
                break

    elif choose == 0:
        student_conn.commit()
        student_conn.close()
        Student_marks_conn.commit()
        Student_marks_conn.close()
        print("=============Bye==============")
        break
