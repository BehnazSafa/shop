from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from database import Base, engine
from routers import products, curtains
import os
# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Textile Shop")

app.include_router(products.router)
app.include_router(curtains.router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "../frontend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "../frontend", "static")
if not os.path.exists(TEMPLATES_DIR):
    raise Exception(f"Template folder not found: {TEMPLATES_DIR}")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/test")
def test():
    return {"msg": "FastAPI is running!"}
