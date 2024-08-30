from fastapi import APIRouter, Query, Body, Path
from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel


router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'date': "01/01/2000"},
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_blog(id: int, blog: BlogModel, v: int = 1):
    return {
        "id": id,  # paramètre path
        "blog info": blog,  # parametre body
        "version": v}      # parametre query


@router.post("/new/{id}/comment/{comment_id}")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: str = Query(
        None,
        title="Id of comment",
        description="description of the comment",
        alias="commentTitle",
        deprecated=False),
    content: str = Body(
        ...,  # obligatoire
        min_length=10,  # éléments de validation
        max_length=40,
        regex="^[a-z]*$"
    ),
    comment_id: int = Path(le=5),
    v: Optional[List[str]] = Query(['1.3', '1.1']),  # multiple ou rien ou None

):
    return {
        "id": id,
        "blog_info": blog,
        "comment_title": comment_title,
        "comment_id": comment_id,
        "content": content
    }
