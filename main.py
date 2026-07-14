from fastapi import FastAPI, status
from routers import posts

app = FastAPI()
app.include_router(posts.router)


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "mainPage1"}
