from pydantic import BaseModel
import random
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

import pathlib  # built in library

##############################################################
# create fastAPI app

app = FastAPI()


##############################################################
# configure templates and static folders

parent_path = pathlib.Path(__file__).parent.parent
app.mount(
    "/mount",
    StaticFiles(directory=parent_path/"static"),
    name="static")
templates = Jinja2Templates(directory=parent_path/"templates")


##############################################################
# configure the routes


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# run the app
# python3 -m uvicorn scripts.test-fullstack-fastapi:app --reload --port=8000
