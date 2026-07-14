from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Path

from sqlalchemy import select, func

from database import SessionLocal
from models import Post
import math

router = APIRouter(prefix="/posts", tags=["게시글"])


@router.post("/")
def create_post(
    category: str,
    title: str,
    content: str,
    nickname: str,
    password: str,
):

    with SessionLocal() as db:

        post = Post(
            category=category,
            title=title,
            content=content,
            nickname=nickname,
            password=password,
            view_count=0,
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return {"message": "작성 완료", "post_id": post.id}


@router.get("/{post_id}")
def get_post(post_id: Annotated[int, Path(description="게시글 ID")]):

    with SessionLocal() as db:

        post = db.get(Post, post_id)

        if not post:
            raise HTTPException(status_code=404, detail="게시글 없음")

        # 조회수 증가
        post.view_count += 1

        db.commit()
        db.refresh(post)

        return {
            "id": post.id,
            "category": post.category,
            "title": post.title,
            "content": post.content,
            "nickname": post.nickname,
            "view_count": post.view_count,
            "created_at": post.created_at,
        }


@router.get("/")
def get_posts(
    page: Annotated[int, Query(description="현재 페이지", ge=1, example=1)] = 1,
    limit: Annotated[
        int, Query(description="페이지당 출력 개수", ge=1, le=100, example=10)
    ] = 10,
):

    with SessionLocal() as db:

        offset = (page - 1) * limit

        # 전체 게시글 개수
        total_count = db.scalar(select(func.count(Post.id)))

        # 전체 페이지 수
        total_pages = math.ceil(total_count / limit)

        posts = db.scalars(
            select(Post).order_by(Post.id.desc()).offset(offset).limit(limit)
        ).all()

        data = []

        for post in posts:
            data.append(
                {
                    "id": post.id,
                    "category": post.category,
                    "title": post.title,
                    "nickname": post.nickname,
                    "view_count": post.view_count,
                    "created_at": post.created_at,
                }
            )

        return {
            "page": page,
            "limit": limit,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages,
            "data": data,
        }


@router.put("/{post_id}")
def update_post(
    post_id: int,
    password: str,
    category: str,
    title: str,
    content: str,
):

    with SessionLocal() as db:

        post = db.get(Post, post_id)

        if not post:
            raise HTTPException(404, "게시글 없음")

        if post.password != password:

            raise HTTPException(403, "비밀번호 불일치")

        post.category = category
        post.title = title
        post.content = content

        db.commit()

        return {"message": "수정 완료"}


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    password: str,
):
    with SessionLocal() as db:

        post = db.get(Post, post_id)

        if not post:
            raise HTTPException(status_code=404, detail="게시글이 없습니다.")

        # 비밀번호 확인
        if post.password != password:
            raise HTTPException(status_code=403, detail="비밀번호가 틀렸습니다.")

        db.delete(post)
        db.commit()

        return {"message": "삭제 완료"}
