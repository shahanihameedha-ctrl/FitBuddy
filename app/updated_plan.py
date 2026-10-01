import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""
    You are an expert personal trainer. 
    Here is the client's current 7-day workout plan:
    ---
    {original_plan}
    ---
    The client provided the following feedback/request for changes:
    "{feedback}"

    Please update and regenerate the complete 7-day workout plan incorporating this feedback cleanly.
    """
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text
