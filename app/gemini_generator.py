import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_workout_gemini(goal: str, intensity: str, age: int, weight: int) -> str:
    prompt = f"""
    Create a detailed, personalized 7-day workout plan for a user with the following details:
    - Age: {age}
    - Weight: {weight} kg
    - Fitness Goal: {goal}
    - Intensity Level: {intensity}

    Structure the response clearly day-by-day (Day 1 to Day 7). 
    For each workout day, include:
    1. Warm-up (5-10 mins)
    2. Main Workout (Exercises, Sets, Reps/Duration)
    3. Cooldown / Recovery Suggestion
    """
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text
