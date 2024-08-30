from fastapi import FastAPI, status, Response
from enum import Enum
from typing import Optional

app = FastAPI()

############################################################
# example de requête get


@app.get("/hello")
def index():
    return {"message": "coucou"}


# attention à définir en premier car maintenant erreur car sinon après la route /blog/ attend un integer


@app.get(
    '/blog/all',
    tags=['blog'],
    summary="Get all blogs",
    description="API call that stimulates getting all blogs", response_description="list of all blogs")  # paramètres de path
def get_all_blogs():
    return {"message": "All Blogs "}


# tout ensemble
@app.get("/blog/{id}/comments/{comment_id}", tags=['blog', "comment"])
def get_comment(id: int, comment_id: int, valid: bool = True, pseudo: Optional[str] = None):
    """Simulates getting on comment of a blog
    - **id** required path parameter..."""
    return {"message": f"comment {comment_id} on blog {id} by {pseudo}, {valid}"}


class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"


@app.get('/blog/type/{type}', tags=['blog'])  # paramètres prédéfinis
def get_blog_type(type: BlogType):
    return {"message": f"Blog {type=}"}


@app.get('/pages', tags=['blog'])  # paramètres de query
def get_pages(page: int = 1, page_size: Optional[int] = 10):
    return {"message": f"{page_size} blogs on page {page} "}


# paramètre de path avec status code.
@app.get('/blog/{id}', status_code=status.HTTP_200_OK, tags=['blog'])
def get_blog(id: int, response: Response):
    if id >= 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f"Blog {id=} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog {id}"}


# se placer dans le bon répertoire (reload pour recharger le charger à chaque fois qu'il y a une modif) ou sinon
# uvicorn simplon.main:app --reload   pour lancer le server
# puis http://127.0.0.1:8000/hello
# puis http://127.0.0.1:8000/docs  pour tester si les requêtes fonctionnent (format swagger, doc de l'API)
