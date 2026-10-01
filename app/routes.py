import os
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db, save_user, save_plan, update_plan_db, get_all_users_with_plans, PlanDB, UserDB
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-workout")
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    workout_plan = generate_workout_gemini(goal, intensity, age, weight)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    save_user(db, user_id, username, age, weight, goal, intensity)
    save_plan(db, user_id, workout_plan, nutrition_tip)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "workout_plan": workout_plan,
        "nutrition_tip": nutrition_tip,
        "updated_plan": None
    })

@router.post("/submit-feedback")
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    plan_entry = db.query(PlanDB).filter(PlanDB.user_id == user_id).first()
    user_entry = db.query(UserDB).filter(UserDB.user_id == user_id).first()

    if not plan_entry or not user_entry:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "error": "User or original plan not found!"
        })

    revised_plan = update_workout_plan(plan_entry.original_plan, feedback)
    update_plan_db(db, user_id, revised_plan)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "username": user_entry.username,
        "user_id": user_entry.user_id,
        "age": user_entry.age,
        "weight": user_entry.weight,
        "goal": user_entry.goal,
        "intensity": user_entry.intensity,
        "workout_plan": plan_entry.original_plan,
        "nutrition_tip": plan_entry.nutrition_tip,
        "updated_plan": revised_plan,
        "msg": "Plan updated successfully based on feedback!"
    })

@router.get("/view-all-users")
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users_data = get_all_users_with_plans(db)
    return templates.TemplateResponse("all_users.html", {
        "request": request,
        "users": users_data
    })
