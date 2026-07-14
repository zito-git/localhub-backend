from fastapi import FastAPI, status
from routers import posts, data

from fastapi import FastAPI

app = FastAPI(
    title="localhub Gumi API",
    description="""
구미·경북권 관광 데이터를 조회하는 REST API입니다.
""",
)

app.include_router(posts.router)
app.include_router(data.router)


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "mainPage1"}
