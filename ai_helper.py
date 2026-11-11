import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_api_key():
    """Retrieve Groq API key from environment variables."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from environment variables or .env file.")
    return api_key

def choose_model(client):
    """Choose configured model or select default Groq text-generation model."""
    configured_model = os.getenv("GROQ_MODEL")
    if configured_model:
        return configured_model
    return "llama-3.3-70b-versatile"

def ask_ai(prompt):
    """Send prompt to Groq API and return the response."""
    try:
        api_key = get_api_key()
        client = Groq(api_key=api_key)
        model = choose_model(client)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert academic advisor and educational assistant. Provide clear, constructive, practical, and encouraging feedback."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model,
            temperature=0.7,
            max_tokens=1000
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Groq API Error: {str(e)}")

def describe_student(student):
    """Format student data for AI while strictly respecting privacy (no name, no ID)."""
    marks_str = ", ".join([f"{subj}: {mark}" for subj, mark in student.get("marks", {}).items()])
    description = (
        f"Student Academic Profile:\n"
        f"- Class / Semester: {student.get('class', 'N/A')}\n"
        f"- Subjects & Marks: {marks_str}\n"
        f"- Total Marks: {student.get('total', 0)}\n"
        f"- Average Percentage: {student.get('average', 0)}%\n"
        f"- Grade: {student.get('grade', 'N/A')}"
    )
    return description

def analyze_performance(student):
    """Analyze student academic performance using Groq API."""
    profile = describe_student(student)
    prompt = (
        f"Analyze the following student academic performance based on their marks:\n\n"
        f"{profile}\n\n"
        f"Please provide:\n"
        f"1. A short performance summary.\n"
        f"2. Identification of strong subjects.\n"
        f"3. Identification of weak subjects (if any).\n"
        f"4. Practical, actionable ways to improve academic performance."
    )
    return ask_ai(prompt)

def generate_study_tips(student):
    """Generate personalized study tips using Groq API."""
    profile = describe_student(student)
    prompt = (
        f"Based on the following student academic profile, generate personalized study recommendations:\n\n"
        f"{profile}\n\n"
        f"Please provide:\n"
        f"1. A simple weekly study plan.\n"
        f"2. Specific suggestions for improving weak subjects.\n"
        f"3. Effective daily study habits/tips.\n"
        f"4. Practical learning recommendations.\n"
        f"5. Short motivational advice."
    )
    return ask_ai(prompt)
