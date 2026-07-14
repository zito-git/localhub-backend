from fastapi import APIRouter

router = APIRouter(prefix="/posts", tags=["posts"])


# @router.get("/")
# def get_posts():
#     return {"message": "post list"}


# @router.post("/")
# def create_post():
#     return {"message": "post created"}
