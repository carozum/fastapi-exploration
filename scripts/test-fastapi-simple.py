# pip install "fastapi[standard]"
# in dev mode : fastapi dev scripts/test-fastapi-simple.py
# http://127.0.0.1:8000/generate_name
# http://127.0.0.1:8000/docs

# in production mode : fastapi run

from pydantic import BaseModel
import random
import fastapi


# create a fastapi app
app = fastapi.FastAPI()

# define the main route


@app.get("/")
async def index():
    return {"operation": "index"}

############################################################
# handling get requests


@app.get("/generate_name")
async def generate_name():
    # define an api route as an async function
    names = ["Minnie", "Margaret", "Myrtle", "Noa", "Nadia"]
    random_name = random.choice(names)
    return {"name": random_name}

############################################################
# handling get requests with parameters


@app.get("/generate_name_2")
async def generate_name_2(
        starts_with: str = None,
        min_length: int = None):
    # adding a starts_with parameter optional (as with default value)
    names = ["Minnie", "Margaret", "Myrtle", "Noa", "Nadia"]
    if starts_with is not None:
        names = [name for name in names if name.lower(
        ).startswith(starts_with.lower())]
    if min_length is not None:
        names = [name for name in names if len(name) >= min_length]
    if len(names) == 0:
        raise fastapi.HTTPException(404, "No Names Found")
    random_name = random.choice(names)
    return {"name": random_name}

############################################################
# handling post requests


class NameRequests(BaseModel):
    starts_with: str = None
    min_length: int


@app.post("/generate_name_2")
async def generate_name_2(name_request: NameRequests):
    names = ["Minnie", "Margaret", "Myrtle", "Noa", "Nadia"]
    if name_request.starts_with is not None:
        names = [name for name in names if name.lower(
        ).startswith(name_request.starts_with.lower())]
    if name_request.min_length is not None:
        names = [name for name in names if len(
            name) >= name_request.min_length]
    if len(names) == 0:
        raise fastapi.HTTPException(404, "No names found")
    random_name = random.choice(names)
    return {"name": random_name}
