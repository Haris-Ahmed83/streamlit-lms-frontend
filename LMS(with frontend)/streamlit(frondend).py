import streamlit as st
import sqlite3
import pandas as pd
import random
import time

# Single Database Connection
conn = sqlite3.connect("sqllite3.db", check_same_thread=False)
cursor = conn.cursor()

# Page Config
st.set_page_config(page_title="Student LMS", layout="wide")

# Session State for Navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Back Button
def back_button():
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# Home Page
if st.session_state.page == "home":
    st.title("🎓 Student Learning Management System")
    st.markdown("### Select an action")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("###")
        if st.button("📋 Show All Students", use_container_width=True):
            st.session_state.page = "show"
            st.rerun()
        if st.button("➕ Add New Student", use_container_width=True):
            st.session_state.page = "add"
            st.rerun()
        if st.button("🗑️ Delete Student", use_container_width=True):
            st.session_state.page = "delete"
            st.rerun()
        if st.button("🔍 Search Student", use_container_width=True):
            st.session_state.page = "search"
            st.rerun()
        if st.button("📊 View Results", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()

# Show All Students
elif st.session_state.page == "show":
    st.subheader("📋 All Student Records")
    back_button()
    cursor.execute("SELECT * FROM student")
    data = cursor.fetchall()
    if data:
        cols = ["ID","Roll No","Name","Father Name","Department","Semester","Marks","Attendance","Fees Status","GPA","Courses"]
        st.dataframe(pd.DataFrame(data, columns=cols), use_container_width=True)
    else:
        st.warning("No data found.")

# Add New Student
elif st.session_state.page == "add":
    st.subheader("➕ Add New Student")
    back_button()
    with st.form("add_student"):
        roll = st.number_input("Roll Number", step=1)
        # Check duplicate roll
        cursor.execute("SELECT * FROM student WHERE St_Roll_no=?", (roll,))
        if cursor.fetchone():
            st.error("Roll Number already exists.")
        else:
            name = st.text_input("Student Name")
            father = st.text_input("Father Name")
            dept = st.text_input("Department")
            sem = st.text_input("Semester")
            attendance = st.number_input("Attendance (%)", 0.0, 100.0, step=0.1)
            fees = st.selectbox("Fees Status", ["Paid", "Unpaid"])
            courses = st.text_input("Courses")
            submit = st.form_submit_button("Save Student")

            if submit:
                with conn:
                    cursor.execute("""
                        INSERT INTO student(St_Name, St_Roll_no, St_Father_Name, st_Department,
                        st_Semester, st_Marks, St_Attendance, St_Fees_Status, st_GPA, St_Course_Enrollment)
                        VALUES (?, ?, ?, ?, ?, 0, ?, ?, 0, ?)""",
                        (name, roll, father, dept, sem, attendance, fees, courses)
                    )
                    # Random initial marks
                    eng, urdu, math, bio, phy = [random.randint(50, 100) for _ in range(5)]
                    total = eng + urdu + math + bio + phy
                    cgpa = round(total / 500 * 4, 2)
                    cursor.execute("""
                        INSERT INTO student_marks(St_Roll_no, st_Name, English, Urdu, Math, Biology, Physics, Total_marks, CGPA)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (roll, name, eng, urdu, math, bio, phy, total, cgpa)
                    )
                st.success("Student added successfully ✅")

# Delete Student
elif st.session_state.page == "delete":
    st.subheader("🗑️ Delete Student")
    back_button()
    roll = st.number_input("Enter Roll Number", step=1)
    if st.button("Delete"):
        with conn:
            cursor.execute("DELETE FROM student WHERE St_Roll_no=?", (roll,))
            cursor.execute("DELETE FROM student_marks WHERE St_Roll_no=?", (roll,))
        if cursor.rowcount > 0:
            st.success("Student deleted successfully.")
        else:
            st.error("Student not found.")

# Search Student
elif st.session_state.page == "search":
    st.subheader("🔍 Search Student")
    back_button()
    roll = st.number_input("Enter Roll Number", step=1)
    if st.button("Search"):
        cursor.execute("SELECT * FROM student WHERE St_Roll_no=?", (roll,))
        data = cursor.fetchone()
        if data:
            cols = ["ID","Roll No","Name","Father Name","Department","Semester","Marks","Attendance","Fees Status","GPA","Courses"]
            st.dataframe(pd.DataFrame([data], columns=cols), use_container_width=True)
        else:
            st.warning("Student not found.")
# View Results
elif st.session_state.page == "results":
    st.subheader("📊 Student Results")
    back_button()
    option = st.radio("Select Option", ["View All Results", "Search Result", "Add/Update Marks"])
    
    if option == "View All Results":
        cursor.execute("SELECT * FROM student_marks")
        data = cursor.fetchall()
        if data:
            cols = ["ID","Roll No","Name","English","Urdu","Math","Biology","Physics","Total Marks","CGPA"]
            st.dataframe(pd.DataFrame(data, columns=cols), use_container_width=True)
        else:
            st.warning("No results found.")
    
    elif option == "Search Result":
        roll = st.number_input("Enter Roll Number to Search", step=1, key="search_roll")
        if st.button("Search", key="search_button"):
            cursor.execute("SELECT * FROM student_marks WHERE St_Roll_no=?", (roll,))
            data = cursor.fetchone()
            if data:
                cols = ["ID","Roll No","Name","English","Urdu","Math","Biology","Physics","Total Marks","CGPA"]
                st.dataframe(pd.DataFrame([data], columns=cols), use_container_width=True)
            else:
                st.warning("Result not found.")
    
    elif option == "Add/Update Marks":
        roll = st.number_input("Enter Roll Number", step=1, key="update_roll")
        cursor.execute("SELECT * FROM student_marks WHERE St_Roll_no=?", (roll,))
        data = cursor.fetchone()
        if data:
            st.markdown(f"Updating marks for **{data[2]}**")
            eng = st.number_input("English", 0, 100, value=int(data[3]))
            urdu = st.number_input("Urdu", 0, 100, value=int(data[4]))
            math = st.number_input("Math", 0, 100, value=int(data[5]))
            bio = st.number_input("Biology", 0, 100, value=int(data[6]))
            phy = st.number_input("Physics", 0, 100, value=int(data[7]))
            if st.button("Save Marks"):
                total = eng + urdu + math + bio + phy
                cgpa = round(total / 500 * 4, 2)
                with conn:
                    cursor.execute("""
                        UPDATE student_marks
                        SET English=?, Urdu=?, Math=?, Biology=?, Physics=?, Total_marks=?, CGPA=?
                        WHERE St_Roll_no=?""",
                        (eng, urdu, math, bio, phy, total, cgpa, roll)
                    )
                st.success("Marks updated successfully ✅")
        else:
            st.warning("Student not found. Add student first.")
