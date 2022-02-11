import pathlib
import os
import io
from functools import lru_cache
import uuid
from fastapi import Depends, FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings


class Settings(BaseSettings): #manage the debug variable for development or production
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG=settings.debug
print(DEBUG)

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"

app = FastAPI() #REST API
templates = Jinja2Templates(directory=str(BASE_DIR / "templates")) # print(BASE_DIR / "templates") - to check the path

@app.get("/", response_class=HTMLResponse) #http GET -- return json
def home_view(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/") #http POST
def home_detail_view():
    return {"hello": "world"}


@app.post("/img-echo/", response_class=FileResponse)
async def img_echo_view(file:UploadFile = File(...), settings: Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint", status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    with open(str(dest), 'wb') as out:
        out.write(bytes_str.read())
    return dest
