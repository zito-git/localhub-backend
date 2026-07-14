from fastapi import FastAPI, status
from routers import posts, data

from fastapi import FastAPI

# DB
from database import engine
from models import Base
from routers import posts

# CORS
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="localhub Gumi API",
    description="""
구미·경북권 관광 데이터를 조회하는 REST API입니다.
""",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용(GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)


app.include_router(posts.router)
app.include_router(data.router)


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "mainPage1"}
