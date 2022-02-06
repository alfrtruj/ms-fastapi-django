import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI() #REST API
templates = Jinja2Templates(directory=str(BASE_DIR / "templates")) # print(BASE_DIR / "templates") - to check the path

@app.get("/", response_class=HTMLResponse) #http get -- return json
def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
def home_detail_view():
    return {"hello": "world"}