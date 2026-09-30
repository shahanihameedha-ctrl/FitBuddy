from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from ai.gemini_client import generate_fitness_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/generate")
async def generate_plan(request: Request, goal: str = Form(...), age: int = Form(...)):
    plan = generate_fitness_plan(goal, age)
    return templates.TemplateResponse(
        request=request, 
        name="result.html", 
        context={"plan": plan}
    )
