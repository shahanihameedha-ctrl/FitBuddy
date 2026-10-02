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

    # Goal-க்கு ஏற்றவாறு படங்கள்
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
