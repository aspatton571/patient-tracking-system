How to run (Windows)

1) Open this folder in VS Code (or File Explorer > address bar type cmd to open a terminal here).
2) Create/activate a virtual environment:
   python -m venv .venv
   .venv\Scripts\activate
3) Install packages:
   pip install -r requirements.txt
4) Seed demo data:
   python seed.py
5) Start the app:
   python app.py
6) Open http://127.0.0.1:5000

Demo flow:
- Add a patient, edit, discharge, delete
- Use search and status filter
- Data persists in SQLite (patients.db)
