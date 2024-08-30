from router import blog_get
from router import blob_post
from router import user
from db import models
from db.database import engine


from fastapi import FastAPI, status, Response
from enum import Enum
from typing import Optional

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blob_post.router)
app.include_router(user.router)

############################################################
# example de requête get


@app.get("/hello")
def index():
    return {"message": "coucou"}


@app.get('/pages', tags=['blog'])  # paramètres de query
def get_pages(page: int = 1, page_size: Optional[int] = 10):
    return {"message": f"{page_size} blogs on page {page} "}


# se placer dans le bon répertoire (reload pour recharger le charger à chaque fois qu'il y a une modif) ou sinon
# uvicorn simplon.main:app --reload   pour lancer le server
# puis http://127.0.0.1:8000/hello
# puis http://127.0.0.1:8000/docs  pour tester si les requêtes fonctionnent (format swagger, doc de l'API)

###########################################
# 3. Création dans le main

models.Base.metadata.create_all(engine)
