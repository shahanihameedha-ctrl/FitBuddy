from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routes import router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(router)
