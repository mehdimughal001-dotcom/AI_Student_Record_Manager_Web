import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import ai_helper

load_dotenv()

app = Flask(__name__)
DATA_FILE = "students.json"

def load_students():
    """Load student records from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {DATA_FILE}: {e}")
        return []

def save_students(students):
    """Save student records to JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=4)
    except Exception as e:
        print(f"Error saving {DATA_FILE}: {e}")

def calculate_results(marks_dict):
    """Calculate total, average percentage, and grade according to criteria."""
    if not marks_dict:
        return 0, 0.0, "F"
    
    total = sum(marks_dict.values())
    average = round(total / len(marks_dict), 2)
    
    if average >= 85:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "F"
        
    return total, average, grade

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/students", methods=["GET"])
def get_students():
    students = load_students()
    return jsonify(students)

@app.route("/api/students", methods=["POST"])
def add_student():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        student_id = data.get("id", "").strip()
        name = data.get("name", "").strip()
        semester = data.get("class", "").strip()
        subjects = data.get("subjects", [])
        raw_marks = data.get("marks", [])

        if not student_id or not name or not semester or not subjects or not raw_marks:
            return jsonify({"error": "All required fields must be completed."}), 400

        if len(subjects) != len(raw_marks):
            return jsonify({"error": "The number of subjects must match the number of marks."}), 400

        students = load_students()
        if any(s["id"] == student_id for s in students):
            return jsonify({"error": f"Student ID '{student_id}' already exists."}), 400

        if len(subjects) != len(set(subjects)):
            return jsonify({"error": "Subject names must not be duplicated."}), 400

        marks_dict = {}
        for subj, mark in zip(subjects, raw_marks):
            subj_clean = subj.strip()
            if not subj_clean:
                return jsonify({"error": "Subject name cannot be empty."}), 400
            try:
                m_val = float(mark)
                if not (0 <= m_val <= 100):
                    return jsonify({"error": f"Marks for '{subj_clean}' must be between 0 and 100."}), 400
                marks_dict[subj_clean] = m_val
            except ValueError:
                return jsonify({"error": f"Marks for '{subj_clean}' must be numeric."}), 400

        total, average, grade = calculate_results(marks_dict)

        new_student = {
            "id": student_id,
            "name": name,
            "class": semester,
            "marks": marks_dict,
            "total": total,
            "average": average,
            "grade": grade
        }

        students.append(new_student)
        save_students(students)

        return jsonify({"message": "Student added successfully", "student": new_student}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        name = data.get("name", "").strip()
        semester = data.get("class", "").strip()
        subjects = data.get("subjects", [])
        raw_marks = data.get("marks", [])

        if not name or not semester or not subjects or not raw_marks:
            return jsonify({"error": "All required fields must be completed."}), 400

        if len(subjects) != len(raw_marks):
            return jsonify({"error": "The number of subjects must match the number of marks."}), 400

        if len(subjects) != len(set(subjects)):
            return jsonify({"error": "Subject names must not be duplicated."}), 400

        students = load_students()
        student_index = -1
        for i, s in enumerate(students):
            if s["id"] == student_id:
                student_index = i
                break

        if student_index == -1:
            return jsonify({"error": f"Student ID '{student_id}' not found."}), 404

        marks_dict = {}
        for subj, mark in zip(subjects, raw_marks):
            subj_clean = subj.strip()
            if not subj_clean:
                return jsonify({"error": "Subject name cannot be empty."}), 400
            try:
                m_val = float(mark)
                if not (0 <= m_val <= 100):
                    return jsonify({"error": f"Marks for '{subj_clean}' must be between 0 and 100."}), 400
                marks_dict[subj_clean] = m_val
            except ValueError:
                return jsonify({"error": f"Marks for '{subj_clean}' must be numeric."}), 400

        total, average, grade = calculate_results(marks_dict)

        updated_record = {
            "id": student_id,
            "name": name,
            "class": semester,
            "marks": marks_dict,
            "total": total,
            "average": average,
            "grade": grade
        }

        students[student_index] = updated_record
        save_students(students)

        return jsonify({"message": "Student updated successfully", "student": updated_record}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        students = load_students()
        new_students = [s for s in students if s["id"] != student_id]

        if len(new_students) == len(students):
            return jsonify({"error": f"Student ID '{student_id}' not found."}), 404

        save_students(new_students)
        return jsonify({"message": f"Student '{student_id}' deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai/<kind>/<student_id>", methods=["POST"])
def handle_ai(kind, student_id):
    try:
        students = load_students()
        student = next((s for s in students if s["id"] == student_id), None)

        if not student:
            return jsonify({"error": f"Student ID '{student_id}' not found."}), 404

        if kind == "analyze":
            result = ai_helper.analyze_performance(student)
        elif kind == "tips":
            result = ai_helper.generate_study_tips(student)
        else:
            return jsonify({"error": "Invalid AI request type."}), 400

        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
