import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_fitness_plan(goal: str, age: int):
    # Stable model name
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"Create a simple fitness plan for a {age} year old person with a goal of {goal}."
    
    response = model.generate_content(prompt)
    return response.text
