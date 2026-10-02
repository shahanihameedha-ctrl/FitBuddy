import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Gemini API Key - Render Environment variable la set pannu
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.json
    age = data.get("age")
    weight = data.get("weight")
    goal = data.get("goal")

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Create diet plan, workout plan and tips for Age {age}, Weight {weight}kg, Goal {goal}. Give in short bullet points."
        response = model.generate_content(prompt)
        text = response.text
        # Simple parse - full text ah return panrom
        return jsonify({"plan": text})
    except Exception as e:
        # API key illa na, video la var maadiri dummy plan return pannum - 404/401 varaadhu
        print(e)
        if goal == "Weight Loss":
            diet = ["Green tea + almonds morning", "Oats + eggs breakfast", "Brown rice + chicken lunch", "Fruits evening", "2 roti + dal dinner", "2-3L water"]
            workout = ["30 min walking morning", "10 min jogging", "15 min skipping evening", "5 days workout"]
            tips = ["Calorie deficit maintain pannu"]
        elif goal == "Muscle Gain":
            diet = ["4 eggs + oats morning", "Chicken + rice afternoon", "Protein shake evening"]
            workout = ["Chest, Shoulder, Back, Legs - daily one", "Heavy weights 6-12 reps"]
            tips = ["Protein 1.5g per kg eduthuko"]
        else: # Stay Fit
            diet = ["Balanced 3 meals + 2 snacks", "Carbs, Protein, Veggies", "No junk food", "2.5L water"]
            workout = ["Yoga 20 min morning", "Cardio + strength 30 min", "Weekend any sport", "10000 steps daily"]
            tips = ["Consistent ah iru machi"]

        plan_text = f"**Diet Plan:**\n- " + "\n- ".join(diet) + f"\n\n**Workout Plan:**\n- " + "\n- ".join(workout) + f"\n\n**Tips:**\n- " + "\n- ".join(tips)
        return jsonify({"plan": plan_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
