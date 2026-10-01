import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"Provide a concise, practical nutrition or recovery tip tailored specifically for a fitness goal of '{goal}'."
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
