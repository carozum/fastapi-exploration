from fastapi import status, Response, APIRouter
from enum import Enum
from typing import Optional

router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)

# attention à définir en premier car maintenant erreur car sinon après la route /blog/ attend un integer


@router.get(
    '/all',
    summary="Get all blogs",
    description="API call that stimulates getting all blogs", response_description="list of all blogs")  # paramètres de path
def get_all_blogs():
    return {"message": "All Blogs "}


# tout ensemble
@router.get("/{id}/comments/{comment_id}", tags=["comment"])
def get_comment(id: int, comment_id: int, valid: bool = True, pseudo: Optional[str] = None):
    """Simulates getting on comment of a blog
    - **id** required path parameter..."""
    return {"message": f"comment {comment_id} on blog {id} by {pseudo}, {valid}"}


class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"


@router.get('/type/{type}', tags=['blog'])  # paramètres prédéfinis
def get_blog_type(type: BlogType):
    return {"message": f"Blog {type=}"}


# paramètre de path avec status code.
@router.get('/{id}', status_code=status.HTTP_200_OK, tags=['blog'])
def get_blog(id: int, response: Response):
    if id >= 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f"Blog {id=} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog {id}"}
