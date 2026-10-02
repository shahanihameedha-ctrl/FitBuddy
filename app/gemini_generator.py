import os
import google.generativeai as genai

# Render Environment Variable-la irundhu Key-a edukkum
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_fitness_plan(name, age, gender, weight, height, goal, dietary_preference, fitness_level):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Create a detailed fitness and workout plan for:
    Name: {name}
    Age: {age}
    Gender: {gender}
    Weight: {weight} kg
    Height: {height} cm
    Fitness Goal: {goal}
    Dietary Preference: {dietary_preference}
    Fitness Level: {fitness_level}
    
    Include daily exercises and a basic diet overview.
    """
    
    response = model.generate_content(prompt)
    return response.text
