from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db, FitnessPlan
from app.gemini_generator import generate_fitness_plan

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
    # Gemini API Call to generate plan
    ai_plan = generate_fitness_plan(
        name=name, age=age, gender=gender, weight=weight, 
        height=height, goal=goal, dietary_preference=dietary_preference, 
        fitness_level=fitness_level
    )

    # Save details to database
    db_plan = FitnessPlan(
        name=name, age=age, gender=gender, weight=weight,
        height=height, goal=goal, dietary_preference=dietary_preference,
        fitness_level=fitness_level, generated_plan=ai_plan
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    return templates.TemplateResponse(
        request=request, 
        name="result.html", 
        context={"plan": ai_plan, "name": name}
    )

@router.get("/view-all-users")
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(FitnessPlan).all()
    return templates.TemplateResponse(
        request=request, 
        name="all_users.html", 
        context={"users": users}
    )
