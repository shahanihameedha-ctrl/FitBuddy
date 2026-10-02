from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.gemini_generator import generate_fitness_plan

# router-ஐ முதலில் create செய்ய வேண்டும்
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@router.post("/generate-plan")
def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    goal: str = Form(...),
    dietary_preference: str = Form(...),
    fitness_level: str = Form(...),
    db: Session = Depends(get_db)
):
    plan_text = generate_fitness_plan(
        name=name, age=age, gender=gender, weight=weight, height=height,
        goal=goal, dietary_preference=dietary_preference, fitness_level=fitness_level
    )

    # Images for response
    workout_image = "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=800"
    diet_image = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=800"

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "plan": plan_text,
            "name": name,
            "workout_image": workout_image,
            "diet_image": diet_image
        }
    )
