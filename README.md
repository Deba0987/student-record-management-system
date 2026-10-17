# Student Record Management System

A beginner-friendly portfolio project built with **Python, Streamlit, and SQLite**.

## Features
- Create, view, search, update, and delete student records (CRUD)
- SQLite database with a unique email constraint and validation
- Search records by name, email, or department
- Dashboard metrics: total students, average marks, department count
- Export the displayed records to CSV
- Parameterized SQL queries for database operations

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```
6. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Deploy a public demo with Streamlit Community Cloud
1. Create a GitHub repository named `student-record-management-system`.
2. Upload `app.py`, `requirements.txt`, and `README.md` to the repository. Do not upload `students.db`.
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Choose **Create app**, select your repository, branch, and `app.py`, then deploy.
5. Copy the public app URL after deployment and add that URL to your CV.

## Important deployment note
This demo uses a local SQLite file. On hosted platforms, local files may reset or may not persist across restarts/redeployments. Treat the public demo as a demonstration app, and use sample data only. Do not enter sensitive or real student information.

## CV bullet points (use after you have run and tested the app)
**Student Record Management System | Python, SQLite, SQL, Streamlit**
- Built a CRUD application for student records with search, update, deletion, and CSV export.
- Designed a SQLite schema with constraints and used parameterized SQL queries for data operations.
- Added input validation and a dashboard for record counts and average marks.

## Before adding it to your CV
Run the app, test adding/editing/deleting/searching records, and make sure you can explain each function and SQL query. Mark it as **In Progress** until you have tested it.
