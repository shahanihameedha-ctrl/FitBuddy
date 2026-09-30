import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_fitness_plan(goal: str, age: int) -> str:
    if not GEMINI_API_KEY:
        return "API key config panna villai. Env variable check pannunga."
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Create a simple workout and diet plan for a {age}-year-old person with the goal: {goal}."
    
    response = model.generate_content(prompt)
    return response.text
