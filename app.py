import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

DB_PATH = Path("students.db")

st.set_page_config(page_title="Student Record Manager", page_icon="🎓", layout="wide")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 6),
                marks REAL NOT NULL CHECK (marks BETWEEN 0 AND 100)
            )
        """)
        conn.commit()

def load_students(search=""):
    with get_connection() as conn:
        if search.strip():
            pattern = f"%{search.strip()}%"
            df = pd.read_sql_query(
                """SELECT student_id, name, email, department, year, marks
                   FROM students
                   WHERE name LIKE ? OR email LIKE ? OR department LIKE ?
                   ORDER BY student_id DESC""",
                conn, params=(pattern, pattern, pattern)
            )
        else:
            df = pd.read_sql_query(
                """SELECT student_id, name, email, department, year, marks
                   FROM students ORDER BY student_id DESC""", conn
            )
    return df

def add_student(name, email, department, year, marks):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO students (name, email, department, year, marks) VALUES (?, ?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), department, year, marks)
        )
        conn.commit()

def update_student(student_id, name, email, department, year, marks):
    with get_connection() as conn:
        conn.execute(
            """UPDATE students SET name=?, email=?, department=?, year=?, marks=?
               WHERE student_id=?""",
            (name.strip(), email.strip().lower(), department, year, marks, student_id)
        )
        conn.commit()

def delete_student(student_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        conn.commit()

init_db()
st.title("🎓 Student Record Management System")
st.caption("A small CRUD application built with Python, Streamlit, and SQLite.")

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose an action", ["Dashboard", "Add Student", "Edit / Delete"])
    st.divider()
    st.caption("Data is stored in a local SQLite database for this app instance.")

students = load_students()

if page == "Dashboard":
    total = len(students)
    avg_marks = float(students["marks"].mean()) if total else 0.0
    departments = int(students["department"].nunique()) if total else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total students", total)
    c2.metric("Average marks", f"{avg_marks:.1f}" if total else "—")
    c3.metric("Departments", departments)

    search = st.text_input("Search by name, email, or department")
    view = load_students(search)
    if not view.empty:
        view = view.rename(columns={
            "student_id": "ID", "name": "Name", "email": "Email",
            "department": "Department", "year": "Year", "marks": "Marks"
        })
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.download_button(
            "Download records as CSV",
            data=view.to_csv(index=False).encode("utf-8"),
            file_name="student_records.csv",
            mime="text/csv"
        )
    else:
        st.info("No records found. Add a student to get started.")

elif page == "Add Student":
    st.subheader("Add a new student")
    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("Full name")
        email = st.text_input("Email")
        department = st.selectbox("Department", ["ECE", "CSE", "EE", "ME", "Civil", "Other"])
        year = st.selectbox("Year of study", [1, 2, 3, 4, 5, 6])
        marks = st.number_input("Marks (0–100)", min_value=0.0, max_value=100.0, value=75.0, step=0.5)
        submitted = st.form_submit_button("Save student", type="primary")
    if submitted:
        if not name.strip() or not email.strip():
            st.error("Name and email are required.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            st.error("Enter a valid email address.")
        else:
            try:
                add_student(name, email, department, year, marks)
                st.success(f"Added {name.strip()} successfully.")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("That email already exists. Use a unique email address.")

else:
    st.subheader("Edit or delete a student")
    if students.empty:
        st.info("There are no records to edit yet.")
    else:
        options = {
            f'#{int(row.student_id)} — {row.name} ({row.email})': int(row.student_id)
            for row in students.itertuples()
        }
        selected_label = st.selectbox("Select a record", list(options.keys()))
        selected_id = options[selected_label]
        row = students.loc[students["student_id"] == selected_id].iloc[0]

        with st.form("edit_student_form"):
            name = st.text_input("Full name", value=str(row["name"]))
            email = st.text_input("Email", value=str(row["email"]))
            departments = ["ECE", "CSE", "EE", "ME", "Civil", "Other"]
            department = st.selectbox(
                "Department", departments,
                index=departments.index(row["department"]) if row["department"] in departments else departments.index("Other")
            )
            year = st.selectbox("Year of study", [1, 2, 3, 4, 5, 6], index=int(row["year"]) - 1)
            marks = st.number_input("Marks (0–100)", min_value=0.0, max_value=100.0, value=float(row["marks"]), step=0.5)
            save = st.form_submit_button("Update record", type="primary")
        if save:
            if not name.strip() or not email.strip():
                st.error("Name and email are required.")
            else:
                try:
                    update_student(selected_id, name, email, department, year, marks)
                    st.success("Record updated.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("That email is already assigned to another record.")

        st.divider()
        st.warning("Deleting a record cannot be undone.")
        confirm = st.checkbox("I understand and want to delete this record.")
        if st.button("Delete selected student", disabled=not confirm):
            delete_student(selected_id)
            st.success("Record deleted.")
            st.rerun()

st.divider()
st.caption("Portfolio project • Demonstrates CRUD operations, SQL queries, validation, filtering, and CSV export.")
