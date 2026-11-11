# AI Student Record Manager

A beginner-friendly web application designed for teachers to manage student academic records, calculate results automatically, and leverage Generative AI (Groq API) to analyze academic performance and generate personalized study tips.

---

## Features

- **Student Management (CRUD):** Add, view, update, and delete student records with a responsive green-and-white interface.
- **Automatic Calculations:** Instantly computes total marks, average percentage, and letter grades (A, B, C, D, F) upon adding or updating records.
- **Search & Filter:** Search students by Name or Student ID, with a "Show All" toggle.
- **Groq AI Integration:** 
  - **Analyze Performance:** Subject-wise breakdown, strengths, weaknesses, performance summary, and actionable advice.
  - **Generate Study Tips:** Personalized weekly study plans, daily tips, and motivational guidance.
  - **Privacy First:** Only anonymous academic metrics (class, subjects, marks, total, average, grade) are sent to the AI API; names and student IDs are excluded.
- **Persistent Storage:** Records are securely saved in `students.json`.

---

## Technologies Used

- **Backend:** Python 3, Flask, `python-dotenv`, Groq Python SDK
- **Frontend:** HTML5, CSS3, JavaScript, Fetch API
- **Storage:** JSON (`students.json`)
- **Environment:** Visual Studio Code, Python Virtual Environment (`venv`), Google Chrome

---

## Setup & Installation Instructions

### 1. Prerequisites
Ensure you have Python 3.x and Visual Studio Code installed.

### 2. Create Virtual Environment
Open your terminal in the project directory and run:
```bash
python -m venv venv
```

### 3. Activate Environment
- **Windows (Command Prompt / PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 5. Configure Groq API Key
1. Copy `.env.example` to a new file named `.env`:
   ```bash
   copy .env.example .env
   ```
   *(On macOS/Linux: `cp .env.example .env`)*
2. Open `.env` and add your actual Groq API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

---

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open **Google Chrome** and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

---

## Common Errors & Solutions

- **`GROQ_API_KEY is missing`**: Ensure you created the `.env` file in the root directory with a valid `GROQ_API_KEY`.
- **ModuleNotFoundError**: Ensure your virtual environment is activated and dependencies are installed via `pip install -r requirements.txt`.
- **Port 5000 in use**: Stop any other service running on port 5000 or modify the port at the bottom of `app.py`.
