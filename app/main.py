from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes import router

app = FastAPI(title="FitBuddy")

#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
